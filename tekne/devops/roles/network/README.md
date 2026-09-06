# Network Role

Configures systemd-networkd, systemd-resolved DNS policy, THEMIS bridge (br0) and SSH drop-in, ASTER WiFi via iwd, and waits for outbound connectivity before later roles run.

## What It Does

1. **Workstation (ASTER, YUGEN)** – Deploys `80-wifi-station.network` and `89-ethernet.network`; enables systemd-networkd, resolved, acpid; ASTER also enables iwd/bluetooth/tlp/thermald and connects to WiFi.
2. **THEMIS** – Deploys `25-br0` netdev/network units and `sshd_config.d/ssh.conf`.
3. **DNS** – `95-dns.conf` (search/cache) plus **`99-dot-override.conf`** (strict DoT on 853, Quad9 then Google). Link drop-ins `*.network.d/99-dns-override.conf` set `DNSDefaultRoute=no` so the router is never the default resolver.
4. **Connectivity** – Flushes handlers and pings `archlinux.org` until reachable.

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
| `network_resolved_manage` | Deploy the resolved drop-in (default `true`) |
| `network_dns_servers` | DoT resolvers (`ip#name`); default Quad9 then Google. Not Cloudflare (Tigo blocks 1.1.1.1:853). |
| `network_dns_over_tls` | `yes` (strict, port 853). Set by `99-dot-override.conf`. |
| `network_dhcp_use_dns` | Always `no` so DHCP/router DNS cannot inject port 53. |
| `network_dhcp_use_domains` | `UseDomains=` in the `.network` units (default `no`) |

## Tags

| Tag | Description |
|-----|-------------|
| `network-host` | All host network tasks (systemd-networkd, DNS, WiFi, br0) |
| `dns` | resolved drop-in only |
| `wifi` | ASTER WiFi connect steps |

## Example

```yaml
- role: tekne.devops.network
  tags: [network-host]
```

## DNS

The role writes `/etc/systemd/resolved.conf.d/95-dns.conf` and, on a booted system, forces
`/etc/resolv.conf` → `/run/systemd/resolve/stub-resolv.conf`. That symlink task is skipped
during `arch-chroot` (`install_chroot_phase`): `arch-chroot` bind-mounts the live ISO's
`resolv.conf` over the same path, so replacing it with a symlink fails with EBUSY. The
installer already creates the persistent stub link in `task_configure_base`.

ASTER Wi‑Fi uses `DNSDefaultRoute=yes` so DHCP DNS (the LAN gateway at home) is used when
Ethernet is down. Ethernet still has a better `RouteMetric`, so a cable wins for traffic
when both links are up.

Defaults keep DHCP DNS and add Quad9 over TLS as fallback:

```yaml
network_dns_over_tls: opportunistic
network_dns_fallback: ['9.9.9.9#dns.quad9.net', '149.112.112.112#dns.quad9.net']
```

To resolve through the LAN gateway instead, pin it — `network_dhcp_use_dns` then flips to `no`
automatically so DHCP cannot re-add its own servers:

```yaml
network_dns_servers: ['192.168.135.1']
```

Use `network_dns_over_tls: yes` (strict) only when **every** pinned server serves DoT on port 853.
A gateway that does not will make all lookups fail over to `FallbackDNS`, which looks like working
DNS while local names silently break.

## ASTER WiFi troubleshooting

If **Resolve WiFi interface name** times out:

1. Confirm the driver is loaded: `lsmod | grep mt7925e` and `ip -o link show type wlan`.
2. Check rfkill: `rfkill list` — unblock with `rfkill unblock wifi` if soft-blocked.
3. Pin the interface instead of auto-detect: `-e os_wifi_interface=wlp0s20f3` (or in vault).
4. During arch-chroot install, WiFi connect is intentionally skipped (`network_connect_wifi=false`); run `workstation.sh` after first boot.
