import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import datetime

# Sayfa Genişliği
st.set_page_config(page_title="Global Mini-Discord", layout="wide")

# Google'ın STUN sunucuları (Farklı ağlardaki cihazların birbirini bulmasını sağlar)
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

st.title("🌐 Küresel Sesli Sohbet")

# Sol Panel
with st.sidebar:
    st.header("Profil")
    username = st.text_input("Kullanıcı Adı", value="Gezgin")
    st.divider()
    st.info("Bu linki arkadaşlarına göndererek onları davet edebilirsin!")

# --- SESLİ KANAL ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎙️ Sesli Kanal")
    webrtc_ctx = webrtc_streamer(
        key="discord-voice",
        mode=WebRtcMode.SENDRECV, # Hem gönder hem al
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": False, "audio": True}, # Sadece ses
        async_processing=True,
    )

# --- YAZILI MESAJLAR (BASİT VERİTABANI OLMADAN) ---
with col2:
    st.subheader("💬 Sohbet")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mesaj Kutusu
    chat_placeholder = st.empty()
    with chat_placeholder.container():
        for msg in st.session_state.messages:
            st.markdown(f"**{msg['user']}**: {msg['text']}")

    # Mesaj Gönderme
    if prompt := st.chat_input("Bir şeyler yaz..."):
        st.session_state.messages.append({"user": username, "text": prompt})
        st.rerun()