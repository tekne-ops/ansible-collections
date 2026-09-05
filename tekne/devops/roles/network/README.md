# Network Role

Configures systemd-networkd, systemd-resolved DNS policy, THEMIS bridge (br0) and SSH drop-in, ASTER WiFi via iwd, and waits for outbound connectivity before later roles run.

## What It Does

1. **Workstation (ASTER, YUGEN)** – Deploys `80-wifi-station.network` and `89-ethernet.network`; enables systemd-networkd, resolved, acpid; ASTER also enables iwd/bluetooth/tlp/thermald and connects to WiFi.
2. **THEMIS** – Deploys `25-br0` netdev/network units and `sshd_config.d/ssh.conf`.
3. **DNS** – Deploys `/etc/systemd/resolved.conf.d/95-dns.conf`, the stub `/etc/resolv.conf` symlink, and `systemd-resolvconf`.
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
| `network_dns_servers` | Pinned resolvers, e.g. `['192.168.135.1']`; empty keeps DHCP-advertised DNS |
| `network_dns_fallback` | Fallback resolvers (default Quad9 with `#dns.quad9.net` for TLS validation) |
| `network_dns_search_domains` | `Domains=` in resolved (default `tekne.sv`) |
| `network_dns_over_tls` | `opportunistic` (default), `yes` for strict DoT, or `no` |
| `network_dnssec` / `network_dns_cache` | `DNSSEC=` (default `no`) and `Cache=` (default `yes`) |
| `network_dhcp_use_dns` | `UseDNS=` in the `.network` units; auto-set to `no` when resolvers are pinned |
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

The role writes `/etc/systemd/resolved.conf.d/95-dns.conf` and forces
`/etc/resolv.conf` → `/run/systemd/resolve/stub-resolv.conf`. The `.network` units carry no
`DNS=` of their own.

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
