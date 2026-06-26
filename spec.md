# Argus — Specification

**Argus** is an autonomous, multi-provider cloud SRE (Site Reliability Engineering) and AI monitoring assistant. It continuously ingests cloud logs, detects anomalies, triages errors with LLMs, generates code fixes, and proposes remediation via automated pull requests — a closed *Observe → Reason → Act → Heal* loop.

- **Language:** Python 3.12+
- **Package manager:** `uv`
- **Entry point:** `argus` CLI (`argus.cli.main:app`, built on Typer + Rich)
- **License:** MIT
- **Version:** 0.1.1 (pyproject) / 0.2.1 (CLI banner)

---

## 1. Goals

1. **Autonomous remediation** — go beyond alerting; diagnose root causes and open concrete PRs with fixes ready for human review.
2. **Provider independence** — switch freely across 100+ LLM providers (OpenAI, Anthropic, Google Gemini, Grok, Ollama, local models) with cost-aware routing and fallback.
3. **Pluggable ingestion** — support enterprise cloud log sources and modern PaaS webhook drains behind a uniform adapter interface.
4. **Operator-first UX** — interactive terminal wizard; no manual YAML editing required to get running.
5. **Safety** — validate and sanitize generated code; mask credentials and PII before any external call or commit.

## 2. Non-Goals

- Argus does not auto-merge fixes; a human reviews every PR.
- Not a metrics/APM replacement — it complements observability stacks, focused on log-driven triage and remediation.

---

## 3. System Architecture

Event-driven, modular pipeline:

```
Log Sources ──> Ingestion Manager ──> Triage & Pattern Detection ──> LLM Router
   (AWS/GCP/                                                              │
    K8s/PaaS)                                          ┌─────────────────┴─────────────────┐
                                                  Root Cause Analyzer            Code Generator
                                                       └──────────────┬──────────────┘
                                                              Automated PR Builder
                                                              (GitHub / GitLab)
```

### 3.1 Core Subsystems (`argus/`)

| Module | Responsibility |
|--------|----------------|
| `ingestion/` | Pluggable log adapters (GCP Pub/Sub, AWS CloudWatch, Azure, Kubernetes, local files, HTTP webhook drains for Vercel/Render/Railway/Cloudflare). Manager, processor, queues, monitoring. |
| `pattern_detector/` | 4-layer anomaly detection: cascade failures, resource exhaustion, service degradation. Sliding-window logic + ML similarity caching. |
| `llm/` | Multi-provider LLM framework: provider adapters, capability detection, model mixing/routing, cost monitoring, circuit breakers, fallback. |
| `agents/` | Agent abstractions and specialized agents (triage, analysis, code, remediation, text). Base + enhanced/optimized variants, request/response/state models. |
| `ml/` | Code-generation pipeline: specialized generators (database, API, security), multi-level validation, caching, performance, workflow orchestration. |
| `source_control/` | Git provider integrations (GitHub, GitLab), credential management, error handling, metrics — builds and pushes automated PRs. |
| `notifications/` | Alert routing to Slack, Discord, Telegram. |
| `security/` | PII/credential sanitization, secure handling of secrets. |
| `resilience/` + `core/resilience/` | Circuit breakers, retries (tenacity/hyx), rate limiting. |
| `core/` | Cross-cutting: dependency injection, interfaces, logging, performance, quality gates, types, validation, exceptions. |
| `config/` | Configuration models, loading, examples. |
| `metrics/` | Runtime metrics collection. |
| `cli/` | Typer-based interactive terminal UI. |

### 3.2 Core SRE Loop (`main.py`)

- `initialize_enhanced_agents(...)` — wires up the agent pipeline.
- `process_log_with_enhanced_pipeline(...)` — runs a single log entry through triage → analysis → code generation → remediation.
- `run_pipeline(...)` / `run_log_manager()` — drives continuous ingestion and per-entry processing.

---

## 4. CLI Surface

`argus <command>` (Typer app, Rich UI):

| Command | Description |
|---------|-------------|
| `argus init` | Initialize `~/.argus/` base directory and default `config.yaml`. |
| `argus run` | Launch the interactive dashboard / monitoring loop. Options: `--log-file/-l`, `--provider/-p`. |
| `argus config` | View and manage Argus configuration and keys interactively. |

Configuration lives at `~/.argus/config.yaml`. The interactive setup masks and stores API keys locally.

---

## 5. Pipeline Stages (functional spec)

1. **Ingest** — adapters normalize heterogeneous log sources into a uniform `LogEntry` and enqueue them through the ingestion manager.
2. **Detect** — pattern detector applies sliding-window + ML-similarity analysis to classify anomalies and suppress noise.
3. **Triage** — triage agent assesses severity and routes via the multi-provider LLM router (cost-aware, with circuit breakers and fallback).
4. **Analyze** — root-cause analyzer produces a structured diagnosis.
5. **Generate** — domain-specific code generators (database/API/security) produce fixes, passed through multi-level validation and PII/credential sanitization.
6. **Remediate** — source-control layer packages the fix into an automated PR (GitHub/GitLab) for human review.
7. **Notify** — alerts and status pushed to configured channels (Slack/Discord/Telegram).

---

## 6. Key Dependencies

- **LLM/AI:** `litellm`, `instructor`, `mirascope`, `anthropic`, `openai`, `google-generativeai`, `google-cloud-aiplatform`, `ollama`
- **Cloud/ingestion:** `google-cloud-logging`, `google-cloud-pubsub`, `boto3`, `kubernetes`, `aiohttp`, `aiofiles`
- **Resilience:** `tenacity`, `circuitbreaker`, `hyx`, `limits`, `slowapi`
- **Source control:** `PyGithub`, `python-gitlab`, `gitpython`, `patch-ng`
- **API/serving:** `fastapi`, `uvicorn`, `httpx`
- **Config/validation:** `pydantic`, `pydantic-settings`, `pyyaml`
- **CLI/UX:** `typer`, `click`, `rich`, `questionary`
- **Logging:** `structlog`

---

## 7. Quality & Tooling

- **Static analysis:** Pyright (`pyrightconfig.json`) — type-clean is a release gate.
- **Lint/format:** Ruff (`ruff.toml`), Bandit (`.bandit`), Trunk (`.trunk/`), pre-commit (`.pre-commit-config.yaml`).
- **Tests:** Pytest + pytest-asyncio (`pytest.ini`); markers `integration` and `slow`.
- **Build:** Hatchling.
- **CI/CD:** GitHub Actions (`.github/`).

---

## 8. Detailed Documentation

In-depth docs live under `docs/` — Architecture, Log Ingestion, Pattern Detection, Prompt Generation, Unified Code Generation, Multi-Provider LLM Configuration, Capability System, Error Handling, Secure Credential Management, Cost Management, Deployment, Operations, and setup/quickstart guides.
