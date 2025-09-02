# CI/CD

## Continuous Integration
Pull requests trigger the [CI workflow](../.github/workflows/ci.yml) which runs:
- **flake8** for linting
- **pytest** for unit tests
- **bandit** for security scanning

## Continuous Deployment
Merges to `main` run the [CD workflow](../.github/workflows/cd.yml) to deploy sequentially to:
1. `dev`
2. `test`
3. `qa`
4. `qa-staging`
5. `production` *(requires manual approval)*

Each job uses environment-specific secrets such as `DEV_API_KEY` and `PRODUCTION_API_KEY`.

### Deploying
1. Merge changes to `main`.
2. Monitor the workflow as it promotes builds through each environment.
3. Approve the production deployment when prompted.

### Rollback
1. Revert the problematic commit: `git revert <sha>`.
2. Push the revert to `main` to trigger the workflow again.
3. The CD pipeline redeploys to all environments, restoring the previous version.
4. To halt a pending production deployment, decline the approval request.
