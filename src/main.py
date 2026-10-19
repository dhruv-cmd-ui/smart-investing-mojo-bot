"""Orchestrator: pick content for a slot, render an image card, post to Telegram, persist rotation state."""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

from content_picker import load_state, pick_content, save_state  # noqa: E402
from render_image import render_card  # noqa: E402

DISCLAIMER = (
    "⚠️ Educational content only — not investment advice. Not a SEBI-registered "
    "advisor. Please consult a certified financial advisor before investing."
)

CHANNEL_TAG = "#SmartInvestingIndia"

LINKS_PATH = Path(__file__).resolve().parent.parent / "config" / "affiliate_links.json"


def load_affiliate_link(link_key: str | None) -> str | None:
    """Returns a usable affiliate URL for link_key, or None if missing/still a placeholder."""
    if not link_key:
        return None
    with open(LINKS_PATH, "r", encoding="utf-8") as f:
        links = json.load(f)
    url = links.get(link_key, "")
    if not url or "ADD_YOUR" in url:
        return None
    return url


def build_post(bank_name: str, item: dict):
    """Returns (category, heading, body, caption)."""
    heading = item["heading"]
    body = item["body"]
    category = bank_name

    caption_body = body if len(body) <= 600 else body[:597] + "..."
    caption = f"<b>{heading}</b>\n\n{caption_body}\n\n{DISCLAIMER}"

    link_url = load_affiliate_link(item.get("link_key"))
    if link_url:
        link_label = item.get("link_label", "Learn more")
        caption += f"\n\n🔗 {link_label} (affiliate link — we may earn a commission): {link_url}"

    caption += f"\n{CHANNEL_TAG}"
    if len(caption) > 1024:
        caption = caption[:1021] + "..."

    return category, heading, body, caption


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slot", required=True, choices=["morning", "evening"])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    state = load_state()
    bank_name, item = pick_content(args.slot, state)
    category, heading, body, caption = build_post(bank_name, item)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"out/{args.slot}_{category}_{timestamp}.png"
    render_card(category, heading, body, DISCLAIMER, out_path)

    print(f"[{args.slot}] bank={bank_name} category={category}")
    print(f"Heading: {heading}")
    print(f"Body:\n{body}")
    print(f"Caption:\n{caption}")
    print(f"Image saved to: {out_path}")

    if args.dry_run:
        print("Dry run — skipping Telegram post and state save.")
        return

    from telegram_client import send_photo

    send_photo(out_path, caption)
    save_state(state)
    print("Posted to Telegram and rotation state saved.")


if __name__ == "__main__":
    main()
