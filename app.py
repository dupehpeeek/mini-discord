import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os

# Sayfa Ayarları
st.set_page_config(page_title="Bizim Discord", layout="wide")

# Kararlı STUN Sunucuları
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# --- MESAJ SİSTEMİ ---
DB_FILE = "chat_log.txt"

def save_message(user, text):
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(f"{user}: {text}\n")

def load_messages():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return f.readlines()[-20:] # Sadece son 20 mesajı göster (hız için)

# --- ARAYÜZ ---
st.title("🎙️ Ortak Sesli Sohbet")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Sesli Kanal")
    # Hatalı parametreler temizlendi
    webrtc_streamer(
        key="voice-chat",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": False, "audio": True},
    )

with col2:
    st.subheader("Yazılı Sohbet")
    username = st.text_input("Adın:", value="User", key="chat_user")
    
    # Mesajları oku
    messages = load_messages()
    for m in messages:
        st.write(m.strip())

    if prompt := st.chat_input("Mesaj yaz..."):
        save_message(username, prompt)
        st.rerun()
