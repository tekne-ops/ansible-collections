# Consul

Creates `/srv/docker/consul` and starts the pinned `hashicorp/consul` image on the `dockers` network at `192.168.75.11`. The container uses the official image user, a TLS domain of `consul.tekne.sv`, and stores the bootstrap and admin tokens under the config directory.

Run this after the Docker role has created the `dockers` network.

## Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `consul_docker_image` | `hashicorp/consul:1.21.5` | Image tag |
| `consul_docker_network` | `dockers` | Docker network |
| `consul_docker_ip` | `192.168.75.11` | Address on that network |
| `consul_directory` | `/srv/docker/consul/config` | Config and token directory |
| `consul_data_directory` | `/srv/docker/consul/data` | Data directory |
| `consul_tls_domain` | `consul.tekne.sv` | TLS domain |

## Tags

`consul`, `config`, `docker`
