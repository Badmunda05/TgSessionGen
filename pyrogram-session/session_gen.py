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
        print("❌  Pyrogram is not installed.")
        print("Run: pip install pyrogram tgcrypto")
        sys.exit(1)


def banner():
    print("╔══════════════════════════════════════════╗")
    print("║  Telegram String Session Generator      ║")
    print("║  Powered by Pyrogram (Python)           ║")
    print("╚══════════════════════════════════════════╝")
    print()
    print("Get your API credentials at:")
    print("https://my.telegram.org/apps")
    print()


def get_api_id() -> int:
    while True:
        try:
            val = int(input("Enter your API ID: ").strip())

            if val > 0:
                return val

            print("❌ Must be a positive integer.")

        except ValueError:
            print("❌ Invalid input — enter numbers only.")

        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            sys.exit(0)


def get_api_hash() -> str:
    while True:
        try:
            val = input("Enter your API Hash: ").strip()

            if len(val) >= 10:
                return val

            print("❌ Invalid API Hash.")

        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            sys.exit(0)


async def generate_session():
    from pyrogram import Client, enums
    from pyrogram.errors import (
        ApiIdInvalid,
        PhoneNumberInvalid,
        PhoneCodeInvalid,
        PhoneCodeExpired,
        SessionPasswordNeeded,
        PasswordHashInvalid,
    )

    banner()

    api_id = get_api_id()
    api_hash = get_api_hash()

    print("\n🔗 Connecting to Telegram...")

    client = Client(
        name=":memory:",
        api_id=api_id,
        api_hash=api_hash,
        in_memory=True,
    )

    await client.connect()

    # ── Phone Number ────────────────────────────────────────────────
    while True:
        try:
            phone = input(
                "Enter your phone number (e.g. +919876543210): "
            ).strip()

            sent_code = await client.send_code(phone)

            break

        except ApiIdInvalid:
            print("❌ Invalid API ID or API Hash.")
            await client.disconnect()
            return

        except PhoneNumberInvalid:
            print("❌ Invalid phone number format.")

        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            await client.disconnect()
            return

    # ── OTP Login ───────────────────────────────────────────────────
    while True:
        try:
            otp = input(
                "Enter the OTP code from Telegram: "
            ).strip()

            await client.sign_in(
                phone_number=phone,
                phone_code_hash=sent_code.phone_code_hash,
                phone_code=otp
            )

            break

        except PhoneCodeInvalid:
            print("❌ Invalid OTP code.")

        except PhoneCodeExpired:
            print("❌ OTP expired. Restart the script.")
            await client.disconnect()
            return

        except SessionPasswordNeeded:
            print("🔐 Two-Step Verification Enabled.")

            while True:
                try:
                    import getpass

                    password = getpass.getpass(
                        "Enter your 2FA password: "
                    )

                    await client.check_password(password)

                    break

                except PasswordHashInvalid:
                    print("❌ Wrong password.")

                except (KeyboardInterrupt, EOFError):
                    print("\nAborted.")
                    await client.disconnect()
                    return

            break

        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            await client.disconnect()
            return

    # ── Generate Session ────────────────────────────────────────────
    session_string = await client.export_session_string()

    print()
    print("╔══════════════════════════════════════════╗")
    print("║   ✅ YOUR STRING SESSION (Pyrogram)     ║")
    print("╚══════════════════════════════════════════╝")
    print()

    print(session_string)
    print()

    # ── Send to Saved Messages ──────────────────────────────────────
    try:
        message_text = (
            "✅ YOUR STRING SESSION (Pyrogram)\n\n"
            f"`{session_string}`\n\n"
            "⚠️ KEEP YOUR SESSION STRING SECRET!"
        )

        await client.send_message(
            chat_id="me",
            text=message_text,
            parse_mode=enums.ParseMode.MARKDOWN
        )

        print("📨 Session sent to Saved Messages.")

    except Exception as e:
        print(f"⚠️ Could not send message: {e}")

    # ── Account Info ────────────────────────────────────────────────
    try:
        me = await client.get_me()

        print()
        print("👤 Logged in as:")

        full_name = f"{me.first_name} {me.last_name or ''}".strip()

        print(f"    Name    : {full_name}")

        if me.username:
            print(f"    Username: @{me.username}")

        print(f"    User ID : {me.id}")
        print(f"    Phone   : +{me.phone_number}")

    except Exception as e:
        print(f"⚠️ Could not fetch account info: {e}")

    await client.disconnect()

    print()
    print("⚠️ KEEP YOUR SESSION STRING SECRET.")
    print("It gives full access to your Telegram account.")


if __name__ == "__main__":
    check_deps()

    try:
        asyncio.run(generate_session())

    except KeyboardInterrupt:
        print("\nAborted.")
