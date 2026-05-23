import streamlit as st
from pypdf import PdfReader
from huggingface_hub import InferenceClient

st.set_page_config(page_title="Yapay Zeka Destekli CV Analizörü", layout="centered")

st.title("🤖 Yapay Zeka Destekli CV Analizörü")
st.write("CV'nizi yükleyin ve hedeflediğiniz işe uygunluğunuzu analiz edin!")

is_tanimi = st.text_area("Hedeflediğiniz Pozisyonun Açıklaması / İş Tanımı:")
yuklenen_dosya = st.file_uploader("CV'nizi PDF formatında yükleyin", type=["pdf"])

if st.button("CV'yi Analiz Et ✨"):
    if is_tanimi and yuklenen_dosya:
        try:
            if "HF_TOKEN" not in st.secrets:
                st.error("API Anahtarı bulunamadı!")
                st.stop()

            client = InferenceClient(
                provider="novita",
                api_key=st.secrets["HF_TOKEN"],
                headers={"Content-Type": "application/json; charset=utf-8"}
            )

            pdf_okuyucu = PdfReader(yuklenen_dosya)
            cv_metni = ""
            for sayfa in pdf_okuyucu.pages:
                cv_metni += sayfa.extract_text() or ""

            komut = f"Is Tanimi: {is_tanimi}\n\nCV Metni: {cv_metni}\n\nYukarıdaki bilgilere göre bir CV analiz raporu oluştur. Uygunluk skoru, güçlü yönler, eksik yönler ve gelişim tavsiyelerini açıkla."

            cevap = client.chat.completions.create(
                model="meta-llama/llama-3.3-70b-instruct",
                messages=[{"role": "user", "content": komut}],
                max_tokens=1000
            )

            st.success("Analiz Tamamlandı!")
            st.markdown("### 📄 Yapay Zeka Analiz Raporu")
            st.write(cevap.choices[0].message.content)

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen hem iş tanımını girin hem de CV'nizi yükleyin!")
