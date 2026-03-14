import streamlit as st
import instaloader
from fpdf import FPDF

st.set_page_config(page_title="Öz Bilgi Filtresi", page_icon="✨")

st.title("✨ Öz Bilgi ve Bolluk Aktarıcı")
st.write("Instagram linkini yapıştır, metni temizleyip PDF olarak al.")

# Link Girişi
url = st.text_input("Instagram Gönderi Linki:")

if st.button("Metni Çöz ve PDF Yap"):
    if url:
        try:
            with st.spinner('Bilgi ayıklanıyor...'):
                L = instaloader.Instaloader()
                # Linkten kısa kodu (shortcode) çekiyoruz
                shortcode = url.split("/")[-2]
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                
                # Metni al ve temizle
                raw_text = post.caption
                st.subheader("Bulunan Metin:")
                st.write(raw_text)

                # PDF Oluşturma
                pdf = FPDF()
                pdf.add_page()
                pdf.add_font('Arial', '', 'arial.ttf', uni=True) # Türkçe karakter desteği için
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt=raw_text)
                
                # İndirme Butonu
                pdf_output = pdf.output(dest='S').encode('latin-1', 'ignore')
                st.download_button(label="📥 PDF Olarak İndir", data=pdf_output, file_name="bilgi_notum.pdf")
                
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen bir link girin.")