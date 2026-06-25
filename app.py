import streamlit as st
import pandas as pd

# Sayfa ayarları
st.set_page_config(page_title="Gelişmiş Sineklik Hesaplayıcı", page_icon="🦟", layout="wide")

st.title("🦟 Sineklik Kesim Ölçüsü & Maliyet Hesaplayıcı")
st.write("Ölçüleri girip listeye ekleyerek toplu sipariş ve maliyet analizi oluşturabilirsiniz.")

# Hafıza (Session State) Tanımlamaları
if "siparisler" not in st.session_state:
    st.session_state.siparisler = []
    
# Fiyat çarpanının hafızada tutulması (Varsayılan: 540)
if "fiyat_carpani" not in st.session_state:
    st.session_state.fiyat_carpani = 540.0

# --- SIDEBAR: MALİYET ÇARPANI AYARI ---
st.sidebar.header("💰 Fiyat Ayarı")

# Onar onar artırma/azaltma butonları ve sayı girişi
col_eksi, col_arti = st.sidebar.columns(2)
with col_eksi:
    if st.button("➖ 10 Azalt"):
        st.session_state.fiyat_carpani -= 10
with col_arti:
    if st.button("➕ 10 Artır"):
        st.session_state.fiyat_carpani += 10

# Elle de değiştirilebilen giriş kutusu
st.session_state.fiyat_carpani = st.sidebar.number_input(
    "Maliyet Çarpanı:", 
    min_value=0.0, 
    value=float(st.session_state.fiyat_carpani), 
    step=10.0
)

# --- SIDEBAR: ÖLÇÜ GİRİŞİ ---
st.sidebar.markdown("---")
st.sidebar.header("📏 Yeni Ölçü Girişi")
pencere_adi = st.sidebar.text_input("Pencere / Konum Adı:", value=f"Pencere {len(st.session_state.siparisler) + 1}")
en = st.sidebar.number_input("En (cm):", min_value=0.0, value=60.0, step=1.0)
boy = st.sidebar.number_input("Boy (cm):", min_value=0.0, value=120.0, step=1.0)
adet = st.sidebar.number_input("Adet:", min_value=1, value=1, step=1)

# Listeye Ekleme Butonu ve Hesaplama Mantığı
if st.sidebar.button("📥 Listeye Ekle"):
    # Kesim Formülü Hesaplamaları
    yatay_kasa = en - 4.0
    dikey_kasa = boy - 7.8
    kanat = boy - 8.5
    tul_dikey = boy - 4.5
    tepe_sayisi = round((en * 25) / 60)
    
    # Dinamik Maliyet Formülü: (En + Boy) * Belirlenen Çarpan * Adet
    tekil_maliyet = (en + boy) * st.session_state.fiyat_carpani
    toplam_maliyet = tekil_maliyet * adet

    # Veriyi sözlük yapısında hafızaya ekleme
    yeni_siparis = {
        "Konum/Ad": pencere_adi,
        "En (cm)": en,
        "Boy (cm)": boy,
        "Adet": adet,
        "Yatay Kasa (cm)": round(yatay_kasa, 1),
        "Dikey Kasa (cm)": round(dikey_kasa, 1),
        "Kanat (cm)": round(kanat, 1),
        "Tül Dikey (cm)": round(tul_dikey, 1),
        "Tül Tepe (Adet)": tepe_sayisi,
        "Maliyet (TL)": round(toplam_maliyet, 2)
    }
    
    st.session_state.siparisler.append(yeni_siparis)
    st.toast(f"{pencere_adi} başarıyla listeye eklendi!", icon="✅")

# --- ANA EKRAN: SONUÇLAR VE TABLO ---
if st.session_state.siparisler:
    # Siparişleri Pandas DataFrame'e çeviriyoruz
    df = pd.DataFrame(st.session_state.siparisler)
    
    st.subheader("📊 Sipariş ve Kesim Listesi")
    st.dataframe(df, use_container_width=True)
    
    # Listeyi Temizleme Butonu
    if st.button("🗑️ Listeyi Temizle"):
        st.session_state.siparisler = []
        st.rerun()
        
    st.markdown("---")
    st.subheader("📈 Toplam Analiz")
    
    # Toplam Özet Hesaplamaları
    toplam_adet = int(df["Adet"].sum())
    genel_toplam_maliyet = df["Maliyet (TL)"].sum()
    
    # Özet Kartları
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Toplam Sineklik Adedi", value=f"{toplam_adet} Adet")
    with col2:
        st.metric(label="Genel Toplam Tutar", value=f"{genel_toplam_maliyet:,.2f} TL")
    
    st.caption(f"Hesaplamada kullanılan güncel çarpan: {st.session_state.fiyat_carpani} TL")

else:
    st.info("Henüz listeye eklenmiş bir sipariş bulunmuyor. Sol taraftaki menüyü kullanarak ölçü girebilirsiniz.")
