import streamlit as st
import instaloader
from fpdf import FPDF
import pytesseract
from PIL import Image
import io

st.set_page_config(page_title="Öz Bilgi Filtresi", page_icon="✨")
st.title("✨ Öz Bilgi ve Bolluk Aktarıcı")

if 'extracted_text' not in st.session_state:
    st.session_state['extracted_text'] = ""

# --- SEÇENEK 1: INSTAGRAM LINKI ---
st.subheader("1. Yöntem: Instagram Linki ile (Hızlı)")
url = st.text_input("Instagram Gönderi Linkini Buraya Yapıştır:")

if st.button("🔗 Linkten Çöz"):
    try:
        L = instaloader.Instaloader()
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        st.session_state['extracted_text'] = post.caption
        st.success("Metin linkten başarıyla çekildi!")
    except Exception as e:
        st.error("Instagram erişimi kısıtladı. Lütfen 2. Yöntemi (Ekran Görüntüsü) kullanın.")

st.divider()

# --- SEÇENEK 2: EKRAN GÖRÜNTÜSÜ (GARANTİ) ---
st.subheader("2. Yöntem: Ekran Görüntüsü ile (Kesin Çözüm)")
uploaded_file = st.file_uploader("Kopyalayamadığın yazının ekran görüntüsünü yükle:", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    if st.button("👁️ Resimdeki Yazıyı Oku"):
        try:
            image = Image.open(uploaded_file)
            # OCR işlemi (Tesseract'ın Streamlit üzerinde kurulu olması gerekir)
            text = pytesseract.image_to_string(image, lang='tur')
            st.session_state['extracted_text'] = text
            st.success("Resimdeki yazı başarıyla okundu!")
        except Exception as e:
            st.error("OCR Hatası: Lütfen sistem yöneticisine danışın.")

st.divider()

# --- DÜZENLEME VE PDF ---
edited_text = st.text_area("Ayıklanan Metin (Düzenleyebilirsin):", value=st.session_state['extracted_text'], height=250)

if st.button("📄 PDF Dosyası Oluştur"):
    if edited_text:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12) # Standart font
        pdf.multi_cell(0, 10, txt=edited_text.encode('latin-1', 'ignore').decode('latin-1'))
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(label="📥 PDF'i İndir", data=pdf_output, file_name="oz_bilgi.pdf", mime="application/pdf")
