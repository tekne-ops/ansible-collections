# Network Role

Configures systemd-networkd, systemd-resolved DNS policy, THEMIS bridge (br0) and SSH drop-in, ASTER WiFi via iwd, and waits for outbound connectivity before later roles run.

## What It Does

1. **Workstation (ASTER, YUGEN)** – Deploys `80-wifi-station.network` and `89-ethernet.network`; enables systemd-networkd, resolved, acpid; ASTER also enables iwd/bluetooth/tlp/thermald and connects to WiFi.
2. **THEMIS** – Deploys `25-br0` netdev/network units and `sshd_config.d/ssh.conf`.
3. **DNS** – One resolved drop-in, `95-dns.conf`. Strict DoT (`DNSOverTLS=yes`) on every host. **ASTER** uses DHCP nameservers (`UseDNS=yes`, `DNSDefaultRoute=yes`) and pins nothing. Other hosts pin Quad9 then Google and set `DNSDefaultRoute=no` so the router is not the resolver. `FallbackDNS=` clears systemd's compiled-in plaintext list.
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
| `network_dns_from_dhcp` | `true` on ASTER: use router-advertised DNS with strict DoT. `false` elsewhere. |
| `network_dns_servers` | Pinned DoT resolvers (`ip#name`) when not using DHCP. Default Quad9 then Google (not Cloudflare; Tigo blocks 1.1.1.1:853). Ignored on ASTER. |
| `network_dns_fallback` | Extra DoT fallbacks. Empty (default) writes `FallbackDNS=` and disables compiled-in 1.1.1.1/8.8.8.8. |
| `network_dns_over_tls` | `yes` (strict, port 853) in resolved and `.network` units. |
| `network_dhcp_use_dns` | `yes` on ASTER, `no` on pinned-resolver hosts. |
| `network_dns_default_route` | `yes` on ASTER so DHCP DNS is used; `no` on pinned-resolver hosts. |
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

ASTER takes nameservers from DHCP and requires DoT to those IPs. Wi‑Fi and Ethernet both
set `DNSDefaultRoute=yes`; Ethernet still has a better `RouteMetric` for traffic. There is
no Quad9/Google pin and no compiled-in fallback, so if the advertised servers do not speak
DoT on 853, resolution fails instead of leaking to plaintext DNS.

YUGEN, THEMIS, and KVM keep pinned Quad9/Google DoT. DHCP DNS is ignored on those hosts.

Do not set `network_dns_over_tls` to opportunistic on ASTER if the goal is to never use port 53.

## ASTER WiFi troubleshooting

If **Resolve WiFi interface name** times out:

1. Confirm the driver is loaded: `lsmod | grep mt7925e` and `ip -o link show type wlan`.
2. Check rfkill: `rfkill list` — unblock with `rfkill unblock wifi` if soft-blocked.
3. Pin the interface instead of auto-detect: `-e os_wifi_interface=wlp0s20f3` (or in vault).
4. During arch-chroot install, WiFi connect is intentionally skipped (`network_connect_wifi=false`); run `workstation.sh` after first boot.
