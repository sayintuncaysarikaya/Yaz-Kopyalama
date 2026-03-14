import streamlit as st
import instaloader
from fpdf import FPDF

st.set_page_config(page_title="Öz Bilgi Filtresi", page_icon="✨")

st.title("✨ Öz Bilgi ve Bolluk Aktarıcı")

# Link Girişi
url = st.text_input("Instagram Gönderi Linki:")

# Uygulama Hafızası (Session State) - Metni butonlar arasında taşımak için
if 'extracted_text' not in st.session_state:
    st.session_state['extracted_text'] = ""

# 1. BUTON: Sadece Metni Çek
if st.button("🔍 Sadece Metni Çöz"):
    if url:
        try:
            with st.spinner('Bilgi ayıklanıyor...'):
                L = instaloader.Instaloader()
                shortcode = url.split("/")[-2]
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                st.session_state['extracted_text'] = post.caption
                st.success("Metin başarıyla çekildi!")
        except Exception as e:
            st.error(f"Hata: {e}")
    else:
        st.warning("Lütfen bir link girin.")

# Metin Alanı (Kullanıcı burada metni düzenleyebilir)
edited_text = st.text_area("Ayıklanan Metin (Düzenleyebilirsin):", value=st.session_state['extracted_text'], height=300)

# 2. BUTON: Düzenlenmiş Metni PDF Yap
if st.button("📄 PDF Olarak Hazırla"):
    if edited_text:
        pdf = FPDF()
        pdf.add_page()
        # Türkçe karakter desteği için standart font yerine 'Arial' kullanıyoruz
        pdf.set_font("Arial", size=12)
        
        # PDF içeriğini oluştur
        pdf.multi_cell(0, 10, txt=edited_text.encode('latin-1', 'ignore').decode('latin-1'))
        
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(label="📥 PDF'i Şimdi İndir", data=pdf_output, file_name="oz_bilgi_notum.pdf", mime="application/pdf")
    else:
        st.info("Önce metni çözmelisin veya buraya bir şeyler yazmalısın.")
