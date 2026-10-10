# ansible-collections

Ansible collection repository for Tekne infrastructure automation. Contains the **`tekne.devops`** collection — a set of reusable roles for provisioning Arch Linux workstations and servers, plus Kubernetes node preparation on Debian.

Playbooks that consume this collection live in the companion [`ansible-playbooks`](../ansible-playbooks) repo.

## What This Repo Does

- Packages all Tekne automation logic as an Ansible collection (`tekne.devops`)
- Provides **22 roles** covering OS setup, desktop, gaming, networking, Docker services, AWS, and Kubernetes
- Depends on `amazon.aws`, `ansible.posix`, `community.docker`, and `community.general`
- Publishes collection metadata via `galaxy.yml` for `ansible-galaxy` installation

## Repository Structure

```
ansible-collections/
└── tekne/
    └── devops/                          # tekne.devops collection source (only copy in git)
        ├── galaxy.yml                   # Collection metadata (namespace, version, deps)
        ├── README.md                    # Collection-level docs
        ├── meta/                        # Runtime dependencies
        ├── plugins/                     # Custom Ansible plugins
        └── roles/                       # All automation roles (see below)
```

Install third-party collections via `ansible-galaxy collection install` (see `ansible-playbooks/requirements.yml`). Do not commit `tekne/ansible_collections/` or `ansible_collections/` — they are gitignored install artifacts.

## Collection: tekne.devops

| Field | Value |
|-------|-------|
| Namespace | `tekne` |
| Name | `devops` |
| Version | 1.3.0 |
| FQCN prefix | `tekne.devops.*` |
| Dependencies | `amazon.aws >= 7.0.0`, `ansible.posix >= 1.5.0`, `community.docker >= 4.0.0`, `community.general >= 10.0.0` |

## Roles

### Workstation & Desktop

| Role | Description |
|------|-------------|
| **user** | System users, passwords, SSH keys, sudoers, home directories, dotfiles |
| **network** | systemd-networkd, ASTER WiFi (iwd), THEMIS bridge (br0), connectivity wait |
| **os** | Locale, NTP, reflector mirrors, THEMIS services, tekne repo clones |
| **pipewire** | PipeWire audio with EQ, Bluetooth quality, LDAC, volume boost |
| **gpu** | NVIDIA TKG (YUGEN), hybrid Intel+NVIDIA (ASTER), or Intel/Mesa (THEMIS, KVM) |
| **xfce4** | XFCE4 desktop, LightDM, themes, bluetooth, portals |
| **kde** | KDE Plasma desktop and plasma login manager |
| **gaming** | Steam, Lutris, Wine, Proton, gamemode, gaming fonts |
| **onedrive** | OneDrive client (abraunegg fork) installation and systemd service |
| **bootstrap** | Post-install packages, OneDrive first sync, symlinks, XFCE desktop config |

### Server & Infrastructure

| Role | Description |
|------|-------------|
| **nftables** | Host-specific firewall rules (workstation vs THEMIS server config) |
| **docker** | Docker engine, compose, buildx; `dockers` bridge network (192.168.75.0/24) |
| **libvirt** | QEMU/KVM, dnsmasq, OVMF; adds local users to libvirt/kvm groups |
| **haproxy** | HAProxy in Docker, TLS termination for tekne.sv (consul, repo, jenkins) |
| **repotekne** | Arch package repository container (`fiercebrake/arch`) |
| **gerbera** | UPnP/DLNA media server container (host network, `/srv/media` mount) |
| **consul** | HashiCorp Consul server/agent in Docker with ACL and service registration |
| **jenkins** | Jenkins CI container on the `dockers` network |
| **n8n** | n8n workflow automation container on the `dockers` network; not included in `server.yml` |
| **hermes** | Amazon EC2 instance for Hermes and its SSH bootstrap |

### Kubernetes

| Role | Description |
|------|-------------|
| **k8s** | Debian k8s prerequisites: kubelet/kubeadm/kubectl, containerd, runc, CNI, kubeadm init, Calico |

### Utility

| Role | Description |
|------|-------------|
| **hostname** | Hostname fact caching for role dependencies |

Each role has its own README under `tekne/devops/roles/<role>/README.md` with variables, tags, and usage details.

## Installation

### From local source (development)

When checked out alongside `ansible-playbooks`, the collections repository exposes the standard search path:

```text
ansible_collections/tekne -> ../tekne
```

`ansible-playbooks/ansible.cfg` sets `collections_path = ../ansible-collections`. Ansible then finds `tekne.devops` without a Galaxy install. A path that stops at `tekne/devops` does not.

```bash
ansible-galaxy collection list tekne.devops
```

Or install the collection directly:

```bash
ansible-galaxy collection install tekne/devops --force
```

### From Git (CI / remote)

```bash
ansible-galaxy collection install \
  git+https://github.com/tekne-ops/ansible-collections.git#/tekne/devops \
  --force
```

## Usage in Playbooks

Reference roles by FQCN:

```yaml
- hosts: localhost
  connection: local
  become: true
  roles:
    - role: tekne.devops.user
      tags: [user]
    - role: tekne.devops.os
      tags: [os]
```

See [`ansible-playbooks`](../ansible-playbooks) for complete playbooks, inventories, and vault configuration.

## Host profiles

Roles do not embed Tekne hostnames. `ansible-playbooks` loads `inventories/host_profiles/<HOSTNAME>.yml` after it reads `/etc/hostname`. That file sets Wi-Fi, bridge, laptop, GPU, LightDM, firewall, gaming, and Docker membership. Running a role without that profile leaves those features off.

| Host | Profile behavior |
|------|------------------|
| **ASTER** | iwd Wi-Fi, laptop services, hybrid Intel+NVIDIA, LightDM, ACPI keys |
| **YUGEN** | Ethernet, discrete NVIDIA, LightDM, gaming Xorg drop-in, Docker daemon tuning |
| **THEMIS** | br0 bridge, server services, server firewall, Docker daemon tuning |
| **KVM** | Ethernet and the Intel/Mesa GPU path |

## Requirements

- Target: Arch Linux (most roles) or Debian 13 (k8s role)
- Ansible Core 2.19+
- `amazon.aws`, `ansible.posix`, `community.docker`, and `community.general` collections

```bash
pacman -S ansible-core ansible
ansible-galaxy collection install amazon.aws ansible.posix community.docker community.general
```

## Development

Role source of truth: `tekne/devops/roles/<role>/`

Standard Ansible role layout:

```
roles/<role>/
├── defaults/main.yml    # Default variables
├── vars/main.yml        # Role-internal variables
├── tasks/main.yml       # Task list
├── handlers/main.yml    # Handlers
├── files/               # Static files deployed to targets
├── templates/           # Jinja2 templates
├── meta/main.yml        # Role metadata and dependencies
├── meta/argument_specs.yml
└── README.md            # Role documentation
```

After editing roles, playbooks pick up the working tree through `ansible_collections/tekne`. Reinstall only when a checkout does not have that symlink.

Collection quality checks live in `.github/workflows/collection.yml`. They install the ranges in `tekne/devops/requirements.yml`, then run yamllint, ansible-lint, `ansible-galaxy collection build`, role syntax checks, two-pass idempotence for the hostname role and the resolved DNS template, and `ansible-test sanity`.

## Related Repos

| Repo | Purpose |
|------|---------|
| [`ansible-playbooks`](../ansible-playbooks) | Playbooks, inventories, vault, and installation scripts |

## License

MIT

## Author

dvaliente
