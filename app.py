import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os

# 1. Sayfa Konfigürasyonu
st.set_page_config(page_title="Bizim Discord", layout="wide", page_icon="🎙️")

# 2. Bağlantı Ayarları (Google STUN Sunucuları)
# Bu ayar, farklı ağlardaki insanların birbirine bağlanmasını sağlar.
RTC_CONFIG = RTCConfiguration(
    {"iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]}
    ]}
)

# 3. Mesajlaşma Altyapısı (Dosya Tabanlı)
DB_FILE = "chat_log.txt"

def mesaj_kaydet(kullanici, mesaj):
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(f"{kullanici}: {mesaj}\n")

def mesajlari_getir():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        return lines[-20:] # Sadece son 20 mesajı gösterir

# --- ARAYÜZ BAŞLIYOR ---

st.title("🎙️ Mini-Discord: Sesli ve Yazılı Sohbet")
st.divider()

# Ekranı ikiye bölüyoruz
sol_kolon, sag_kolon = st.columns([1, 1])

# --- SOL TARAF: SESLİ KANAL ---
with sol_kolon:
    st.header("🔊 Sesli Kanal")
    st.write("Aşağıdaki butona basarak odaya katılın.")
    
    # Kamerayı tamamen kapatıp sadece sesi açan bileşen
    webrtc_streamer(
        key="sesli-baglanti",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIG,
        # ÖNEMLİ: video: False yaparak kamera zorunluluğunu kaldırdık
        media_stream_constraints={
            "video": False,
            "audio": True
        },
        async_processing=True,
    )
    st.info("💡 Not: Ses gelmiyorsa arkadaşınızın da 'START' butonuna bastığından emin olun.")

# --- SAĞ TARAF: YAZILI SOHBET ---
with sag_kolon:
    st.header("💬 Mesajlar")
    
    # Kullanıcı adı girişi
    takma_ad = st.text_input("Kullanıcı Adın:", value="Anonim")
    
    # Mesajları görüntüleme alanı
    sohbet_alani = st.container(height=300, border=True)
    mesajlar = mesajlari_getir()
    for m in mesajlar:
        sohbet_alani.write(m.strip())
    
    # Mesaj gönderme kutusu
    yeni_mesaj = st.chat_input("Bir şeyler yaz...")
    if yeni_mesaj:
        mesaj_kaydet(takma_ad, yeni_mesaj)
        st.rerun() # Sayfayı hemen yenileyerek mesajı ekrana basar
