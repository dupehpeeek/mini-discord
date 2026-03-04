import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os

# Sayfa Ayarları
st.set_page_config(page_title="Bizim Discord", layout="wide")

# Daha güçlü STUN/TURN Sunucuları (Bağlantı sorunu için)
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]},
        {"urls": ["stun:stun2.l.google.com:19302"]}
    ]}
)

# --- MESAJLARI ORTAKLAŞTIRMA (Basit Dosya Sistemi) ---
DB_FILE = "chat_log.txt"

def save_message(user, text):
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(f"{user}: {text}\n")

def load_messages():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return f.readlines()

# --- ARAYÜZ ---
st.title("🌐 Ortak Sesli & Yazılı Kanal")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎙️ Sesli Bağlantı")
    st.info("Start'a basınca mikrofonun açılır. Arkadaşın da basmalı!")
    webrtc_streamer(
        key="global-audio",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": False, "audio": True},
    )

with col2:
    st.subheader("💬 Sohbet Geçmişi")
    username = st.text_input("Adın:", value="User", key="user_name")
    
    # Mesajları yükle ve göster
    messages = load_messages()
    chat_box = st.container(height=300)
    for m in messages:
        chat_box.write(m.strip())

    if prompt := st.chat_input("Mesajını yaz..."):
        save_message(username, prompt)
        st.rerun() # Sayfayı yenile ki mesaj hemen gelsin
