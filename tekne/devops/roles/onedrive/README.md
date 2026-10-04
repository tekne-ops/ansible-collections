# OneDrive Role

Installs and configures OneDrive client (abraunegg fork) for all users defined in ansible-role-user.

## What It Does

1. **Installs OneDrive package** (onedrive-abraunegg)
2. **Creates config directory** (`~/.config/onedrive`) for each user
3. **Creates sync directory** (`/srv/OneDrive`) owned by `dvaliente`
4. **Copies config file and `sync_list`** to dvaliente's config directory
5. **Verifies installation** and configuration

## Requirements

- `community.general` collection (for `pacman` module)
- `ansible-role-user` must run before this role (provides `users` variable)

```bash
ansible-galaxy collection install community.general
```

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `onedrive_package` | `onedrive-abraunegg` | OneDrive package to install |
| `onedrive_owner` | `dvaliente` | Owner of the sync directory |
| `onedrive_group` | `users` | Group of the sync directory |
| `onedrive_sync_dir` | `/srv/OneDrive` | Sync directory |
| `onedrive_config_dir` | `.config/onedrive` | Config directory in home |

## Files Deployed

| Source | Destination | Mode |
|--------|-------------|------|
| `templates/onedrive.j2` | `~/.config/onedrive/config` | 0600 |
| `files/sync_list` | `~/.config/onedrive/sync_list` | 0600 |

## Directories Created

- `/home/dvaliente/.config/onedrive/` (mode 0700)
- `/srv/OneDrive/` (owner `dvaliente`, mode 0700, user ACL `rwx`)

## Dependencies

- **ansible-role-user**: Provides the `users` list for per-user configuration

## Example Playbook

```yaml
- hosts: workstations
  roles:
    - ansible-role-user      # Creates users first
    - ansible-role-onedrive  # Configures OneDrive for those users
```

## Tags

| Tag | Description |
|-----|-------------|
| `onedrive` | All OneDrive tasks |
| `packages` | Package installation only |
| `directories` | /var/log/onedrive and per-user dirs |
| `config` | Config file and directory creation |
| `verify` | Verification tasks |

## Post-Installation

After running the role, each user needs to authenticate:

```bash
onedrive --synchronize --single-directory
```

## License

MIT-0

## Author

dvaliente
