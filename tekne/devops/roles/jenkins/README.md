# Jenkins

Starts the pinned Jenkins LTS image on the `dockers` network at `192.168.75.12`. The image comparison is strict, so a tag change is a container change.

Run this after the Docker role has created the `dockers` network. The server playbook exposes it with the `jenkins` tag.

## Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `jenkins_docker_image` | `jenkins/jenkins:2.516.3-lts-jdk21` | Image tag |
| `jenkins_docker_network` | `dockers` | Docker network |
| `jenkins_docker_ip` | `192.168.75.12` | Address on that network |

## Tags

`jenkins`, `docker`
