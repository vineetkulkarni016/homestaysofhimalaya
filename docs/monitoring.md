# Monitoring and Alerting

This project uses [Datadog](https://www.datadoghq.com/) for metrics, traces, and logs and runs [Snyk](https://snyk.io/) in CI to detect security issues.

## Datadog Setup

- The application runs alongside a Datadog agent defined in `docker-compose.yml`.
- Metrics and traces are sent to the agent via environment variables such as `DD_AGENT_HOST` and `DD_SERVICE`.
- Dashboards and monitors can be imported using the files in the `datadog/` directory.
  - `dashboard.json` visualizes request latency and error rate.
  - `monitors.json` defines alerts for high latency and high error rates.

## Alerting Policies

- **High request latency**
  - Triggered when the 95th percentile of request latency exceeds 1 second over 5 minutes.
  - Alerts notify the on-call engineer via PagerDuty.
- **High error rate**
  - Triggered when error rate exceeds 5% over 5 minutes.
  - Alerts notify the on-call engineer via PagerDuty.

## Response Runbooks

### High request latency
1. Confirm alert in Datadog and identify affected endpoints.
2. Check recent deployments or infrastructure changes.
3. Examine service logs for slow queries or external dependency issues.
4. Mitigate by reverting recent changes or scaling resources.
5. Once resolved, document the incident in the issue tracker.

### High error rate
1. Confirm alert and inspect error logs for stack traces.
2. Roll back recent releases if a bug is suspected.
3. Verify dependency availability (databases, external APIs).
4. Communicate status to stakeholders until resolved.
5. Record root cause and remediation steps.

## Snyk in CI

`Snyk` is executed in GitHub Actions (`.github/workflows/snyk.yml`) and fails the build on critical vulnerabilities.
