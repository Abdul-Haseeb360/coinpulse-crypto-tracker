import chainlit as cl
import requests
import re

# -----------------------------------------
# 🔧 Global Config
# -----------------------------------------
HEADERS = {"User-Agent": "Mozilla/5.0"}
BINANCE_PRICE_URL = "https://api.binance.com/api/v3/ticker/price"
BINANCE_24H_URL = "https://api.binance.com/api/v3/ticker/24hr"


# -----------------------------------------
# 🔹 Get price of a specific coin
# -----------------------------------------
def get_coin_price(symbol):
    url = f"{BINANCE_PRICE_URL}?symbol={symbol}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            return res.json()
        return None
    except Exception as e:
        return {"error": str(e)}


# -----------------------------------------
# 🔹 Get top 10 coins (basic)
# -----------------------------------------
def get_top_10():
    try:
        res = requests.get(BINANCE_PRICE_URL, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            return res.json()[:10]
        return None
    except Exception as e:
        return {"error": str(e)}


# -----------------------------------------
# 🔥 NEW: Get Top Gainers (Top 10 by % change)
# -----------------------------------------
def get_top_gainers():
    try:
        res = requests.get(BINANCE_24H_URL, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            return None

        data = res.json()

        # Sort by priceChangePercent DESC
        sorted_coins = sorted(
            data,
            key=lambda x: float(x["priceChangePercent"]),
            reverse=True
        )

        return sorted_coins[:10]

    except Exception as e:
        return {"error": str(e)}


# 🔻 Get Top 3 Losers (coins with biggest negative % change in 24h)
def get_top_3_losers():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            return None

        data = res.json()

        # Filter coins which actually have negative change
        losers = [coin for coin in data if float(coin["priceChangePercent"]) < 0]

        # Sort most negative → least negative
        losers_sorted = sorted(losers, key=lambda x: float(x["priceChangePercent"]))

        return losers_sorted[:3]  # top 3 losers
    except Exception as e:
        return {"error": str(e)}



def extract_number(text):
    """Extracts the first number from a user message."""
    match = re.search(r'\b\d+\b', text)
    return int(match.group()) if match else None


# -----------------------------------------
# 🚀 Chat Start Message
# -----------------------------------------
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content=(
            "💹 **Welcome to CoinPulse AI Crypto Agent!**\n\n"
            "You can ask:\n"
            "• `BTCUSDT` → Get live price\n"
            "• `TOP 10` → Top 10 coins\n"
            "• `GAINERS` → 🔥 Top 10 gaining coins\n"
        )
    ).send()


# -----------------------------------------
# 💬 Message Handler
# -----------------------------------------
@cl.on_message
@cl.on_message
async def on_message(message: cl.Message):
    user_text = message.content.strip()
    user_upper = user_text.upper()

    # ---------------------------------
    # Detect numbers for dynamic count
    # ---------------------------------
    count = extract_number(user_text) or 10  # default = 10

    # ---------------------------------
    # Natural Language: LOSERS (24h)
    # ---------------------------------
    if "LOSER" in user_upper or "LOSS" in user_upper or "TOP" in user_upper and "LOSS" in user_upper:
        losers = get_top_3_losers()

        if losers and isinstance(losers, list):
            losers = losers[:count]

            text = f"📉 **Top {count} Losers (24h)**\n\n"
            for coin in losers:
                text += (
                    f"• **{coin['symbol']}** — "
                    f"Change: `{coin['priceChangePercent']}%`\n"
                )

            await cl.Message(content=text).send()
        else:
            await cl.Message(content="❌ Failed to fetch top losers.").send()
        return

    # ---------------------------------
    # Natural Language: Gainers
    # ---------------------------------
    if "GAINER" in user_upper or ("TOP" in user_upper and "GAIN" in user_upper):
        gainers = get_top_gainers()

        if gainers and isinstance(gainers, list):
            gainers = gainers[:count]

            text = f"📈 **Top {count} Gainers (24h)**\n\n"
            for coin in gainers:
                text += (
                    f"• **{coin['symbol']}** — "
                    f"Change: `{coin['priceChangePercent']}%`\n"
                )

            await cl.Message(content=text).send()
        else:
            await cl.Message(content="❌ Failed to fetch top gainers.").send()
        return

    # ---------------------------------
    # Hard command: TOP 10
    # ---------------------------------
    if user_upper == "TOP 10":
        coins = get_top_10()
        if coins and isinstance(coins, list):
            text = "🔟 **Top 10 Coins by Symbol**\n"
            for coin in coins:
                text += f"• **{coin['symbol']}** = `{coin['price']} USDT`\n"
            await cl.Message(content=text).send()
        else:
            await cl.Message(content="❌ Failed to fetch top 10 coins.").send()
        return

    # ---------------------------------
    # Specific Coin Price
    # ---------------------------------
    coin = get_coin_price(user_upper)
    if coin and "price" in coin:
        await cl.Message(
            content=f"💰 **{user_upper}** price: `{coin['price']} USDT`"
        ).send()
        return

    # ---------------------------------
    # Invalid Input
    # ---------------------------------
    await cl.Message(
        content="⚠️ I didn't understand your request. Try symbols like `BTCUSDT`, or say: `Give me the top 3 losers`."
    ).send()
