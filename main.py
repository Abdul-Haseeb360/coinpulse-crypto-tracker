import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(page_title="📈 CoinPulse - Live Crypto Tracker", page_icon="", layout="centered")

# --- Styling ---
st.markdown("""
    <style>
        .main-title {
            font-size: 32px;
            font-weight: bold;
            color: #3F51B5;
        }
        .subtext {
            font-size: 16px;
            color: #555;
        }
        .btn-row {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)


st.title("💹 CoinPulse Live Crypto Agent")
st.markdown("Type a coin symbol like `BTCUSDT` or click below to get **Top 10 coin prices**.")

# --- User Inputs ---
user_input = st.text_input("🔎 Enter a Coin Symbol (e.g., BTCUSDT)", "")

col1, col2 = st.columns(2)
with col1:
    top_button = st.button("🔟 Get Top 10 Coins")
with col2: 
    live_button = st.button("💰 Get Live Price")

# --- Helper Functions ---
headers = {"User-Agent": "Mozilla/5.0"}

def get_coin_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        st.text(f"Debug: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.text(f"Error: {e}")
        return None

def get_top_10():
    url = "https://api.binance.com/api/v3/ticker/price"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        st.text(f"Top Debug: {response.status_code}")
        if response.status_code == 200:
            return response.json()[:10]
        return None
    except Exception as e:
        st.text(f"Top Error: {e}")
        return None


# --- Actions ---
if top_button:
    st.subheader("🔝 Top 10 Coins")
    data = get_top_10()
    if data:
        for item in data:
            st.write(f"**{item['symbol']}**: {item['price']} USDT")
    else:
        st.error("❌ Could not fetch top coins. Check your connection.")

if live_button:
    symbol = user_input.strip().upper()
    if not symbol:
        st.warning("⚠️ Please enter a coin symbol before clicking Get Live Price.")
    else:
        st.subheader(f"📈 Live Price for `{symbol}`")
        data = get_coin_price(symbol)
        if data:
             st.success(f" **{symbol}**: {data['price']} USDT")
        else:
            st.error("⚠️ Invalid symbol or problem with Binance API.")
            



st.markdown("---")
st.markdown(" 📈 **CoinPulse – Live Crypto Tracker AI** &copy; 2025 | Built with ❤️ using Streamlit")
st.markdown(
    "📧 Contact: `abdulhaseebshaikh1234@gmail.com` | 🔗 [GitHub](https://github.com/Abdul-Haseeb360)")
