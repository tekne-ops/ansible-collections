# tekne.devops

Ansible collection for Tekne Arch Linux workstation and server automation.

## Overview

`tekne.devops` provides roles for provisioning Tekne hosts — from fresh Arch installs through desktop configuration, gaming, and server-side Docker services (HAProxy, Consul, Jenkins, package repo, media server). A separate `k8s` role prepares Debian nodes for Kubernetes.

**Version:** 1.3.0  
**Namespace:** `tekne`  
**Dependencies:** `community.general >= 10.0.0`, `ansible.posix >= 1.5.0`

## Roles

| Role | Tags (common) | Summary |
|------|---------------|---------|
| `user` | `user` | Users, SSH, sudoers, dotfiles |
| `network` | `network-host`, `wifi` | systemd-networkd, WiFi, br0 |
| `os` | `os`, `locale`, `mirrors` | Locale, NTP, reflector, repo clones |
| `pipewire` | `pipewire` | Audio stack and Bluetooth tuning |
| `gpu` | `gpu` | NVIDIA (YUGEN) or Intel/Mesa drivers |
| `xfce4` | `xfce4` | Desktop environment and display manager |
| `gaming` | `gaming` | Steam, Lutris, Wine, gamemode |
| `onedrive` | `onedrive` | OneDrive client and service |
| `bootstrap` | `bootstrap` | Post-install sync, symlinks, XFCE config |
| `nftables` | `nftables` | Per-host firewall |
| `docker` | `docker-host` | Docker engine and bridge network |
| `libvirt` | `libvirt` | QEMU/KVM virtualization |
| `haproxy` | `haproxy` | TLS reverse proxy for tekne.sv |
| `repotekne` | `repotekne` | Arch package repository container |
| `gerbera` | `gerbera` | UPnP/DLNA media server |
| `consul` | `consul` | HashiCorp Consul in Docker |
| `jenkins` | `jenkins` | Jenkins CI in Docker |
| `k8s` | `k8s`, `k8s-kubeadm`, `k8s-calico` | Debian Kubernetes node prep |
| `hostname` | — | Hostname fact caching |

See each role's `roles/<name>/README.md` for variables, tags, and examples.

## Install

```bash
ansible-galaxy collection install community.general ansible.posix
ansible-galaxy collection install /path/to/tekne/devops --force
```

## Example

```yaml
- hosts: localhost
  connection: local
  become: true
  roles:
    - role: tekne.devops.user
    - role: tekne.devops.os
      tags: [os]
```

Full playbooks: [`ansible-playbooks`](https://github.com/tekne-ops/ansible-playbooks).

## License

MIT
