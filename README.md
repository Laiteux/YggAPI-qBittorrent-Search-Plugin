# <img src="https://raw.githubusercontent.com/Laiteux/YggAPI-qBittorrent-Search-Plugin/main/yggapi.ico" height="32" alt="YggTorrent Icon"></img> YggAPI qBittorrent Search Plugin

This [qBittorrent](https://github.com/qbittorrent/qBittorrent) Search Plugin uses [YggAPI](https://yggapi.eu), a non-official [YggTorrent](https://www.yggtorrent.org) search database.

![Demo GIF](https://raw.githubusercontent.com/Sterbweise/YggAPI-qBittorrent-Search-Plugin/main/assets/demo.gif)

## 📚 Documentation

- **[Installation Guide](docs/INSTALL_VIA_URL.md)** - URL installation with auto-update
- **[Testing Guide](docs/TEST_GUIDE.md)** - Complete testing documentation
- **[Configuration Examples](examples/)** - Setup scripts and templates

## 📂 Quick Links

- 🔧 [Configuration Examples](examples/)
- 🧪 [Test Suite](tests/) (64 tests)
- 📖 [Documentation](docs/)
- 🎬 [Assets](assets/)

## Features

- **Automatic URL Discovery**: Fetches the current YggTorrent URL from [yeeti.io/@ygg](https://yeeti.io/@ygg) automatically
- **Smart Caching**: Caches the discovered URL for 24 hours to reduce network requests
- **Enhanced Categories**: Support for 8+ categories (movies, TV, music, games, anime, software, pictures, books)
- **Robust Error Handling**: Automatic retry logic with fallback mechanisms
- **Modern Python Code**: Type hints, proper class structure, and PEP 8 compliant
- **Better Performance**: Optimized API calls with configurable pagination

## 📦 Installation

### Method 1: Install via URL (Recommended - Auto-Updates!)

**One-click installation with automatic updates:**

1. Open qBittorrent → **View** → Enable **Search Engine**
2. **Search** tab → **Search plugins...** → **Install a new one** → **Web link**
3. Paste this URL:

   ```
   https://raw.githubusercontent.com/OWNER_USERNAME/YggAPI-qBittorrent-Search-Plugin/main/yggapi.py
   ```

   _(Replace `OWNER_USERNAME` with the actual GitHub repository owner)_

4. **Configure your passkey** - Create a file:

   - **Windows**: `%localappdata%\qBittorrent\nova3\engines\yggapi_passkey.txt`
   - **Mac**: `~/Library/Application Support/qBittorrent/nova3/engines/yggapi_passkey.txt`
   - **Linux**: `~/.local/share/qBittorrent/nova3/engines/yggapi_passkey.txt`

   Put ONLY your passkey in this file (get it from https://www.yggtorrent.org/user/account)

5. **Auto-update anytime**: Click **Search plugins...** → **Check for updates**

✅ **Benefits**: One-click install, automatic updates, passkey preserved on updates!

📖 **Detailed Guide**: See [INSTALL_VIA_URL.md](/docs/INSTALL_VIA_URL.md)

---

### Method 2: Install via Local File

1. Download the plugin file: [yggapi.py](https://github.com/Laiteux/YggAPI-qBittorrent-Search-Plugin/blob/main/yggapi.py)

2. **Configure your Passkey**: Create `yggapi_passkey.txt` (recommended) OR edit the plugin file

3. `View` menu → Enable `Search Engine`

4. `Search` tab → `Search plugins...` → `Install a new one` → `Local file`

---

### Manual Installation

Copy the `yggapi.py` & `yggapi.ico` files to:

- **Windows**: `%localappdata%\qBittorrent\nova3\engines\`
- **Mac**: `~/Library/Application Support/qBittorrent/nova3/engines/`
- **Linux**: `~/.local/share/qBittorrent/nova3/engines/`

## ⚙️ Configuration

### Passkey Configuration (3 Methods)

The plugin supports multiple ways to configure your YggTorrent passkey:

**Priority Order:** Environment Variable > Config File > Hardcoded

#### 1. Config File (Recommended)

Create `yggapi_passkey.txt` in the engines folder with just your passkey:

```
your_passkey_here
```

#### 2. Environment Variable

```bash
# Windows (PowerShell)
[System.Environment]::SetEnvironmentVariable('YGG_PASSKEY', 'your_passkey', 'User')

# Linux/Mac
export YGG_PASSKEY="your_passkey"
```

#### 3. Edit Plugin File

Modify line ~70 in `yggapi.py`:

```python
return "YOUR_PASSKEY_HERE"  # Replace with your passkey
```

⚠️ **Note**: Methods 1 & 2 survive auto-updates! Method 3 gets overwritten.

---

### Advanced Settings

You can customize the plugin behavior by modifying the `YggAPIConfig` class:

```python
class YggAPIConfig:
    # Search Configuration
    DEFAULT_PER_PAGE: int = 100          # Results per page
    DEFAULT_ORDER_BY: str = "seeders"    # Sort by seeders
    MAX_RETRIES: int = 3                 # Retry failed requests
    RETRY_DELAY_SECONDS: int = 2         # Delay between retries

    # URL Cache Settings
    URL_CACHE_DURATION_HOURS: int = 24   # Cache YggTorrent URL for 24 hours
```

### Supported Categories

#### qBittorrent Standard Categories

- `all` - All categories
- `movies` - Films (2183)
- `tv` - TV Series (2184)
- `music` - Music (2148)
- `games` - Video Games (2142)
- `anime` - Animation Series (2179)
- `software` - Applications (2144)
- `pictures` - Images (2191)
- `books` - eBooks (2140)

#### Extended YggTorrent Categories

**Films & Vidéos (2145)**

- `animation` - Animation (2178)
- `animation_series` - Animation Série (2179)
- `concert` - Concert (2180)
- `documentary` - Documentaire (2181)
- `tv_show` - Emission TV (2182)
- `movie` - Film (2183)
- `series` - Série TV (2184)
- `show` - Spectacle (2185)
- `sport` - Sport (2186)
- `videoclip` - Video-Clip (2187)

**Ebook (2140)**

- `audiobook` - Audio (2151)
- `comics` - Comics (2153)
- `books` - Livres (2154)
- `manga` - Manga (2155)
- `press` - Presse (2156)

**Audio (2139)**

- `karaoke` - Karaoké (2147)
- `samples` - Samples (2149)
- `podcast` - Podcast Radio (2150)

**Jeux vidéo (2142)**

- `games_linux` - Linux (2159)
- `games_mac` - MacOS (2160)
- `games_microsoft` - Microsoft (2162)
- `games_nintendo` - Nintendo (2163)
- `games_sony` - Sony (2164)
- `games_windows` - Windows (2161)

**Applications (2144)**

- `training` - Formation (2176)
- `software_linux` - Linux (2171)
- `software_mac` - MacOS (2172)
- `software_windows` - Windows (2173)

**Nulled (2300)**

- `nulled` - Scripts & CMS (2300)
- `wordpress` - WordPress (2301)
- `php_scripts` - Scripts PHP & CMS (2302)

**3D Printing (2200)**

- `3d_printing` - Imprimante 3D (2200)
- `3d_objects` - Objets (2201)
- `3d_characters` - Personnages (2202)

**GPS (2143)**

- `gps` - GPS (2143)
- `gps_apps` - Applications (2168)
- `gps_maps` - Cartes (2169)

**Émulation (2141)**

- `emulation` - Émulation (2141)
- `emulator` - Émulateur (2157)
- `roms` - ROM/ISO (2158)

> **Note**: The plugin supports **60+ categories** covering all YggTorrent content types. You can use qBittorrent standard categories or extended YggTorrent-specific categories for more precise filtering.

## 🔄 How Automatic URL Discovery Works

The plugin automatically fetches the current YggTorrent URL from [yeeti.io/@ygg](https://yeeti.io/@ygg), which always maintains the most up-to-date YggTorrent domain. This means:

1. **No manual updates needed** when YggTorrent changes domains
2. **Cached for 24 hours** to minimize network overhead
3. **Automatic fallback** to default URL if fetch fails
4. **Transparent operation** - works silently in the background

## 🧪 Testing

The plugin includes a comprehensive test suite with **64 tests** covering all functionality.

### Run Tests

```bash
# Run all tests
python test_yggapi.py

# Run with verbose output
python -m unittest test_yggapi.py -v

# Run specific test class
python -m unittest test_yggapi.TestURLCache
```

### Test Coverage

- ✅ Configuration validation (60+ categories)
- ✅ URL caching and expiration
- ✅ Automatic URL discovery
- ✅ Search functionality (pagination, error handling)
- ✅ Data parsing (dates, sizes)
- ✅ Category resolution
- ✅ Integration workflows
- ✅ Edge cases

**Test Results:** 64/64 tests passing ✅

See **TEST_GUIDE.md** for complete testing documentation.

## 🛠️ Troubleshooting

### Plugin not appearing in qBittorrent

- Ensure Python 3.6+ is installed and accessible to qBittorrent
- Check that the plugin files are in the correct engines directory
- Restart qBittorrent after installation

### No search results

- Verify your passkey is correctly configured
- Check that YggAPI service (https://yggapi.eu) is accessible
- Ensure you have an active YggTorrent account

### Downloads not working

- Your passkey must be valid and from an active YggTorrent account
- Get your passkey from: https://www.yggtorrent.org/user/account

---

## 📂 Project Structure

```
YggAPI-qBittorrent-Search-Plugin/
├── yggapi.py                # Main plugin (must be in root)
├── yggapi.ico               # Plugin icon
├── README.md                # This file
├── PROJECT_STRUCTURE.md     # Detailed structure documentation
├── docs/                    # Documentation
│   ├── INSTALL_VIA_URL.md
│   ├── TEST_GUIDE.md
│   └── TESTING_QUICKREF.md
├── tests/                   # Test suite (64 tests)
│   ├── test_yggapi.py
│   └── test_yeeti_url_fetch.py
├── examples/                # Configuration examples & scripts
│   ├── README.md
│   └── yggapi_passkey.example.txt
└── assets/                  # Media files
    └── demo.gif
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

---

## 🙏 Credits

- **Original Author:** [Laiteux](https://github.com/Laiteux) (matt@laiteux.dev)
- **Contributors:** [Sterbweise](https://github.com/Sterbweise) (contact@sterbweise.dev)
- **YggAPI Service:** https://yggapi.eu
- **YggTorrent:** https://www.yggtorrent.org
- **URL Tracking:** https://yeeti.io/@ygg

---

**Version:** 2.0 | **Tests:** 64/64 passing ✅ | **Categories:** 60+
