# YggAPI Configuration Examples

This folder contains example configuration files and setup scripts.

## Passkey Configuration

### Example File

Copy `yggapi_passkey.example.txt` to the qBittorrent engines folder and rename it:

**Windows:**

```powershell
$passkey = "your_actual_passkey"
$configPath = "$env:LOCALAPPDATA\qBittorrent\nova3\engines\yggapi_passkey.txt"
Set-Content -Path $configPath -Value $passkey -NoNewline
```

**Linux/Mac:**

```bash
echo "your_actual_passkey" > ~/.local/share/qBittorrent/nova3/engines/yggapi_passkey.txt
```

### Environment Variable

**Windows:**

```powershell
[System.Environment]::SetEnvironmentVariable('YGG_PASSKEY', 'your_passkey', 'User')
```

**Linux/Mac:**

```bash
export YGG_PASSKEY="your_passkey"
# Add to ~/.bashrc or ~/.zshrc for persistence
echo 'export YGG_PASSKEY="your_passkey"' >> ~/.bashrc
```

## qBittorrent Engines Directory

### Windows

```
%localappdata%\qBittorrent\nova3\engines\
```

Full path usually:

```
C:\Users\YourUsername\AppData\Local\qBittorrent\nova3\engines\
```

### macOS

```
~/Library/Application Support/qBittorrent/nova3/engines/
```

### Linux

```
~/.local/share/qBittorrent/nova3/engines/
```

## Quick Setup Script

### Windows (PowerShell)

```powershell
# Setup script - run after installing plugin via URL
param(
    [Parameter(Mandatory=$true)]
    [string]$Passkey
)

$enginesPath = "$env:LOCALAPPDATA\qBittorrent\nova3\engines"
$passkeyFile = Join-Path $enginesPath "yggapi_passkey.txt"

# Create directory if it doesn't exist
if (-not (Test-Path $enginesPath)) {
    New-Item -ItemType Directory -Path $enginesPath -Force
}

# Write passkey
Set-Content -Path $passkeyFile -Value $Passkey -NoNewline

Write-Host "✅ Passkey configured successfully!"
Write-Host "Location: $passkeyFile"
```

Save as `setup_passkey.ps1` and run:

```powershell
.\setup_passkey.ps1 -Passkey "your_passkey_here"
```

### Linux/Mac (Bash)

```bash
#!/bin/bash
# Setup script - run after installing plugin via URL

if [ -z "$1" ]; then
    echo "Usage: ./setup_passkey.sh YOUR_PASSKEY"
    exit 1
fi

ENGINES_PATH="$HOME/.local/share/qBittorrent/nova3/engines"
PASSKEY_FILE="$ENGINES_PATH/yggapi_passkey.txt"

# Create directory if it doesn't exist
mkdir -p "$ENGINES_PATH"

# Write passkey
echo -n "$1" > "$PASSKEY_FILE"

echo "✅ Passkey configured successfully!"
echo "Location: $PASSKEY_FILE"
```

Save as `setup_passkey.sh`, make executable, and run:

```bash
chmod +x setup_passkey.sh
./setup_passkey.sh "your_passkey_here"
```

## Get Your Passkey

1. Go to https://www.yggtorrent.org/user/account
2. Login with your account
3. Find the "Passkey" section
4. Copy the long alphanumeric string
5. Use it in one of the methods above

## Verification

After configuring, restart qBittorrent and try a search. If downloads work, your passkey is configured correctly!

## Security Notes

- ⚠️ **Never commit your passkey to version control!**
- ⚠️ **Don't share your passkey with others**
- ⚠️ **Keep `yggapi_passkey.txt` private**
- ✅ The `.gitignore` is configured to ignore this file
- ✅ Environment variables are safer than file storage
- ✅ Config file survives plugin auto-updates

## Troubleshooting

### Passkey not working

1. Check for extra spaces or newlines in the file
2. Verify passkey is correct from YggTorrent website
3. Ensure file is in the correct directory
4. Restart qBittorrent after configuration

### File not found

1. Check the engines directory exists
2. Verify qBittorrent is installed
3. Check you're using the correct path for your OS

### Permission denied

1. Ensure you have write permissions
2. Try running terminal as administrator (Windows)
3. Check file isn't read-only

## Additional Help

See `/docs/INSTALL_VIA_URL.md` for complete installation guide.
