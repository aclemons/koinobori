locals {
  project_name  = "koinobori"
  env           = "dev"
  function_name = "${local.project_name}-${local.env}-api"
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_ecr_repository" "koinobori" {
  name                 = "${local.project_name}/${local.env}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project = local.project_name
    Env     = local.env
  }
}

resource "aws_cloudwatch_log_group" "lambda" {
  name = "/aws/lambda/${local.project_name}/${local.env}"

  tags = {
    Project = local.project_name
    Env     = local.env
  }
}
resource "aws_lambda_function" "api_lambda" {
  function_name = local.function_name
  description   = "Dev API for Koinobori"
  role          = aws_iam_role.iam_for_lambda.arn

  package_type = "Image"
  image_uri    = "${aws_ecr_repository.koinobori.repository_url}:latest"

  image_config {
    command = ["koinobori.lambdas.api.main.lambda_handler"]
  }

  tags = {
    Project = local.project_name
    Env     = local.env
  }
}

resource "aws_lambda_function_url" "api" {
  function_name      = local.function_name
  authorization_type = "NONE"
}
