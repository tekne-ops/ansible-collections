# Network Role

Configures systemd-networkd, systemd-resolved DNS policy, THEMIS bridge (br0) and SSH drop-in, ASTER WiFi via iwd, and waits for outbound connectivity before later roles run.

## What It Does

1. **Workstation (ASTER, YUGEN)** – Deploys `80-wifi-station.network` and `89-ethernet.network`; enables systemd-networkd, resolved, acpid; ASTER installs and enables iwd/bluetooth/tlp/thermald/bolt and connects to WiFi.
2. **THEMIS** – Deploys `25-br0` netdev/network units and `sshd_config.d/ssh.conf`.
3. **DNS** – One resolved drop-in, `95-dns.conf`. Strict DoT (`DNSOverTLS=yes`) on every host, including ASTER. Resolvers are pinned as `IP#hostname` (Quad9, then Google) so the certificate matches a DNS name. DHCP and IPv6 router-advertisement DNS are ignored (`UseDNS=no`, `DNSDefaultRoute=no`). `FallbackDNS=` clears systemd's compiled-in plaintext list. `LLMNR=no`. `StaleRetentionSec=30min` keeps expired cache entries usable during a short outage. `Domains` includes the search suffix `tekne.sv` and the default route `~.`.
4. **IPv6** – Managed links accept router advertisements (SLAAC) and still use DHCPv4. Wi-Fi and Ethernet use IPv6 privacy extensions. THEMIS `br0` keeps a stable address. Bridge member ports stay IPv6-off. THEMIS and YUGEN firewalls allow the ICMPv6 types SLAAC needs, and every firewall allows DHCPv6 replies.
5. **Online** – `systemd-networkd-wait-online` uses `--any --ipv4 --dns --timeout=30` (requires systemd 258 or newer). `.network` changes reload networkd with `networkctl reload` instead of restarting it. The final check waits until that same command succeeds and `resolvectl query archlinux.org` resolves. It does not use ICMP.

Run after `tekne.devops.os` locale setup and before roles that need network (mirrors, git clones).

## Variables

| Variable | Description |
|----------|-------------|
| `network_hostname` | Uppercase hostname for conditionals |
| `network_hostname_raw` | Case-sensitive hostname, shown in the role debug output. Network units are selected by which host the role runs on; they do not match `Host=` |
| `network_config_hosts` | Hosts that receive WiFi/Ethernet units (vars: ASTER, YUGEN, KVM) |
| `network_wifi_ssid` | ASTER WiFi SSID (default `esher`) |
| `network_wifi_interface` | ASTER interface; empty = auto-detect first wireless netdev (`/sys/class/net/*/wireless`) |
| `network_wifi_passphrase` | ASTER passphrase; defaults from vault `os_wifi_passphrase` |
| `network_wifi_driver_module` | Kernel module to load before auto-detect (default `mt7925e`) |
| `network_wifi_detect_retries` | Auto-detect retry count (default `30`, ~60s with default delay) |
| `network_wifi_detect_delay` | Seconds between auto-detect retries (default `2`) |
| `network_connect_wifi` | Run live `iwctl` connect on ASTER (disable during arch-chroot install) |
| `network_laptop_service_packages` | Packages providing the ASTER services managed by this role (`bluez`, `iwd`, `thermald`, `tlp`, `bolt`) |
| `network_resolved_manage` | Deploy the resolved drop-in (default `true`) |
| `network_dns_from_dhcp` | `false` on every host. Set `true` only to accept DHCP DNS under strict DoT; those servers are bare IPs and usually fail certificate checks. |
| `network_dns_servers` | Pinned DoT resolvers (`ip#name`). Default Quad9 then Google (not Cloudflare; Tigo blocks 1.1.1.1:853). |
| `network_dns_fallback` | Extra DoT fallbacks. Empty (default) writes `FallbackDNS=` and disables compiled-in 1.1.1.1/8.8.8.8. |
| `network_dns_search_domains` | Search suffixes. Default `tekne.sv`. Single-label names are queried as `name.tekne.sv` on the pinned resolvers. |
| `network_dns_route_domains` | Route-only domains. Default `~.`, so global resolvers are the default DNS route. A longer per-link suffix still wins. |
| `network_dns_over_tls` | `yes` (strict, port 853) in resolved and `.network` units. |
| `network_dns_llmnr` | `no`. Link-local multicast name resolution stays off. |
| `network_dns_stale_retention_sec` | How long expired cache records may still be served. Default `30min`. |
| `network_dhcp_use_dns` | `no` unless `network_dns_from_dhcp` is true. Also applied to IPv6 RA and DHCPv6. |
| `network_dns_default_route` | `no` unless `network_dns_from_dhcp` is true. |
| `network_dhcp_use_domains` | `UseDomains=` in the `.network` units (default `no`) |
| `network_ipv6_accept_ra` | Accept IPv6 router advertisements on Wi-Fi, Ethernet, and `br0` (default `true`). |
| `network_ipv6_privacy_extensions` | `yes` on Wi-Fi and Ethernet. `br0` stays stable. |

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

Every host pins Quad9 and Google and requires DoT. DHCP and router-advertisement DNS
are ignored, including on ASTER. A router that only offers an IP address cannot pass
strict certificate checks, so using it as a DoT resolver fails closed on travel and
captive networks. Ethernet still has the better `RouteMetric` for traffic.

`Domains=tekne.sv ~.` sends single-label lookups through the search suffix and sends
every other name to the pinned resolvers unless a link has a longer routing suffix.

Do not set `network_dns_over_tls` to opportunistic if the goal is to never use port 53.

IPv6 router advertisements are accepted beside DHCPv4. THEMIS `server.conf` and YUGEN
`workstation-docker.conf` allow neighbor discovery and router advertisements; without
those rules SLAAC cannot complete. Bridge ports (`25-br0-en.network`) still reject RA
so only `br0` is addressed.

`.network` and `.netdev` changes call `networkctl reload`. The wait-online drop-in only
reloads systemd. `--dns` needs systemd 258 or newer. It succeeds from the global
resolvers because links set `DNSDefaultRoute=no`.

`wpa_supplicant` and `systemd-resolvconf` are removed. iwd is the Wi-Fi supplicant, and
nothing in this install calls `resolvconf`. `/etc/iwd/main.conf` sets
`EnableNetworkConfiguration=false`, which is also iwd's default, so networkd keeps DHCP.

## ASTER WiFi troubleshooting

If **Resolve WiFi interface name** times out:

1. Confirm the driver is loaded: `lsmod | grep mt7925e` and `ip -o link show type wlan`.
2. Check rfkill: `rfkill list` — unblock with `rfkill unblock wifi` if soft-blocked.
3. Pin the interface instead of auto-detect: `-e os_wifi_interface=wlp0s20f3` (or in vault).
4. During arch-chroot install, WiFi connect is intentionally skipped (`network_connect_wifi=false`); run `workstation.sh` after first boot.

## Install lifecycle

The role installs the packages that provide its ASTER service units before
enabling them. In particular, `bluetooth.service` comes from `bluez`; the
network role runs before the XFCE role, so it cannot depend on XFCE installing
`bluez` later.

During `arch-chroot`, units are enabled for the installed system but are not
started because there is no booted systemd instance in the chroot. On a
normally booted host, the same tasks both enable and start the services.
