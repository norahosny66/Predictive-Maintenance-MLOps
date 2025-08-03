terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }
}

provider "github" {
  owner = "norahosny66"
  token = "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" # or `GITHUB_TOKEN`
}