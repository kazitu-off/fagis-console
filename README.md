# FAGIS Console OS v2.0

## 📋 Description
A feature-rich console-based OS emulator with interactive terminal environment.

## ✨ Core Features

### Basic Commands
- `help`, `exit`, `clear`, `time`, `date`, `whoami`, `pwd`, `sysinfo`

### File Management
- `ls`/`dir` - List files
- `cd` - Change directory
- `mkdir` - Create directory
- `touch` - Create file
- `rm`/`del` - Delete files/dirs
- `cat` - View file contents
- `echo` - Print text

### Entertainment
- `calc` - Calculator
- `game` - Number guessing game

### Utilities
- `history` - Command history
- `checkinternet` - Test connection
- `urlcheck` - Check URL safety
- `update` - Check for updates
- `update_db` - Update malicious URL database

## 🚀 10 New Functions

| Command | Description |
|---------|-------------|
| `hash` | Calculate MD5/SHA1/SHA256 hashes |
| `timer` | Countdown timer |
| `stopwatch` | Stopwatch |
| `notes` | Notes manager (CRUD + search) |
| `portscan` | Port scanner |
| `password` | Password generator |
| `translate` | Simple translator |
| `qr` | QR code generator (requires qrencode) |
| `reminder` | Set reminders |
| `convert` | Unit converter |

## 🎨 Key Features
- **Color interface** (auto-disabled on Windows)
- **Multi-language** (EN/RU)
- **Command history**
- **Command aliases** (ls/dir, exit/quit, etc.)
- **Security features** (safe eval, path validation, malicious URL DB)

## 🚀 Quick Start
```bash
pip install requests
python3 fagis_console.py
```

## 📝 Examples
```
> password          # Generate password
> notes add TODO    # Create note
> urlcheck https://bit.ly/xxx  # Check URL
> convert           # Convert units
```

## 🔧 Requirements
- Python 3.6+
- requests library

---
**FAGIS Console OS** - Your console assistant! 🚀
