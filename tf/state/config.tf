terraform {
  backend "s3" {
    bucket  = "koinobori-dev-terraform"
    key     = "state/terraform.tfstate"
    region  = "eu-central-1"
    encrypt = true

    use_lockfile = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.67.0"
    }
  }

  required_version = "1.13.1"

}

provider "aws" {
  region = "eu-central-1"
}
