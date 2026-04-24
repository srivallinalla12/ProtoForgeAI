diff --git a/README.md b/README.md
index e34c62c9b9be3c695d5e805ed01ed283ede0834d..07c58b495e9c2c22f92b491339d25d0042a0c7fb 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,81 @@
-# Codex_Challenge
\ No newline at end of file
+# Codex_Challenge
+
+Production-style multi-agent system that turns a product idea into a tested working prototype.
+
+## Public Website (GitHub Pages)
+
+- **Website URL (after pushing to your GitHub `main` branch and enabling Pages):**
+  `https://<YOUR_GITHUB_USERNAME>.github.io/Codex_Challenge/`
+- The static site content lives in `docs/index.html` and is deployed by `.github/workflows/deploy-pages.yml`.
+
+### One-time setup to make the site publicly viewable
+
+1. Push this repository to your GitHub account as `Codex_Challenge`.
+2. In GitHub, go to **Settings → Pages** and ensure **GitHub Actions** is selected as the source.
+3. Push to `main` (or run the workflow manually in **Actions → Deploy public website (GitHub Pages)**).
+4. Open the deployed URL:
+   `https://<YOUR_GITHUB_USERNAME>.github.io/Codex_Challenge/`
+
+## What this system does
+
+Given a high-level product idea, the pipeline:
+
+1. Creates milestones and orchestrates agents.
+2. Produces product specs (requirements, features, user stories, API contracts).
+3. Proposes architecture and service boundaries.
+4. Generates runnable prototype files.
+5. Runs unit/integration tests and reports failures.
+6. Evaluates quality, maintainability, scalability, and security.
+7. Iterates automatically when tests or architecture checks fail.
+8. Emits structured logs and a build summary.
+
+## Layered agent architecture
+
+- **Orchestration layer**: `OrchestratorAgent` coordinates stage execution, retry logic, and status tracking.
+- **Planning layer**: `SpecificationAgent` + `ArchitectureAgent` create the plan and constraints.
+- **Execution layer**: `ImplementationAgent` writes implementation artifacts.
+- **Verification layer**: `TestingAgent` runs tests and returns structured failures.
+- **Evaluation layer**: `EvaluationAgent` assesses quality risks and refactor opportunities.
+
+## Run
+
+```bash
+PYTHONPATH=src python -m mas.cli "Build a lightweight product-feedback tracker for internal teams"
+```
+
+Example output includes:
+- final working prototype path under `build_outputs/iteration_*/prototype`
+- test pass/fail status
+- risk assessment
+- technical debt
+- next-iteration roadmap
+
+## Scaling to enterprise-level pipelines
+
+This prototype is intentionally synchronous for determinism, but scales with these production adaptations:
+
+1. **Event-driven orchestration**
+   - Replace in-process loop with a workflow engine (Temporal/Argo/Step Functions).
+   - Persist stage state and retries in durable storage.
+
+2. **Parallelizable task graph**
+   - Split milestone work into independent subtasks (spec decomposition, code generation per module, parallel test shards).
+   - Use a queue (Kafka/SQS/PubSub) for fan-out/fan-in.
+
+3. **Pluggable agent runtime**
+   - Define common agent contracts so teams can swap models/providers or rules engines.
+   - Add policy agents (security/compliance) as mandatory gates.
+
+4. **Enterprise observability**
+   - Emit traces/metrics/logs to OpenTelemetry + centralized dashboards.
+   - Track per-agent latency, cost, retry rates, and defect escape rate.
+
+5. **Governance and safety gates**
+   - Add human approvals for high-risk changes.
+   - Enforce RBAC, secrets scanning, SBOM generation, SAST/DAST checks.
+
+6. **Progressive delivery**
+   - Auto-create feature branches and ephemeral environments.
+   - Run canary experiments before production rollout.
+
+These upgrades preserve the same layer boundaries in this repo while enabling high-throughput, auditable enterprise feature pipelines.
