import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import os

# Sayfa Genişliği
st.set_page_config(page_title="Bizim Discord", layout="wide")

# Kararlı Sunucu Ayarları
RTC_CONFIG = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# --- MESAJLAŞMA SİSTEMİ ---
DB_FILE = "chat.txt"

def save_msg(u, t):
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(f"{u}: {t}\n")

def get_msgs():
    if not os.path.exists(DB_FILE): return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return f.readlines()[-15:]

# --- ARAYÜZ ---
st.title("🎙️ Ortak Sohbet Odası")

c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("Sesli Kanal")
    # Hataya sebep olan 'mode' ve 'constraints' parametrelerini en sade haline getirdik
    webrtc_streamer(
        key="voice",
        rtc_configuration=RTC_CONFIG,
        video_html_attrs={"style": {"display": "none"}}, # Görüntüyü gizle
    )
    st.caption("START butonuna basın ve mikrofon izni verin.")

with c2:
    st.subheader("Yazışma")
    name = st.text_input("Adın:", "User")
    
    # Mesajları göster
    for m in get_msgs():
        st.text(m.strip())

    if txt := st.chat_input("Mesaj yaz..."):
        save_msg(name, txt)
        st.rerun()
