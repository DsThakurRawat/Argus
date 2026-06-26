# argus/ml/gemini_response_cache.py

"""
Intelligent caching system for Gemini API responses.
"""

from datetime import datetime, timedelta
import hashlib
import json
from typing import Any

from argus.ml.gemini_api_client import GeminiResponse
from argus.ml.schemas import PatternContext


class GeminiResponseCache:
    """Caches Gemini API responses with similarity-based matching and TTL/LRU eviction."""

    def __init__(
        self,
        max_cache_size: int = 1000,
        ttl_hours: float = 24.0,
        similarity_threshold: float = 0.85,
    ) -> None:
        self.max_cache_size = max_cache_size
        self.ttl_seconds = int(ttl_hours * 3600)
        self.similarity_threshold = similarity_threshold
        self.cache: dict[str, dict[str, Any]] = {}
        self.access_times: dict[str, datetime] = {}

    def _compute_context_hash(self, context: PatternContext) -> str:
        """Compute 16-character SHA256 hash of context fields."""

        def _serialize_val(val: Any) -> Any:
            if isinstance(val, datetime):
                return val.isoformat()
            elif isinstance(val, (dict, list)):
                return val
            elif hasattr(val, "__dict__"):
                return val.__dict__
            else:
                return str(val) if val is not None else ""

        fields = {}
        # Ensure we sort the keys for a deterministic hash representation
        for k in sorted(context.__dict__.keys()):
            fields[k] = _serialize_val(getattr(context, k))

        serialized = json.dumps(fields, sort_keys=True, ensure_ascii=False)
        h = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        return h[:16]

    def _compare_dict_fields(self, dict1: dict | None, dict2: dict | None) -> float:
        """Compare two dictionary fields and return similarity from 0.0 to 1.0."""
        if dict1 is None and dict2 is None:
            return 1.0
        if dict1 is None or dict2 is None:
            return 0.0
        if not dict1 and not dict2:
            return 1.0

        all_keys = set(dict1.keys()) | set(dict2.keys())
        if not all_keys:
            return 1.0

        matching = 0
        for k in all_keys:
            if k in dict1 and k in dict2 and dict1[k] == dict2[k]:
                matching += 1
        return matching / len(all_keys)

    def _compute_similarity(self, context1: PatternContext, context2: PatternContext) -> float:
        """Compute similarity score between two contexts from 0.0 to 1.0."""
        # 1. Primary service similarity
        p1 = context1.primary_service
        p2 = context2.primary_service
        sim_primary = 1.0 if p1 == p2 else 0.0

        # 2. Affected services similarity (Jaccard similarity)
        a1 = set(context1.affected_services or [])
        a2 = set(context2.affected_services or [])
        if not a1 and not a2:
            sim_affected = 1.0
        elif not a1 or not a2:
            sim_affected = 0.0
        else:
            sim_affected = len(a1 & a2) / len(a1 | a2)

        # 3. Error patterns similarity
        sim_err = self._compare_dict_fields(context1.error_patterns, context2.error_patterns)

        return (sim_primary + sim_affected + sim_err) / 3.0

    async def cache_response(
        self, context: PatternContext, model: str, response: GeminiResponse
    ) -> None:
        """Cache a successful Gemini Response."""
        if not response.success:
            return

        h = self._compute_context_hash(context)
        key = f"{model}:{h}"

        now = datetime.now()
        self.cache[key] = {"response": response, "context": context, "timestamp": now}
        self.access_times[key] = now

        if len(self.cache) > self.max_cache_size:
            await self._evict_lru_entries()

    async def get_cached_response(
        self, context: PatternContext, model: str
    ) -> GeminiResponse | None:
        """Retrieve cached response with exact or similarity match."""
        h = self._compute_context_hash(context)
        key = f"{model}:{h}"
        now = datetime.now()

        # Try exact match first
        if key in self.cache:
            entry = self.cache[key]
            if now - entry["timestamp"] > timedelta(seconds=self.ttl_seconds):
                del self.cache[key]
                self.access_times.pop(key, None)
                return None
            self.access_times[key] = now
            return entry["response"]

        # Try similarity matching
        similar_match_key = None
        highest_similarity = 0.0

        keys_to_delete = []
        for cached_key, entry in self.cache.items():
            # Check model compatibility
            if not cached_key.startswith(f"{model}:"):
                continue

            # Check expiration
            if now - entry["timestamp"] > timedelta(seconds=self.ttl_seconds):
                keys_to_delete.append(cached_key)
                continue

            sim = self._compute_similarity(context, entry["context"])
            if sim >= self.similarity_threshold and sim > highest_similarity:
                highest_similarity = sim
                similar_match_key = cached_key

        # Clean up expired keys checked during iteration
        for k in keys_to_delete:
            self.cache.pop(k, None)
            self.access_times.pop(k, None)

        if similar_match_key:
            self.access_times[similar_match_key] = now
            return self.cache[similar_match_key]["response"]

        return None

    async def _evict_lru_entries(self) -> None:
        """Evict ~20% of entries using LRU policy."""
        if not self.cache:
            return

        num_to_evict = max(1, len(self.cache) // 5)
        # Sort keys by access time ascending
        sorted_keys = sorted(
            self.access_times.keys(), key=lambda k: self.access_times.get(k, datetime.min)
        )

        for key in sorted_keys[:num_to_evict]:
            self.cache.pop(key, None)
            self.access_times.pop(key, None)

    def get_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        total_entries = len(self.cache)
        now = datetime.now()

        expired_entries = 0
        model_distribution = {}
        for key, entry in self.cache.items():
            if now - entry["timestamp"] > timedelta(seconds=self.ttl_seconds):
                expired_entries += 1

            model = key.split(":")[0]
            model_distribution[model] = model_distribution.get(model, 0) + 1

        oldest_age = self._get_oldest_entry_age_hours()

        return {
            "total_entries": total_entries,
            "max_cache_size": self.max_cache_size,
            "cache_utilization": total_entries / self.max_cache_size,
            "expired_entries": expired_entries,
            "model_distribution": model_distribution,
            "oldest_entry_age_hours": oldest_age,
            "ttl_hours": self.ttl_seconds / 3600.0,
        }

    def _get_oldest_entry_age_hours(self) -> float:
        """Calculate the age of the oldest entry in hours."""
        if not self.cache:
            return 0.0
        oldest_ts = min(entry["timestamp"] for entry in self.cache.values())
        return (datetime.now() - oldest_ts).total_seconds() / 3600.0
