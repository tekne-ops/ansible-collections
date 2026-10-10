# Hermes

Ensures boto3 is available, then creates or updates the EC2 instance named `tekne-devops-hermes` from the role defaults (AMI, instance type, subnet, and security groups). AWS credentials are read from the controller environment. The SSH port moves from 22 to `45100` after boot.

This role talks to AWS. It is not part of the normal THEMIS service tag list. Apply it with `--tags hermes`.

## Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `hermes_instance_name` | `tekne-devops-hermes` | EC2 Name tag |
| `hermes_instance_type` | `t3a.micro` | Instance type |
| `hermes_aws_region` | `AWS_DEFAULT_REGION` or `us-east-1` | Region |
| `hermes_ssh_port` | `45100` | SSH port after first boot |
| `hermes_management_user` | `devops` | Account created on the instance |

## Tags

`hermes`, `ec2`

## Requirements

`amazon.aws` and AWS credentials in the controller environment.
