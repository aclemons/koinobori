locals {
  project_name = "koinobori"
  env          = "dev"
}

resource "aws_ecr_repository" "koinobiri" {
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
