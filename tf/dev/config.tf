terraform {
  backend "s3" {
    bucket  = "koinobori-dev-terraform"
    key     = "dev/terraform.tfstate"
    region  = "eu-central-1"
    encrypt = true

    dynamodb_table = "koinobori-dev-terraform"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.29.0"
    }
  }

  required_version = "1.6.6"

}

provider "aws" {
  region = "eu-central-1"
}
