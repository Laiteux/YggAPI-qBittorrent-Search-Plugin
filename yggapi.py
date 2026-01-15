#VERSION: 1.2
#AUTHORS: Laiteux (matt@laiteux.dev)

import json
import os
from datetime import datetime
from helpers import retrieve_url
from novaprinter import prettyPrinter

class yggapi(object):
    name = "YggAPI"
    url = "https://yggapi.eu"
    ygg_url = "https://www.yggtorrent.org"
    passkey = "YOUR_PASSKEY_HERE" # https://www.yggtorrent.org/user/account

    supported_categories = {
        "all": "",
        "movies": "2183",
        "tv": "2184",
        "anime": "2179"
    }

    ygg_categories = {
        "2183": "film",
        "2184": "série-tv",
        "2178": "animation",
        "2179": "animation-série"
    }

    def __init__(self):
        self.page = 1
        self.max_page = 0 # 0 = unlimited
        self.per_page = 100
        self.order_by = "seeders"

        # Load passkey from environment variable or file if provided
        env_passkey = os.getenv('YGG_PASSKEY')
        passkey_file = os.getenv('YGG_PASSKEY_FILE')
        if passkey_file:
            try:
                with open(passkey_file, 'r') as f:
                    self.passkey = f.read().strip()
            except (IOError, OSError):
                # If file can't be read, fall back to env var or class default
                if env_passkey is not None:
                    self.passkey = env_passkey
        elif env_passkey is not None:
            self.passkey = env_passkey

    def search(self, what, cat="all"):
        category_param = ""

        if cat != "all" and cat in self.supported_categories:
            category_param = f"&category_id={self.supported_categories[cat]}"

        while True:
            search_url = f"{self.url}/torrents?q={what}{category_param}&page={self.page}&per_page={self.per_page}&order_by={self.order_by}"

            response = retrieve_url(search_url)
            results = json.loads(response)

            if not results:
                break

            for torrent in results:
                result = {
                    "link": f"{self.url}/torrent/{torrent['id']}/download?passkey={self.passkey}",
                    "name": torrent["title"],
                    "size": str(torrent["size"]),
                    "seeds": torrent["seeders"],
                    "leech": torrent["leechers"],
                    "engine_url": self.url,
                    "desc_link": torrent["link"],
                    "pub_date": int(datetime.strptime(torrent["uploaded_at"], "%Y-%m-%dT%H:%M:%S%z").timestamp())
                }

                prettyPrinter(result)

            if len(results) == self.per_page and (self.max_page <= 0 or self.page < self.max_page):
                self.page += 1
            else:
                break
