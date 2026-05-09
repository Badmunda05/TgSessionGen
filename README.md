# Telegram String Session Generator

Generate a **Telegram String Session** from your account using any of three tools:

| Folder | Language | Library |
|--------|----------|---------|
| `go-session/` | Go | [gogram](https://github.com/amarnathcjd/gogram) |
| `telethon-session/` | Python | [Telethon](https://github.com/LonamiWebs/Telethon) |
| `pyrogram-session/` | Python | [Pyrogram](https://github.com/pyrogram/pyrogram) |

A **String Session** lets your userbot or bot script log in as your Telegram account
on a VPS without needing OTP every time.

---

## Step 0 — Get API Credentials (Required for all tools)

1. Open **[https://my.telegram.org/apps](https://my.telegram.org/apps)**
2. Log in with your Telegram phone number
3. Create a new app (any name is fine)
4. Copy your **App ID** (a number like `12345678`) and **App Hash** (32-char hex string)

---

## Clone the Repo

```bash
git clone https://github.com/Badmunda05/TgSessionGen
```

---

## Option 1 — Pyrogram (Python)

### Install & Run

```bash
cd ~/TgSessionGen/pyrogram-session
pip3 install -r requirements.txt
python3 session_gen.py
```

### What it looks like

```
Enter your API ID: 12345678
Enter your API Hash: abcdef1234567890abcdef1234567890

🔗  Connecting to Telegram …
Enter your phone number (e.g. +919876543210): +919876543210
Enter the OTP code from your Telegram app: 55123
Enter your 2FA password (if enabled): ••••••••

✅  YOUR STRING SESSION (Pyrogram)

BQHBfTsAxx_NOTREAL_xxxxxxxxxxxxxxxxxxxxxxxxxxxx...

💾  Session saved to: pyrogram_session.txt
👤  Name: John Doe | @johndoe | ID: 123456789
```

---

## Option 2 — Telethon (Python)

### Install & Run

```bash
cd ~/TgSessionGen/telethon-session
pip3 install -r requirements.txt
python3 session_gen.py
```

---

## Option 3 — Go / GoGram

### Install Go on Ubuntu / Debian VPS

```bash
sudo apt update && sudo apt install -y golang-go
go version   # should show go1.21+
```

### Install Go manually (latest)

```bash
wget https://go.dev/dl/go1.22.4.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.22.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc
```

### Install & Run

```bash
cd ~/TgSessionGen/go-session
go mod tidy
go run main.go
```

### Build standalone binary (no Go needed after this)

```bash
cd ~/TgSessionGen/go-session
go build -o session-gen main.go
./session-gen
```

---

## VPS Quick-Start (Fresh Ubuntu — Copy & Paste)

### Pyrogram

```bash
sudo apt update && sudo apt install -y python3 python3-pip git
git clone https://github.com/Badmunda05/TgSessionGen
cd ~/TgSessionGen/pyrogram-session
pip3 install -r requirements.txt
python3 session_gen.py
```

### Telethon

```bash
sudo apt update && sudo apt install -y python3 python3-pip git
git clone https://github.com/Badmunda05/TgSessionGen
cd ~/TgSessionGen/telethon-session
pip3 install -r requirements.txt
python3 session_gen.py
```

### Go

```bash
sudo apt update && sudo apt install -y golang-go git
git clone https://github.com/Badmunda05/TgSessionGen
cd ~/TgSessionGen/go-session
go mod tidy
go run main.go
```

---

## Using Your Session String in a Bot

### Pyrogram userbot

```python
from pyrogram import Client

app = Client(
    "mybot",
    api_id=12345678,
    api_hash="your_api_hash",
    session_string="YOUR_PYROGRAM_SESSION_STRING",
)

async def main():
    async with app:
        me = await app.get_me()
        print(f"Logged in as: {me.first_name}")

import asyncio
asyncio.run(main())
```

### Telethon userbot

```python
from telethon import TelegramClient
from telethon.sessions import StringSession

client = TelegramClient(
    StringSession("YOUR_TELETHON_SESSION_STRING"),
    api_id=12345678,
    api_hash="your_api_hash",
)

async def main():
    await client.start()
    me = await client.get_me()
    print(f"Logged in as: {me.first_name}")

import asyncio
asyncio.run(main())
```

### GoGram userbot

```go
package main

import (
    "fmt"
    "github.com/amarnathcjd/gogram/telegram"
)

func main() {
    client, _ := telegram.NewClient(telegram.ClientConfig{
        AppID:         12345678,
        AppHash:       "your_api_hash",
        StringSession: "YOUR_GOGRAM_SESSION_STRING",
    })
    client.Conn()
    me, _ := client.GetMe()
    fmt.Println("Logged in as:", client.JSON(me, true))
    client.Idle()
}
```

---

## Project Structure

```
TgSessionGen/
├── go-session/
│   ├── main.go                 ← Go session generator (GoGram)
│   └── go.mod                  ← Go module file
├── telethon-session/
│   ├── session_gen.py          ← Python session generator (Telethon)
│   └── requirements.txt
├── pyrogram-session/
│   ├── session_gen.py          ← Python session generator (Pyrogram)
│   └── requirements.txt
├── .gitignore
└── README.md
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `go: command not found` | Install Go — see Option 3 above |
| `ModuleNotFoundError: pyrogram` | `pip3 install pyrogram tgcrypto` |
| `ModuleNotFoundError: telethon` | `pip3 install telethon` |
| OTP not arriving | Check Telegram app — code comes as a message from Telegram |
| `PHONE_NUMBER_INVALID` | Use full format: `+919876543210` |
| `API_ID_INVALID` | Double-check App ID and Hash from my.telegram.org |
| `AUTH_KEY_UNREGISTERED` | Session expired — generate a new one |
| 2FA prompt | Enter your Telegram Two-Step Verification password |
| `go mod tidy` fails | Check internet connection |

---

## Security

- **Never share your session string** — it gives full access to your account
- **Never push it to GitHub** — it's already in `.gitignore`
- Use environment variables when deploying bots:

```bash
export SESSION="your_session_string"
```

```python
import os
SESSION = os.environ["SESSION"]
```

---

## License

MIT — free to use, modify, and distribute.
