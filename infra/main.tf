terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_ecs_cluster" "homestays" {
  name = var.cluster_name
}

resource "aws_db_instance" "homestays" {
  identifier         = var.db_identifier
  allocated_storage  = 20
  engine             = "postgres"
  instance_class     = "db.t3.micro"
  username           = var.db_username
  password           = var.db_password
  skip_final_snapshot = true
}

resource "aws_s3_bucket" "homestays" {
  bucket = var.bucket_name
}

resource "aws_cloudwatch_log_group" "services" {
  name = "/homestays/services"
  retention_in_days = 7
}
