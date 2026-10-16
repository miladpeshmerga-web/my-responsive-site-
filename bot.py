from datetime import datetime
import json
import os
import requests

TOKEN = os.environ.get("BOT_TOKEN")

# لینکە سەرەکییەکان
WEB_APP_URL = "[https://miladpeshmerga-web.github.io/my-responsive-site-/](https://miladpeshmerga-web.github.io/my-responsive-site-/)"
SNAPCHAT_WEB_APP_URL = "[https://miladpeshmerga-web.github.io/my-responsive-site-/snapchat.html](https://miladpeshmerga-web.github.io/my-responsive-site-/snapchat.html)"
SMM_WEB_APP_URL = "[https://miladpeshmerga-web.github.io/my-responsive-site-/smm.html](https://miladpeshmerga-web.github.io/my-responsive-site-/smm.html)"
PREMIUM_WEB_APP_URL = "[https://miladpeshmerga-web.github.io/my-responsive-site-/telegram-premium.html](https://miladpeshmerga-web.github.io/my-responsive-site-/telegram-premium.html)"
TIKTOK_WEB_APP_URL = "[https://miladpeshmerga-web.github.io/my-responsive-site-/tiktok.html](https://miladpeshmerga-web.github.io/my-responsive-site-/tiktok.html)"
PUBG_WEB_APP_URL = "[https://miladpeshmerga-web.github.io/my-responsive-site-/pubg.html](https://miladpeshmerga-web.github.io/my-responsive-site-/pubg.html)"

def load_users():
    """خوێندنەوەی لیستی بەکارهێنەران لە فایلی users.json بە شێوەی ئۆبێکت/دیکشنری"""
    users_data = {}
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    if isinstance(data, list):
                        for uid in data:
                            users
