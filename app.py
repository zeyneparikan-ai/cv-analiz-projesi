import streamlit as st
from pypdf import PdfReader
import anthropic

st.set_page_config(page_title="Yapay Zeka Destekli CV Analizörü", layout="centered")

st.title("🤖 Yapay Zeka Destekli CV Analizörü")
st.write("CV'nizi yükleyin ve hedeflediğiniz işe uygunluğunuzu analiz edin!")

is_tanimi = st.text_area("Hedeflediğiniz Pozisyonun Açıklaması / İş Tanımı:")
yuklenen_dosya = st.file_uploader("CV'nizi PDF formatında yükleyin", type=["pdf"])

if st.button("CV'yi Analiz Et ✨"):
    if is_tanimi and yuklenen_dosya:
        try:
            if "ANTHROPIC_API_KEY" not in st.secrets:
                st.error("API Anahtarı bulunamadı!")
                st.stop()

            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

            pdf_okuyucu = PdfReader(yuklenen_dosya)
            cv_metni = ""
            for sayfa in pdf_okuyucu.pages:
                cv_metni += sayfa.extract_text() or ""

            komut = f"İş Tanımı: {is_tanimi}\n\nCV Metni: {cv_metni}\n\nYukarıdaki bilgilere göre bir CV analiz raporu oluştur. Uygunluk skoru, güçlü yönler, eksik yönler ve gelişim tavsiyelerini açıkla."

            cevap = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": komut}]
            )

            st.success("Analiz Tamamlandı!")
            st.markdown("### 📄 Yapay Zeka Analiz Raporu")
            st.write(cevap.content[0].text)

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen hem iş tanımını girin hem de CV'nizi yükleyin!")
         
