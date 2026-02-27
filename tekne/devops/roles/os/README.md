# OS Role

Configures Arch Linux system settings: reflector (mirrors), locale, systemd-networkd, WiFi (ASTER), NTP, pacman mirrorlist, and system scripts.

## What It Does

1. **Reflector** – Ensures `/etc/xdg/reflector` exists and copies `reflector.conf`.
2. **Locale** – Sets `LANG` in `/etc/locale.conf`, uncomments locale in `/etc/locale.gen`, runs `locale-gen` (via handler).
3. **Network** – Deploys systemd-networkd unit files (WiFi and Ethernet) when hostname is in `os_network_hosts`; enables/restarts systemd-networkd, systemd-resolved, bluetooth, acpid (ASTER/YUGEN), and iwd (ASTER only). Optionally connects ASTER to WiFi via `iwctl` using `os_wifi_ssid` and `os_wifi_passphrase`.
4. **NTP** – Enables NTP with `timedatectl set-ntp true`.
5. **Mirrors** – Runs reflector to update `/etc/pacman.d/mirrorlist` (country, count, protocol, age).
6. **Scripts** – Copies `game`, `update`, and `work` to `/usr/local/bin` (mode 0755).

Hostname is taken from `hostname` (playbook) or `cached_hostname` / `ansible_hostname`. Vars can override `os_hostname`; `vars/main.yml` restricts `os_network_hosts` to ASTER and YUGEN and sets WiFi SSID.

## Requirements

- Arch Linux
- `reflector` package installed
- For ASTER WiFi: `os_wifi_passphrase` set (e.g. in vault) and `iwd` available

## Role Variables

### defaults/main.yml

| Variable | Default | Description |
|----------|---------|-------------|
| `os_hostname` | `{{ hostname }}` | Hostname (from playbook/cached fact) |
| `os_locale` | `en_US.UTF-8` | System locale (LANG) |
| `os_mirror_country` | `United States` | Reflector country |
| `os_mirror_count` | `100` | Number of mirrors |
| `os_mirror_protocols` | `https,ftp` | Allowed protocols |
| `os_mirror_age` | `168` | Max mirror age (hours) |
| `os_network_hosts` | ASTER, THEMIS, HEPHAESTUS, YUGEN | Hosts that get network config files |
| `os_wifi_ssid` | `esher` | WiFi SSID (ASTER) |
| `os_wifi_interface` | `""` | WiFi interface (empty = auto-detect first `wl*`) |
| `os_wifi_passphrase` | **(vault)** | WiFi passphrase (required for ASTER) |

### vars/main.yml

- Overrides `os_network_hosts` to `ASTER`, `YUGEN` only.
- Sets `os_hostname` / `os_hostname_raw` from `cached_hostname` / `cached_hostname_raw` (case-sensitive raw for network units).
- Sets `os_wifi_ssid: esher`.

## Handlers

| Handler | Description |
|---------|-------------|
| `Generate locales` | Runs `locale-gen` |
| `Restart systemd-networkd` | Restarts systemd-networkd after template changes |
| `restart bluetooth` | Restarts bluetooth.service (when using systemd) |

## Files and Templates

| Source | Destination | When |
|--------|-------------|------|
| `files/reflector.conf` | `/etc/xdg/reflector/reflector.conf` | Always |
| `templates/80-wifi-station.network.j2` | `/etc/systemd/network/80-wifi-station.network` | `os_hostname in os_network_hosts` |
| `templates/89-ethernet.network.j2` | `/etc/systemd/network/89-ethernet.network` | `os_hostname in os_network_hosts` |
| `files/game` | `/usr/local/bin/game` | Always |
| `files/update` | `/usr/local/bin/update` | Always |
| `files/work` | `/usr/local/bin/work` | Always |

Network templates use `os_hostname_raw` in `Host=` for systemd-networkd matching.

## Host-Specific Behavior

| Hostname | Network config | WiFi (iwd + connect) | Bluetooth/acpid |
|----------|----------------|------------------------|------------------|
| ASTER | Yes | Yes (requires os_wifi_passphrase) | Enabled |
| YUGEN | Yes | No | Enabled |
| Others (if in os_network_hosts) | Yes | No | No |

## Example Playbook

```yaml
- hosts: localhost
  roles:
    - role: ansible-role-os
      vars:
        os_locale: de_DE.UTF-8
        os_mirror_country: Germany
```

## Tags

| Tag | Description |
|-----|-------------|
| `os` | All OS tasks |
| `system_config` | Reflector directory and config |
| `locale` | Locale settings and locale-gen |
| `network` | Network templates, services, WiFi connect |
| `wifi` | ASTER WiFi (interface, connect) |
| `ntp` | NTP enable |
| `mirrors` | Pacman mirrorlist via reflector |
| `scripts` | game, update, work in /usr/local/bin |

## License

MIT

## Author

dvaliente
