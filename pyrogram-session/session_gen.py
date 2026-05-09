"""
Telegram String Session Generator — Python (Pyrogram)
======================================================
Requirements:  pip install pyrogram tgcrypto
Usage:         python3 session_gen.py
"""

import asyncio
import sys


def check_deps():
    try:
        import pyrogram  # noqa
    except ImportError:
        print("❌  Pyrogram is not installed.\n    Run: pip install pyrogram tgcrypto")
        sys.exit(1)


def banner():
    print("╔══════════════════════════════════════════╗")
    print("║  Telegram String Session Generator       ║")
    print("║  Powered by Pyrogram (Python)            ║")
    print("╚══════════════════════════════════════════╝")
    print()
    print("Get your API credentials at: https://my.telegram.org/apps")
    print()


def get_api_id() -> int:
    while True:
        try:
            val = int(input("Enter your API ID: ").strip())
            if val > 0:
                return val
            print("❌  Must be a positive integer.")
        except ValueError:
            print("❌  Invalid input — enter a number.")
        except (KeyboardInterrupt, EOFError):
            print("\nAborted."); sys.exit(0)


def get_api_hash() -> str:
    while True:
        try:
            val = input("Enter your API Hash: ").strip()
            if len(val) >= 10:
                return val
            print("❌  Too short — should be a 32-character hex string.")
        except (KeyboardInterrupt, EOFError):
            print("\nAborted."); sys.exit(0)


async def generate_session():
    from pyrogram import Client
    from pyrogram.errors import (
        ApiIdInvalid, PhoneNumberInvalid,
        PhoneCodeInvalid, PhoneCodeExpired,
        SessionPasswordNeeded, PasswordHashInvalid,
    )

    banner()
    api_id   = get_api_id()
    api_hash = get_api_hash()

    print("\n🔗  Connecting to Telegram …")

    client = Client(
        name=":memory:",
        api_id=api_id,
        api_hash=api_hash,
        in_memory=True,
    )

    await client.connect()

    # ── Phone number ────────────────────────────────────────────────────
    while True:
        try:
            phone = input("Enter your phone number (e.g. +919876543210): ").strip()
            sent  = await client.send_code(phone)
            break
        except ApiIdInvalid:
            print("❌  API ID / Hash is invalid. Please check my.telegram.org/apps")
            await client.disconnect(); return
        except PhoneNumberInvalid:
            print("❌  Invalid phone number. Use full international format: +919876543210")
        except (KeyboardInterrupt, EOFError):
            print("\nAborted."); await client.disconnect(); return

    # ── OTP code ────────────────────────────────────────────────────────
    while True:
        try:
            code = input("Enter the OTP code from your Telegram app: ").strip()
            await client.sign_in(phone, sent.phone_code_hash, code)
            break
        except PhoneCodeInvalid:
            print("❌  Wrong code. Try again.")
        except PhoneCodeExpired:
            print("❌  Code expired. Please restart the script.")
            await client.disconnect(); return
        except SessionPasswordNeeded:
            print("🔐  Two-Step Verification is enabled.")
            while True:
                try:
                    import getpass
                    password = getpass.getpass("Enter your 2FA password: ")
                    await client.check_password(password)
                    break
                except PasswordHashInvalid:
                    print("❌  Wrong password. Try again.")
                except (KeyboardInterrupt, EOFError):
                    print("\nAborted."); await client.disconnect(); return
            break
        except (KeyboardInterrupt, EOFError):
            print("\nAborted."); await client.disconnect(); return

    # ── Export session ──────────────────────────────────────────────────
    session_string = await client.export_session_string()

    print()
    print("╔══════════════════════════════════════════╗")
    print("║   ✅  YOUR STRING SESSION (Pyrogram)     ║")
    print("╚══════════════════════════════════════════╝")
    print()
    print(session_string)
    print()

    try:
        with open("pyrogram_session.txt", "w") as f:
            f.write(session_string + "\n")
        print("💾  Session saved to: pyrogram_session.txt")
    except OSError as e:
        print(f"⚠️   Could not save: {e}")

    try:
        me = await client.get_me()
        print()
        print("👤  Logged in as:")
        name = f"{me.first_name} {me.last_name or ''}".strip()
        print(f"    Name    : {name}")
        if me.username:
            print(f"    Username: @{me.username}")
        print(f"    User ID : {me.id}")
        print(f"    Phone   : +{me.phone_number}")
    except Exception as e:
        print(f"⚠️   Could not fetch account info: {e}")

    await client.disconnect()
    print()
    print("⚠️   KEEP YOUR SESSION STRING SECRET — it gives full access to your account!")


if __name__ == "__main__":
    check_deps()
    try:
        asyncio.run(generate_session())
    except KeyboardInterrupt:
        print("\nAborted.")
          
