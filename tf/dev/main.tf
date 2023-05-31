locals {
  project_name             = "koinobori"
  env                      = "dev"
  api_function_name        = "${local.project_name}-${local.env}-api"
  migrations_function_name = "${local.project_name}-${local.env}-migrations"
  migrations_table_name    = "${local.project_name}-${local.env}-migrations"
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

resource "aws_iam_role_policy_attachment" "lambda_basic_execution_role" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.iam_for_lambda.id
}

data "aws_iam_policy_document" "policy" {
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:Batch*",
      "dynamodb:Describe*",
      "dynamodb:GetItem",
      "dynamodb:PartiQL*",
      "dynamodb:PutItem",
      "dynamodb:Query",
      "dynamodb:Scan",
      "dynamodb:UpdateItem",
    ]
    resources = [
      "arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:table/${local.migrations_table_name}",
    ]
  }
}

resource "aws_iam_policy" "policy" {
  name        = "${local.project_name}-${local.env}-dynamodb-access-policy"
  description = "Allow access to dynamodb resources"
  policy      = data.aws_iam_policy_document.policy.json
}

resource "aws_iam_role_policy_attachment" "dynamodb-access-attach" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.policy.arn
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

resource "aws_cloudwatch_log_group" "api_lambda" {
  name = "/aws/lambda/${local.project_name}/${local.env}/api"

  tags = {
    Project = local.project_name
    Env     = local.env
  }
}

resource "aws_lambda_function" "api_lambda" {
  function_name = local.api_function_name
  description   = "Dev API for Koinobori"
  role          = aws_iam_role.iam_for_lambda.arn

  package_type = "Image"
  image_uri    = "${aws_ecr_repository.koinobori.repository_url}:latest"

  timeout = 30

  image_config {
    command = ["koinobori.lambdas.api.main.lambda_handler"]
  }

  tags = {
    Project = local.project_name
    Env     = local.env
  }

  depends_on = [
    aws_cloudwatch_log_group.api_lambda,
  ]
}

resource "aws_lambda_function_url" "api" {
  function_name      = local.api_function_name
  authorization_type = "NONE"
}

resource "aws_dynamodb_table" "migrations" {
  name         = local.migrations_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "version_num"

  attribute {
    name = "version_num"
    type = "S"
  }
}

resource "aws_cloudwatch_log_group" "migrations_lambda" {
  name = "/aws/lambda/${local.project_name}/${local.env}/migrations"

  tags = {
    Project = local.project_name
    Env     = local.env
  }
}

resource "aws_lambda_function" "migrations_lambda" {
  function_name = local.migrations_function_name
  description   = "Migrations Lambda for Koinobori"
  role          = aws_iam_role.iam_for_lambda.arn

  package_type = "Image"
  image_uri    = "${aws_ecr_repository.koinobori.repository_url}:latest"

  timeout = 30

  environment {
    variables = {
      ALEMBIC_VERSION_TABLE = "${local.project_name}-${local.env}-migrations"
    }
  }

  image_config {
    command = ["koinobori.lambdas.migrations.main.lambda_handler"]
  }

  tags = {
    Project = local.project_name
    Env     = local.env
  }

  depends_on = [
    aws_cloudwatch_log_group.migrations_lambda,
  ]
}

