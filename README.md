# ansible-collections

Ansible collection repository for Tekne infrastructure automation. Contains the **`tekne.devops`** collection — a set of reusable roles for provisioning Arch Linux workstations and servers, plus Kubernetes node preparation on Debian.

Playbooks that consume this collection live in the companion [`ansible-playbooks`](../ansible-playbooks) repo.

## What This Repo Does

- Packages all Tekne automation logic as an Ansible collection (`tekne.devops`)
- Provides **19 roles** covering OS setup, desktop, gaming, networking, Docker services, and Kubernetes
- Vendors third-party collections (`community.general`, `ansible.posix`) under `tekne/ansible_collections/`
- Publishes collection metadata via `galaxy.yml` for `ansible-galaxy` installation

## Repository Structure

```
ansible-collections/
└── tekne/
    ├── devops/                          # tekne.devops collection source
    │   ├── galaxy.yml                   # Collection metadata (namespace, version, deps)
    │   ├── README.md                    # Collection-level docs
    │   ├── meta/                        # Runtime dependencies
    │   ├── plugins/                     # Custom Ansible plugins
    │   └── roles/                       # All automation roles (see below)
    └── ansible_collections/             # Vendored Galaxy collections
        ├── tekne/devops/                # Installed copy of this collection
        ├── community/general/
        └── ansible/posix/
```

The canonical role source is `tekne/devops/`. The `tekne/ansible_collections/` tree is populated by `ansible-galaxy collection install` and used at runtime via `collections_path`.

## Collection: tekne.devops

| Field | Value |
|-------|-------|
| Namespace | `tekne` |
| Name | `devops` |
| Version | 1.3.0 |
| FQCN prefix | `tekne.devops.*` |
| Dependencies | `community.general >= 10.0.0`, `ansible.posix >= 1.5.0` |

## Roles

### Workstation & Desktop

| Role | Description |
|------|-------------|
| **user** | System users, passwords, SSH keys, sudoers, home directories, dotfiles |
| **network** | systemd-networkd, ASTER WiFi (iwd), THEMIS bridge (br0), connectivity wait |
| **os** | Locale, NTP, reflector mirrors, THEMIS services, tekne repo clones |
| **pipewire** | PipeWire audio with EQ, Bluetooth quality, LDAC, volume boost |
| **gpu** | NVIDIA TKG drivers (YUGEN) or Intel/Mesa (all other hosts) |
| **xfce4** | XFCE4 desktop, LightDM, picom, themes, bluetooth portals |
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

When checked out alongside `ansible-playbooks`:

```bash
# ansible-playbooks/ansible.cfg sets:
# collections_path = ../ansible-collections/tekne

ansible-galaxy collection install -r ../ansible-playbooks/requirements.yml
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

## Host-Specific Behavior

Many roles branch on hostname (read from `/etc/hostname` or Ansible facts):

| Host | Notable role behavior |
|------|----------------------|
| **ASTER** | WiFi via iwd, Intel GPU, LightDM, laptop nftables |
| **YUGEN** | NVIDIA TKG GPU, triple-monitor XFCE wallpaper config |
| **THEMIS** | br0 bridge, server nftables, cronie/irqbalance/sshd, Docker services |
| **KVM** | VM network config, standard workstation stack |

## Requirements

- Target: Arch Linux (most roles) or Debian 13 (k8s role)
- Ansible Core 2.14+
- `community.general` and `ansible.posix` collections

```bash
pacman -S ansible-core ansible
ansible-galaxy collection install community.general ansible.posix
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
└── README.md            # Role documentation
```

After editing roles, reinstall or ensure `collections_path` points at `tekne/` so playbooks pick up changes without rebuilding.

## Related Repos

| Repo | Purpose |
|------|---------|
| [`ansible-playbooks`](../ansible-playbooks) | Playbooks, inventories, vault, and installation scripts |

## License

MIT

## Author

dvaliente
