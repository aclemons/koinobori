terraform {
  backend "s3" {
    bucket  = "koinobori-dev-terraform"
    key     = "state/terraform.tfstate"
    region  = "eu-central-1"
    encrypt = true

    dynamodb_table           = "koinobori-dev-terraform"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.6.2"
    }
  }

  required_version = "1.5.2"

}

provider "aws" {
  region = "eu-central-1"
}
