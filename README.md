# <img src="https://raw.githubusercontent.com/Laiteux/YggAPI-qBittorrent-Search-Plugin/main/yggapi.ico" height="32" alt="YggTorrent Icon"></img> YggAPI qBittorrent Search Plugin

This [qBittorrent](https://github.com/qbittorrent/qBittorrent) Search Plugin uses [YggAPI](https://yggapi.eu), a non-official [YggTorrent](https://www.yggtorrent.top) search database.

![Demo GIF](https://raw.githubusercontent.com/Laiteux/YggAPI-qBittorrent-Search-Plugin/main/demo.gif)

## Installation

1. Download the plugin file: [yggapi.py](https://github.com/Laiteux/YggAPI-qBittorrent-Search-Plugin/blob/main/yggapi.py#L13)

2. Replace the `passkey` value on [line 13](https://github.com/Laiteux/YggAPI-qBittorrent-Search-Plugin/blob/main/yggapi.py#L13) with your [YggTorrent Passkey](https://www.yggtorrent.top/user/account) _(required for downloading)_

Then, in qBittorrent:

3. `View` menu -> Enable `Search Engine`

4. `Search` tab -> `Search plugins...` -> `Install a new one` -> `Local file`

Or, manually copy the `yggapi.py` & `yggapi.ico` files to the following location:

- Windows: `%localappdata%\qBittorrent\nova3\engines\`
- Mac: `~/Library/Application\ Support/qBittorrent/nova3/engines/`
- Linux: `~/.local/share/qBittorrent/nova3/engines/`

_Yarrr!_
