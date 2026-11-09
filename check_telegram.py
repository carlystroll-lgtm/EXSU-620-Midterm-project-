"""Run locally in a terminal; never paste a bot token into a chat."""
import argparse
import getpass
import json
import socket
import urllib.error
import urllib.parse
import urllib.request


class TelegramError(Exception):
    pass


def api(token, method, **fields):
    payload = urllib.parse.urlencode(fields).encode("utf-8")
    request = urllib.request.Request(
        "https://api.telegram.org/bot" + token + "/" + method,
        data=payload, method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        # Never print exceptions or URLs: they may contain the token.
        hints = {
            401: "Token rejected. Generate a fresh token in BotFather.",
            404: "Token or API request rejected. Check the fresh token.",
            409: "Update conflict. Stop other bot pollers and check webhook status.",
            403: "Access forbidden. For sending, start/unblock the bot in Telegram.",
            400: "Request rejected. For sending, check the numeric chat ID.",
            429: "Rate limited. Wait before trying again.",
        }
        raise TelegramError(hints.get(error.code, "Telegram HTTP error %s." % error.code)) from None
    except (urllib.error.URLError, TimeoutError, socket.timeout):
        raise TelegramError("Connection failed or timed out. Check internet, VPN/proxy, firewall, and Python certificates.") from None
    except (ValueError, OSError):
        raise TelegramError("Could not read Telegram's response.") from None
    if not result.get("ok"):
        raise TelegramError("Telegram rejected the request; no secret response details printed.")
    return result["result"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--remove-webhook", action="store_true", help="explicitly remove an existing webhook, retaining queued updates")
    parser.add_argument("--test-chat", help="send one clearly labeled test message to this numeric chat ID")
    args = parser.parse_args()
    print("Starting Telegram check...", flush=True)
    print("Use a NEW token generated after revoking the exposed token. It will not be saved.")
    token = getpass.getpass("Paste the NEW token here (input hidden): ").strip()
    if not token or any(c.isspace() for c in token) or ":" not in token:
        raise TelegramError("Missing or malformed token. Paste only the fresh token.")
    print("Checking bot identity (12-second network timeout)...", flush=True)
    identity = api(token, "getMe")
    print("Authenticated bot: @" + identity.get("username", "unknown"))
    print("Checking webhook...", flush=True)
    webhook = api(token, "getWebhookInfo")
    if webhook.get("url"):
        if not args.remove_webhook:
            raise TelegramError("A webhook is active and blocks getUpdates. If this bot should use polling, rerun with --remove-webhook. This disables its webhook integration.")
        api(token, "deleteWebhook", drop_pending_updates="false")
        print("Webhook removed; queued updates retained.")
    if args.test_chat:
        try:
            int(args.test_chat)
        except ValueError:
            raise TelegramError("--test-chat needs a numeric chat ID.") from None
        api(token, "sendMessage", chat_id=args.test_chat, text="EXSU 620: Telegram notification test.")
        print("Telegram accepted the test message. Check your phone and notification settings.")
        return
    input("Open the authenticated bot above, tap Start, send hello NOW, then press Enter here: ")
    print("Checking incoming messages...", flush=True)
    updates = api(token, "getUpdates", timeout=0, allowed_updates=json.dumps(["message"]))
    chats = {}
    for update in updates:
        chat = update.get("message", {}).get("chat")
        if chat:
            chats[chat["id"]] = chat.get("type", "unknown")
    for chat_id, kind in chats.items():
        print("Chat ID:", chat_id, "Type:", kind)
    if not chats:
        print("No chat messages returned. Confirm the bot username, send another fresh message, stop other pollers, then rerun. Empty results do not mean the token is invalid.")
    else:
        print("Use your private chat ID for your own phone. Test with --test-chat CHAT_ID.")


if __name__ == "__main__":
    try:
        main()
    except TelegramError as error:
        print("ERROR:", error, flush=True)
        raise SystemExit(1)
    except (KeyboardInterrupt, EOFError):
        print("\nStopped. Run this script in an interactive terminal.")
        raise SystemExit(1)
