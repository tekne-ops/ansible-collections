# User Role

Manages system users, passwords, SSH authorized keys, sudoers, and home-directory configuration for Arch Linux.

## What It Does

1. **Validates** that `user_password` is defined (e.g. from vault).
2. **Creates users** from the `user_accounts` list (shell, group, groups, password).
3. **Sets root password** when `user_manage_root_password` is true.
4. **Installs SSH identity keys** from vault variables `id_rsa-<user>` and `id_rsa.pub-<user>` into `~/.ssh/`, and configures `authorized_keys` from the public key.
5. **Deploys sudoers files** to `/etc/sudoers.d/` (e.g. `sudo_dvaliente`, `sudo_devops`).
6. **Creates home directories** (e.g. `.config/systemd/user`, `.gnupg`, `.ssh`, `bin`) and copies dotfiles (`.bashrc`, `.vimrc`, `pikaur.conf`).

## Requirements

- `ansible.posix` collection (for `authorized_key` module)

```bash
ansible-galaxy collection install ansible.posix
```

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `user_accounts` | See defaults | List of users to create |
| `user_default_shell` | `/bin/bash` | Default shell for users |
| `user_default_group` | `users` | Default primary group |
| `user_manage_root_password` | `true` | Whether to set root password |
| `user_directories` | See defaults | Directories to create in each user's home |
| `user_password` | **(vault)** | Default password hash for users (required) |
| `root_password` | **(vault)** | Root password hash (falls back to user_password) |

### User Object Properties

Each user in the `user_accounts` list supports:

| Property | Required | Default | Description |
|----------|----------|---------|-------------|
| `name` | Yes | - | Username |
| `groups` | Yes | - | Comma-separated secondary groups |
| `shell` | No | `user_default_shell` | User's login shell |
| `group` | No | `user_default_group` | Primary group |
| `password` | No | `user_password` | User-specific password hash |
| `ssh_exclusive` | No | `true` | Replace all existing SSH keys |

### Default User Directories

Created in each user's home (mode 0755 except `.gnupg`/`.ssh` 0700):

- `.config/systemd/user`, `.config/autostart`, `.config/remmina`, `.config/pikaur.conf` (via copy)
- `.vim/autoload`, `.vim/bundle`, `.vim/colors`
- `bin`, `.gnupg`, `.ssh`

## Files Deployed

| Source (in role `files/`) | Destination | Mode |
|---------------------------|-------------|------|
| `bashrc` | `~/.bashrc` | 0644 |
| `vimrc` | `~/.vimrc` | 0644 |
| `pikaur.conf` | `~/.config/pikaur.conf` | 0644 |
| `sudo_dvaliente` | `/etc/sudoers.d/sudo_dvaliente` | 0440 |
| `sudo_devops` | `/etc/sudoers.d/sudo_devops` | 0440 |

Vault variables `id_rsa-<user>` and `id_rsa.pub-<user>` are written to `~/.ssh/id_rsa` (mode 0600) and `~/.ssh/id_rsa.pub` (mode 0644). The public key is also installed in `~/.ssh/authorized_keys`.

Sudoers files are validated with `visudo -cf %s` before deployment.

## Example Playbook

```yaml
- hosts: localhost
  roles:
    - role: tekne.devops.user
      vars:
        user_accounts:
          - name: admin
            groups: 'wheel,docker'
          - name: deploy
            groups: 'deploy'
            shell: /bin/zsh
```

## Tags

| Tag | Description |
|-----|-------------|
| `user` | All user tasks |
| `validation` | Variable validation only |
| `create` | User creation only |
| `root` | Root password management only |
| `ssh` | SSH key configuration only |
| `sudo` | Sudoers file deployment |
| `home_config` | Home directories and dotfiles |

## Security

Password hashes should be stored in an encrypted vault file:

```bash
ansible-vault create vault
# In vault: user_password: '$6$...'  (and optionally root_password)

ansible-playbook playbook.yml --ask-vault-pass
```

Generate password hashes with:

```bash
# Interactive (password not stored in shell history)
mkpasswd -m sha-512

# One-liner (single-quote the password so $ is not expanded)
openssl passwd -6 'your-password'
```

## License

MIT

## Author

dvaliente
