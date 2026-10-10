# Docker

Installs Docker Engine, Docker Compose, and Docker Buildx on Arch. Hosts listed in `docker_daemon_json_hosts` receive `/etc/docker/daemon.json`. Every host that has the packages gets the `dockers` bridge on `192.168.75.0/24`.

Container DNS uses the LAN gateway and Quad9. Containers cannot use the host stub resolver at `127.0.0.53`.

Membership lists are empty unless a play sets them. Tekne playbooks load `inventories/host_profiles/<HOSTNAME>.yml`.

## Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `docker_daemon_json_hosts` | `[]` | Hostnames that receive `daemon.json` |
| `docker_daemon_json_dest` | `/etc/docker/daemon.json` | Daemon configuration path |
| `docker_network_name` | `dockers` | Bridge network name |
| `docker_network_subnet` | `192.168.75.0/24` | Bridge subnet |
| `docker_dns_servers` | `192.168.135.1`, `9.9.9.9` | Resolver addresses inside containers |

## Tags

`docker-host`, `config`

## Requirements

Arch Linux, `community.general`, and `community.docker`.
