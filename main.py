import chainlit as cl
import requests

# Headers to avoid 451 error (if testing locally)
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Function to get price for a specific symbol
def get_coin_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            return res.json()
        return None
    except Exception as e:
        return {"error": str(e)}

# Function to get top 10 coins
def get_top_10():
    url = "https://api.binance.com/api/v3/ticker/price"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            return res.json()[:10]
        return None
    except Exception as e:
        return {"error": str(e)}

# Start message
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="💹 **Welcome to CoinPulse AI Crypto Agent!**\n\nType a symbol like `BTCUSDT` to get the live price, or type `TOP 10` to see the top coins.").send()

# On message from user
@cl.on_message
async def on_message(message: cl.Message):
    user_input = message.content.strip().upper()

    if user_input == "TOP 10":
        coins = get_top_10()
        if coins and isinstance(coins, list):
            text = "🔟 **Top 10 Coins by Symbol**\n"
            for coin in coins:
                text += f"• **{coin['symbol']}** = `{coin['price']} USDT`\n"
            await cl.Message(content=text).send()
        else:
            await cl.Message(content="❌ Failed to fetch top 10 coins.").send()

    elif user_input:
        coin = get_coin_price(user_input)
        if coin and "price" in coin:
            await cl.Message(content=f"💰 **{user_input}** price: `{coin['price']} USDT`").send()
        else:
            await cl.Message(content=f"⚠️ Symbol `{user_input}` not found or API failed. Try symbols like `BTCUSDT`, `ETHUSDT`.").send()
    else:
        await cl.Message(content="⚠️ Please enter a valid coin symbol.").send()
