# Development Guide

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Terraform](https://developer.hashicorp.com/terraform/downloads)
- Python 3.11+
- AWS credentials configured for access to CloudWatch, RDS and S3

## Getting Started

1. Clone the repository and change into the directory.
2. Run `scripts/setup.sh` to create a virtual environment, install dependencies and start the microservices with Docker Compose.
3. Access the services:
   - Booking service: `http://localhost:8000`
   - User service: `http://localhost:8001`

The payments service has been removed from this project.

Logs are emitted in JSON format and, when AWS credentials are available, forwarded to CloudWatch.

## Infrastructure

Terraform configuration in `infra/` provisions:

- ECS cluster for running containers
- RDS PostgreSQL instance
- S3 bucket for application assets
- CloudWatch log group for service logs

To deploy infrastructure:

```bash
cd infra
terraform init
terraform apply
```

This will create resources in the AWS account configured in your environment.
