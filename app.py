import streamlit as st
import pandas as pd

# Sayfa ayarları (Sekme başlığı Kızılırmak Plise olarak güncellendi)
st.set_page_config(page_title="Kızılırmak Plise - Sineklik Hesaplayıcı", page_icon="🦟", layout="wide")

# Ana Başlık ve Marka Belirteci
st.title("🏭 Kızılırmak Plise")
st.subheader("🦟 Sineklik Kesim Ölçüsü & Maliyet Hesaplayıcı")
st.write("Ölçüleri girip listeye ekleyebilir, tablo üzerinde çift tıklayarak verileri **düzenleyebilir**, satırlara **tik atabilir** veya silebilirsiniz.")

# Hafıza (Session State) Tanımlamaları
if "siparisler" not in st.session_state:
    st.session_state.siparisler = []
    
# Fiyat çarpanının hafızada tutulması (Varsayılan: 540)
if "fiyat_carpani" not in st.session_state:
    st.session_state.fiyat_carpani = 540.0

# --- SIDEBAR: MALİYET ÇARPANI AYARI ---
st.sidebar.header("💰 Fiyat Ayarı")

col_eksi, col_arti = st.sidebar.columns(2)
with col_eksi:
    if st.button("➖ 10 Azalt"):
        st.session_state.fiyat_carpani -= 10
with col_arti:
    if st.button("➕ 10 Artır"):
        st.session_state.fiyat_carpani += 10

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
    # Formül hesaplamaları
    yatay_kasa = en - 4.0
    dikey_kasa = boy - 7.8
    kanat = boy - 8.5
    tul_dikey = boy - 4.5
    tepe_sayisi = round((en * 25) / 60)
    
    # Düzeltilen Maliyet Formülü
    toplam_maliyet = ((en + boy) * st.session_state.fiyat_carpani / 100.0) * adet

    # Veriyi sözlük yapısında hafızaya ekleme (Durum sütunu eklendi)
    yeni_siparis = {
        "Tamamlandı": False,  # İlk eklendiğinde tiksiz (False) başlar
        "Konum/Ad": pencere_adi,
        "En (cm)": en,
        "Boy (cm)": boy,
        "Adet": adet,
        "Yatay Kasa (cm)": round(yatay_kasa, 1),
        "Dikey Kasa (cm)": round(dikey_kasa, 1),
        "Kanat (cm)": round(kanat, 1),
        "Tül Dikey (cm)": round(tul_dikey, 1),
        "Tül Tepe (Adet)": tepe_sayisi,
        "Maliyet": round(toplam_maliyet, 2)
    }
    
    st.session_state.siparisler.append(yeni_siparis)
    st.toast(f"{pencere_adi} başarıyla listeye eklendi!", icon="✅")

# --- ANA EKRAN: SONUÇLAR VE DÜZENLENEBİLİR TABLO ---
if st.session_state.siparisler:
    # Siparişleri Pandas DataFrame'e çeviriyoruz
    df = pd.DataFrame(st.session_state.siparisler)
    
    # Sütun sırasını ayarlama ("Tamamlandı" sütununu en başa aldık)
    sutun_sirasi = ["Tamamlandı"] + [col for col in df.columns if col != "Tamamlandı"]
    df = df[sutun_sirasi]
    
    st.subheader("📊 Kızılırmak Plise Sipariş ve Kesim Listesi")
    st.info("💡 Üretimi biten sinekliklerin yanındaki **'Tamamlandı'** kutusuna tıklayarak tik atabilirsiniz. Ölçü değiştirmek için hücreye çift tıklayın.")
    
    # st.data_editor kullanarak tabloyu Excel gibi yapıyoruz
    editted_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic", 
        disabled=["Yatay Kasa (cm)", "Dikey Kasa (cm)", "Kanat (cm)", "Tül Dikey (cm)", "Tül Tepe (Adet)", "Maliyet"], 
        column_config={
            "Tamamlandı": st.column_config.CheckboxColumn(
                "Tamamlandı",
                help="Üretimi veya montajı bitenleri işaretleyin",
                default=False,
            ),
            "Maliyet": st.column_config.NumberColumn("Maliyet", format="%.2f TL")
        }
    )
    
    # --- DİNAMİK YENİDEN HESAPLAMA MANTIĞI ---
    if not editted_df.equals(df):
        editted_df =
