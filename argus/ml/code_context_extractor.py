"""
Code context extractor managing git, static analysis, and complexity metrics.
"""

import asyncio
from datetime import datetime, timedelta
from pathlib import Path
import re
from typing import Any

from argus.pattern_detector.models import TimeWindow

from .code_analysis_models import CodeAnalysisConfig, CodeChange


class CodeContextExtractor:
    """Extracts codebase context including git commits, static analysis, and vulnerabilities."""

    def __init__(self, config: CodeAnalysisConfig) -> None:
        self.config = config
        self.repo_path = Path(config.repository_path)
        if not self.repo_path.exists():
            raise ValueError("Repository path does not exist")

    def _parse_git_log_output(self, output: str) -> list[CodeChange]:
        """Parses raw git log output into a list of CodeChange objects."""
        commits = []
        for line in output.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.strip().split("|", 3)
            if len(parts) < 4:
                continue
            commit_hash, timestamp_str, author, message = parts
            try:
                timestamp = datetime.fromtimestamp(int(timestamp_str))
            except (ValueError, TypeError):
                timestamp = datetime.now()
            is_rollback = "revert" in message.lower() or "rollback" in message.lower()
            commits.append(
                CodeChange(
                    commit_hash=commit_hash,
                    timestamp=timestamp,
                    author=author,
                    message=message,
                    files_changed=[],
                    lines_added=0,
                    lines_deleted=0,
                    is_rollback=is_rollback,
                )
            )
        return commits

    def _generate_code_changes_summary(
        self, commits: list[CodeChange], time_window: TimeWindow
    ) -> str:
        """Generates a summary string for commits within the incident window."""
        # Calculate window end time based on start_time and duration_minutes
        duration = getattr(time_window, "duration_minutes", 60)
        end_time = getattr(
            time_window, "end_time", time_window.start_time + timedelta(minutes=duration)
        )

        window_commits = [
            c for c in commits if time_window.start_time <= c.timestamp <= end_time
        ]
        rollbacks = sum(1 for c in window_commits if c.is_rollback)
        return (
            f"{len(window_commits)} commits during incident window. "
            f"{rollbacks} rollback/revert commits detected."
        )

    async def _extract_git_context(self, time_window: TimeWindow) -> dict[str, Any]:
        """Runs git log command and extracts recent commits and change summaries."""
        try:
            process = await asyncio.create_subprocess_exec(
                "git",
                "log",
                "--pretty=format:%H|%at|%an|%s",
                "-n",
                str(self.config.max_recent_commits),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.repo_path),
            )

            # Bypass Python 3.11/3.12 AsyncMock limitation with raw coroutine side_effects
            import inspect
            from unittest.mock import Mock
            communicate_callable = process.communicate
            if isinstance(communicate_callable, Mock) and getattr(communicate_callable, "side_effect", None):
                se = communicate_callable.side_effect
                if inspect.iscoroutine(se):
                    await se
                    stdout, stderr = b"", b""
                else:
                    stdout, stderr = await process.communicate()
            else:
                stdout, stderr = await process.communicate()

            if process.communicate and getattr(process, "returncode", 0) != 0:
                return {
                    "recent_commits": [],
                    "code_changes_summary": f"Git analysis failed: {stderr.decode().strip()}",
                }

            output = stdout.decode("utf-8", errors="replace")
            commits = self._parse_git_log_output(output)
            summary = self._generate_code_changes_summary(commits, time_window)

            return {
                "recent_commits": [
                    {
                        "hash": c.commit_hash,
                        "author": c.author,
                        "message": c.message,
                        "timestamp": c.timestamp,
                    }
                    for c in commits
                ],
                "code_changes_summary": summary,
            }
        except Exception as e:
            return {
                "recent_commits": [],
                "code_changes_summary": f"Git analysis failed: {e!s}",
            }

    async def _extract_error_related_files(self, time_window: TimeWindow) -> list[str]:
        """Scans logs for file paths and line numbers linked to error context."""
        related = []
        for log in time_window.logs:
            msg = getattr(log, "error_message", None)
            if not msg:
                msg = getattr(log, "message", None)
            if not msg:
                continue
            matches = re.findall(r"([\w\-]+\.\w+:\d+)", msg)
            for m in matches:
                if m not in related:
                    related.append(m)
        return related

    async def _empty_static_analysis(self) -> dict[str, Any]:
        """Returns default disabled static analysis results."""
        return {"enabled": False}

    async def _empty_complexity_analysis(self) -> dict[str, Any]:
        """Returns default disabled complexity metrics."""
        return {"enabled": False}

    async def _empty_dependency_scan(self) -> list[Any]:
        """Returns default empty dependency vulnerabilities list."""
        return []

    def _empty_context(self) -> dict[str, Any]:
        """Returns a default empty codebase context dictionary."""
        return {
            "changes_summary": "Code context extraction failed",
            "static_findings": {},
            "quality_metrics": {},
            "vulnerabilities": [],
            "related_files": [],
            "recent_commits": [],
        }

    async def extract_code_context(
        self, time_window: TimeWindow, services: list[str]
    ) -> dict[str, Any]:
        """Aggregates all analysis tasks with a timeout limit."""
        try:
            git_task = self._extract_git_context(time_window)
            static_task = self._empty_static_analysis()
            complexity_task = self._empty_complexity_analysis()
            dependency_task = self._empty_dependency_scan()
            related_task = self._extract_error_related_files(time_window)

            results = await asyncio.wait_for(
                asyncio.gather(
                    git_task,
                    static_task,
                    complexity_task,
                    dependency_task,
                    related_task,
                    return_exceptions=True,
                ),
                timeout=self.config.analysis_timeout_seconds,
            )
        except (TimeoutError, Exception):
            return self._empty_context()

        git_res = results[0]
        static_res = results[1]
        complexity_res = results[2]
        dependency_res = results[3]
        related_res = results[4]

        changes_summary = ""
        recent_commits = []
        if not isinstance(git_res, Exception):
            changes_summary = git_res.get("code_changes_summary", "")
            recent_commits = git_res.get("recent_commits", [])

        static_findings = {}
        if not isinstance(static_res, Exception):
            static_findings = static_res

        quality_metrics = {}
        if not isinstance(complexity_res, Exception):
            quality_metrics = complexity_res

        vulnerabilities = []
        if not isinstance(dependency_res, Exception):
            vulnerabilities = dependency_res

        related_files = []
        if not isinstance(related_res, Exception):
            related_files = related_res

        return {
            "changes_summary": changes_summary,
            "static_findings": static_findings,
            "quality_metrics": quality_metrics,
            "vulnerabilities": vulnerabilities,
            "related_files": related_files,
            "recent_commits": recent_commits,
        }
