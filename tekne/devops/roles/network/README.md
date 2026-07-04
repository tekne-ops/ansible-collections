# Network Role

Configures systemd-networkd, THEMIS bridge (br0) and SSH drop-in, ASTER WiFi via iwd, and waits for outbound connectivity before later roles run.

## What It Does

1. **Workstation (ASTER, YUGEN)** – Deploys `80-wifi-station.network` and `89-ethernet.network`; enables systemd-networkd, resolved, acpid; ASTER also enables iwd/bluetooth/tlp/thermald and connects to WiFi.
2. **THEMIS** – Deploys `25-br0` netdev/network units and `sshd_config.d/ssh.conf`.
3. **Connectivity** – Flushes handlers and pings `archlinux.org` until reachable.

Run after `tekne.devops.os` locale setup and before roles that need network (mirrors, git clones).

## Variables

| Variable | Description |
|----------|-------------|
| `network_hostname` | Uppercase hostname for conditionals |
| `network_hostname_raw` | Case-sensitive hostname for `Host=` in network units |
| `network_config_hosts` | Hosts that receive WiFi/Ethernet units (vars: ASTER, YUGEN, KVM) |
| `network_wifi_ssid` | ASTER WiFi SSID (default `esher`) |
| `network_wifi_interface` | ASTER interface; empty = auto-detect first wireless netdev (`/sys/class/net/*/wireless`) |
| `network_wifi_passphrase` | ASTER passphrase; defaults from vault `os_wifi_passphrase` |
| `network_wifi_driver_module` | Kernel module to load before auto-detect (default `mt7925e`) |
| `network_wifi_detect_retries` | Auto-detect retry count (default `30`, ~60s with default delay) |
| `network_wifi_detect_delay` | Seconds between auto-detect retries (default `2`) |
| `network_connect_wifi` | Run live `iwctl` connect on ASTER (disable during arch-chroot install) |

## Tags

| Tag | Description |
|-----|-------------|
| `network-host` | All host network tasks (systemd-networkd, WiFi, br0) |
| `wifi` | ASTER WiFi connect steps |

## Example

```yaml
- role: tekne.devops.network
  tags: [network-host]
```

## ASTER WiFi troubleshooting

If **Resolve WiFi interface name** times out:

1. Confirm the driver is loaded: `lsmod | grep mt7925e` and `ip -o link show type wlan`.
2. Check rfkill: `rfkill list` — unblock with `rfkill unblock wifi` if soft-blocked.
3. Pin the interface instead of auto-detect: `-e os_wifi_interface=wlp0s20f3` (or in vault).
4. During arch-chroot install, WiFi connect is intentionally skipped (`network_connect_wifi=false`); run `workstation.sh` after first boot.
