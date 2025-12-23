# Install YggAPI via GitHub URL (Auto-Update Enabled)

## Quick Installation via URL

qBittorrent can install and auto-update plugins directly from GitHub URLs!

### Step 1: Install Plugin from URL

1. Open **qBittorrent**
2. Go to **View** → Enable **Search Engine**
3. Click on **Search** tab
4. Click **Search plugins...** button
5. Click **Install a new one** → **Web link**
6. Paste this URL:

```
https://raw.githubusercontent.com/Laiteux/YggAPI-qBittorrent-Search-Plugin/main/yggapi.py
```

**Replace `Laiteux`** with the actual GitHub repository owner.

### Step 2: Configure Your Passkey

After installation, you have **3 options** to configure your passkey:

#### Option 1: Config File (Recommended for Auto-Updates)

Create a file named `yggapi_passkey.txt` in the engines folder:

**Windows:**

```
%localappdata%\qBittorrent\nova3\engines\yggapi_passkey.txt
```

**Mac:**

```
~/Library/Application Support/qBittorrent/nova3/engines/yggapi_passkey.txt
```

**Linux:**

```
~/.local/share/qBittorrent/nova3/engines/yggapi_passkey.txt
```

Put ONLY your passkey in this file (one line, no extra characters).

#### Option 2: Environment Variable

Set the `YGG_PASSKEY` environment variable:

**Windows (PowerShell):**

```powershell
[System.Environment]::SetEnvironmentVariable('YGG_PASSKEY', 'your_passkey_here', 'User')
```

**Mac/Linux:**

```bash
export YGG_PASSKEY="your_passkey_here"
# Add to ~/.bashrc or ~/.zshrc for persistence
```

#### Option 3: Edit Plugin File (Not Recommended for Auto-Updates)

Edit `yggapi.py` in the engines folder and change line ~70:

```python
return "YOUR_PASSKEY_HERE"  # Replace with your actual passkey
```

⚠️ **Warning:** This will be overwritten on auto-update!

### Step 3: Get Your Passkey

1. Go to https://www.yggtorrent.org/user/account
2. Copy your passkey (long alphanumeric string)
3. Use it in one of the methods above

---

## Auto-Update Feature

### Enable Auto-Updates

The plugin is configured to auto-update when installed via URL!

**To check for updates:**

1. Go to **Search** tab
2. Click **Search plugins...**
3. Click **Check for updates**
4. qBittorrent will compare versions and update if newer version available

### How It Works

- qBittorrent reads the `# VERSION: X.X` line in the plugin
- When you click "Check for updates", it fetches the latest version from GitHub
- If the remote version is newer, it updates automatically
- **Your passkey stays safe** if you use Option 1 or 2 above!

### Version History

- **v2.0** - Current version (automatic URL discovery, 60+ categories)
- **v1.2** - Original version

---

## Complete Setup Example (Windows)

```powershell
# 1. Install via URL in qBittorrent (paste the GitHub raw URL)

# 2. Create passkey file
$passkey = "your_passkey_here"
$configPath = "$env:LOCALAPPDATA\qBittorrent\nova3\engines\yggapi_passkey.txt"
Set-Content -Path $configPath -Value $passkey -NoNewline

# 3. Restart qBittorrent (if needed)

# 4. Start searching!
```

---

## Complete Setup Example (Linux/Mac)

```bash
# 1. Install via URL in qBittorrent (paste the GitHub raw URL)

# 2. Create passkey file
echo "your_passkey_here" > ~/.local/share/qBittorrent/nova3/engines/yggapi_passkey.txt

# 3. Restart qBittorrent (if needed)

# 4. Start searching!
```

---

## Updating

### Manual Update

Just click **Check for updates** in the Search plugins dialog.

### Automatic Check

qBittorrent doesn't auto-check by default. You need to manually click "Check for updates" periodically.

---

## Benefits of URL Installation

✅ **One-click installation** - No file downloads  
✅ **Auto-updates** - Get new features automatically  
✅ **Passkey preserved** - Separate config file not overwritten  
✅ **Always latest version** - Stay up-to-date with improvements  
✅ **Easy deployment** - Share one URL with all users

---

## Security Notes

### Passkey Security

- **Never commit your passkey to Git!**
- Use `.gitignore` for `yggapi_passkey.txt`
- Environment variables are safer than hardcoded values
- Config file keeps passkey separate from plugin code

### URL Security

- Only install from **trusted sources**
- Verify the GitHub repository is legitimate
- Check the code before installing (it's open source!)

---

## Troubleshooting

### Plugin not updating

1. Check your internet connection
2. Verify the GitHub URL is correct
3. Manually delete old plugin and reinstall

### Passkey not working

1. Check passkey has no extra spaces or newlines
2. Verify passkey is correct from YggTorrent website
3. Restart qBittorrent after configuring

### Plugin not found after installation

1. Restart qBittorrent
2. Check Search Engine is enabled (View menu)
3. Verify plugin file exists in engines folder

---

## For Repository Owners

### Setting Up Your Repository for URL Installation

1. **Ensure VERSION line is at top of file:**

```python
# VERSION: 2.0
```

2. **Host on GitHub** with public access

3. **Provide Raw URL** to users:

```
https://raw.githubusercontent.com/USERNAME/REPO/BRANCH/yggapi.py
```

4. **Update VERSION** when releasing changes:

```python
# VERSION: 2.1  # Increment for updates
```

5. **Add to .gitignore:**

```
yggapi_passkey.txt
__pycache__/
*.pyc
.ygg_url_cache.json
```

### Testing Auto-Update

1. Install plugin via URL
2. Modify VERSION line to a higher number
3. Commit and push
4. Click "Check for updates" in qBittorrent
5. Verify plugin updates automatically

---

**Happy Searching!**

_With URL installation, you're always running the latest version!_
