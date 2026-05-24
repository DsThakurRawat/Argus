# Argus: Multi-Provider Autonomous Monitoring and Remediation

[![GitHub Stars](https://img.shields.io/github/stars/avivl/argus.svg?style=for-the-badge&logo=github&color=gold)](https://github.com/avivl/argus/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/avivl/argus?style=for-the-badge&logo=github)](https://github.com/avivl/argus)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Multi-Provider AI](https://img.shields.io/badge/Multi--Provider%20AI-00BCD4?style=for-the-badge&logo=openai&logoColor=fff)](https://github.com/avivl/argus)
![Argus](static/argus_agent.png)

Welcome to Argus, an autonomous multi-provider SRE assistant designed to enhance cloud operations by intelligently monitoring logs and automating incident response. This project leverages the power of 100+ AI providers (OpenAI, Anthropic, Google, Cohere, Ollama, and more) directly in SRE workflows.

At its core, Argus continuously observes your cloud environment. When anomalies or critical events are detected in your logs, it initiates a structured process of analysis, generates intelligent code fixes using a unified code generation system, and proposes concrete remediation steps via automated GitHub Pull Requests.

---

## 🏗️ System Architecture

Argus employs a modular, event-driven architecture designed for high availability, cost efficiency, and multi-provider redundancy.

* **Log Ingestion:** Pluggable adapters that standardise and ingest raw log streams.
* **Triage & Pattern Detection:** Quick triage filtering and multi-layer analysis of log anomalies.
* **Deep Analysis & Verification:** Context-aware root cause analysis backed by empirical, code-executing verification.
* **Unified Code Generation:** Domain-specific code generators targeting API, database, and security fixes.
* **Automated Remediation:** Code packaging and pull request assembly with human-in-the-loop validation.

For a full breakdown of the architecture, data flows, and provider strategies:
👉 See the [**System Architecture Overview**](docs/ARCHITECTURE.md).

---

## 🛠️ Key Capabilities

* **Enterprise Log Ingestion:** Ingest from GCP Pub/Sub, Kubernetes, AWS CloudWatch, or local files with built-in backpressure, retries, and circuit breakers.
* **4-Layer Pattern Detection:** Detects cascade failures, resource exhaustion, and service degradations via sliding window thresholds and confidence scoring.
* **ML Pattern Refinement:** Optimises log analysis via pre-processing validation, sensitive data sanitisation (PII/credential scrubbing), and similarity caching.
* **Dynamic Prompt Generation:** Revolutionary "AI teaching AI" meta-prompting and domain-specific prompt templates.
* **Unified Code Generation:** Features automated syntax validation, security checks, and best practices scanning.
* **Multi-Service & Multi-Repo Support:** Simultaneously monitor multiple cloud systems and route pull requests to different target repositories.

---

## 📚 Documentation Directory

Explore the sub-systems and configuration guides in detail:

### Core Systems
* [**System Architecture & Flow**](docs/ARCHITECTURE.md) - Deep dive into core SRE loop, data flows, and sequential design.
* [**Log Ingestion Guide**](docs/LOG_INGESTION_SYSTEM_GUIDE.md) - Deploying and managing the enterprise log ingestion adapters.
* [**4-Layer Pattern Detection**](docs/PATTERN_DETECTION_SYSTEM.md) - How sliding window logic, classifications, and confidence metrics work.
* [**ML Pattern Refinement System**](docs/ML_PATTERN_REFINEMENT.md) - Quality validation, sanitization, and response cache optimization.
* [**Dynamic Prompt Generation**](docs/ENHANCED_PROMPT_GENERATION.md) - Details on adaptive prompting strategy and meta-prompt engines.
* [**Unified Code Generation**](docs/UNIFIED_ENHANCED_CODE_GENERATION.md) - Workflows, specialized generators, and the multi-level validation pipeline.

### Setup & Operations
* [**Quick Start Guide**](docs/QUICKSTART.md) - Get the agent up and running in 15 minutes.
* [**Setup and Installation**](docs/SETUP_INSTALLATION.md) - Comprehensive setup and environment preparation details.
* [**Configuration Guide**](docs/CONFIGURATION.md) - Customising agent behavior using type-safe Pydantic configuration.
* [**GCP Infrastructure Setup**](docs/GCP_SETUP.md) - Preparing Google Cloud components (Pub/Sub, IAM, Logging).
* [**Deployment Guide**](docs/DEPLOYMENT.md) - Guidelines for running on Cloud Run, Kubernetes, or other runtimes.
* [**Operations Runbook**](docs/OPERATIONS.md) - Monitoring, error recovery, and day-2 operations guidelines.
* [**Troubleshooting & Flow Tracking**](docs/TROUBLESHOOTING.md) - Debugging problems using flow and execution tracking.
* [**Development & Contributing Guide**](docs/DEVELOPMENT.md) - Code style, local testing, and submission workflows.

---

## 🚀 Getting Started

Ensure you have Python 3.12+ and `uv` installed.

1. **Clone the repository and install dependencies:**
   ```bash
   uv sync
   ```

2. **Authenticate with GCP and set your token:**
   ```bash
   gcloud auth application-default login
   export GITHUB_TOKEN="your_github_token_here"
   ```

3. **Configure log ingestion feature flags:**
   ```bash
   export USE_LOG_INGESTION_SYSTEM=true
   export ENABLE_MONITORING=true
   export ENABLE_LEGACY_FALLBACK=true
   ```

4. **Define your services in `config/config.yaml` and run the orchestrator:**
   ```bash
   python main.py
   ```

---

## 🤝 Contributing

We welcome contributions! Please refer to the [Development Guide](docs/DEVELOPMENT.md) to understand local testing patterns, syntax checking rules, and CI setup.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
