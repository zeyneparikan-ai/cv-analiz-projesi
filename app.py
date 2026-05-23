import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai

st.set_page_config(page_title="Yapay Zeka Destekli CV Analizörü", layout="centered")

st.title("🤖 Yapay Zeka Destekli CV Analizörü")
st.write("CV'nizi yükleyin ve hedeflediğiniz işe uygunluğunuzu analiz edin!")

is_tanimi = st.text_area("Hedeflediğiniz Pozisyonun Açıklaması / İş Tanımı:")
yuklenen_dosya = st.file_uploader("CV'nizi PDF formatında yükleyin", type=["pdf"])

if st.button("CV'yi Analiz Et ✨"):
    if is_tanimi and yuklenen_dosya:
        try:
            if "GEMINI_API_KEY" not in st.secrets:
                st.error("API Anahtarı bulunamadı!")
                st.stop()

            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

            pdf_okuyucu = PdfReader(yuklenen_dosya)
            cv_metni = ""
            for sayfa in pdf_okuyucu.pages:
                cv_metni += sayfa.extract_text() or ""

            komut = f"İş Tanımı: {is_tanimi}\n\nCV Metni: {cv_metni}\n\nYukarıdaki bilgilere göre bir CV analiz raporu oluştur. Uygunluk skoru, güçlü yönler, eksik yönler ve gelişim tavsiyelerini açıkla."

            model = genai.GenerativeModel(model_name='gemini-2.0-flash')
            cevap = model.generate_content(komut)

            st.success("Analiz Tamamlandı!")
            st.markdown("### 📄 Yapay Zeka Analiz Raporu")
            st.write(cevap.text)

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen hem iş tanımını girin hem de CV'nizi yükleyin!")
