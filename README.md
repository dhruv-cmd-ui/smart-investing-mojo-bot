# Stream 1 — Automated Investing/Deals Telegram Channel

A second, separate Telegram channel from your existing finance-tips bot. Same proven engine (GitHub Actions cron + JSON content banks + Pillow-rendered cards + Telegram Bot API), but a different angle: investing deep-dives, broker/app comparisons, book picks, deal alerts, and promotion of your own Stream 2 templates — with affiliate links woven in, unlike the purely-educational original bot.

## How it works

- `.github/workflows/post.yml` runs 08:45 IST (morning) and 19:15 IST (evening) — offset slightly from your existing bot's 08:30/19:00 so the two channels' GitHub Actions don't collide if you ever merge them into one repo later.
- Morning rotates `deep_dive` and `tool_reviews`; evening rotates `book_picks`, `deal_alerts`, and `template_promo`.
- `config/affiliate_links.json` holds your actual affiliate/referral URLs. Until you fill in a real link, any content item referencing that link_key posts WITHOUT the link line — nothing breaks, you just don't get the monetization line until you're approved.
- Every post keeps the same SEBI-educational disclaimer as your existing bot — no stock-specific buy/sell calls, ever.

## Setup — steps only you can do

### 1. Create a second Telegram channel + bot
Same process as your existing bot:
1. In Telegram: **New Channel** → name it (e.g. "Smart Investing India").
2. Message **@BotFather** → `/newbot` → get a token (this is a NEW bot, don't reuse the old one).
3. Add the bot as admin on the new channel with **Post Messages** permission.
4. Get the channel's `@username` (public) or numeric ID via `@userinfobot` (private).

### 2. Create a new GitHub repo and push this folder
```
git remote add origin https://github.com/<your-username>/<new-repo>.git
git branch -M main
git push -u origin main
```
Add repo secrets: **Settings → Secrets and variables → Actions**:
- `TELEGRAM_BOT_TOKEN` — the new bot's token
- `TELEGRAM_CHANNEL_ID` — the new channel's ID

### 3. Sign up for affiliate programs (optional, do this whenever — content works fine without it)
Each has its own approval process; none cost anything to apply:
- **Amazon Associates India** — associates.amazon.in — apply with your Telegram channel as your "site." Approval can take a few days and sometimes requires your first qualifying sale within 180 days to stay active.
- **Groww / Zerodha / INDmoney referral programs** — each has an in-app or website "refer & earn" section; sign up as a user first, then look for the referral/partner link.
- **Cuelinks** — cuelinks.com — a single affiliate network that gives you deal links across many Indian merchants (easier than applying to each merchant separately).

Once approved, replace the placeholder values in `config/affiliate_links.json` (keep the `ADD_YOUR_...` style keys, just change the values) and push — no code changes needed.

### 4. Test it
**Actions → Post to Telegram → Run workflow** → confirm a post lands in the new channel, then let the cron schedule take over.

## Local testing

```
pip install -r requirements.txt
cp .env.example .env   # fill in the new bot token + channel id
python src/main.py --slot morning --dry-run
python src/main.py --slot evening --dry-run
```

## Adding more content later

Add entries to any `content/*.json` file (same `heading`/`body`/optional `link_key`/`link_label` shape) and push — the rotation picks them up automatically, no code changes.
