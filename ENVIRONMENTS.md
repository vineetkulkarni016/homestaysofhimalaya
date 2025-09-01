# Environment Provisioning

This project uses a central configuration store backed by AWS SSM Parameter Store.  
Configuration is organized by environment and service. Each environment has a YAML file under `config/` 
that maps services to their parameter paths in SSM.

## Environments

- **dev-integration** – Used for local integration testing across services.
- **dev-staging** – Mirrors production with staging data for final validation.
- **dev-production** – Production configuration.

## Provisioning Parameters

Parameters are stored in SSM using the following pattern:

```
/homestaysofhimalaya/<environment>/<service>/<parameter>
```

For example, the booking service database URL for the integration environment is stored at:

```
/homestaysofhimalaya/dev-integration/booking/database_url
```

Parameters should be created with `--type SecureString` for sensitive values.

## Using Configuration

Service startup scripts read `APP_ENV` to determine which config file to load. The script then pulls the
appropriate parameter values from SSM before launching the service.

To start the booking service in the staging environment:

```bash
APP_ENV=dev-staging services/booking/start.sh
```

Ensure the IAM role or AWS credentials used by the service allow `ssm:GetParameter` access.
