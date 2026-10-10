# nftables

Installs nftables and writes `/etc/nftables.conf` from one of three policies:

- `server.conf` when the hostname is in `nftables_server_hosts`
- `workstation-docker.conf` when the hostname is in `nftables_docker_hosts` and is not a server host
- `workstation.conf` otherwise

Server and Docker policies allow the ICMPv6 types SLAAC needs and DHCPv6 replies. The workstation policy allows DHCPv6 replies. During the Arch install chroot the service is enabled and left stopped.

Membership lists are empty unless a play sets them. Tekne playbooks load `inventories/host_profiles/<HOSTNAME>.yml`.

## Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `nftables_server_hosts` | `[]` | Hostnames that receive the server policy |
| `nftables_docker_hosts` | `[]` | Hostnames that receive the Docker workstation policy |
| `nftables_install_chroot_phase` | `install_chroot_phase` | Enable the unit without starting it |

## Tags

`nftables`, `packages`, `config`
