import streamlit as st
from pypdf import PdfReader
from huggingface_hub import InferenceClient

st.set_page_config(page_title="Yapay Zeka Destekli CV Analizoru", layout="centered")

st.title("Yapay Zeka Destekli CV Analizoru")
st.write("CV'nizi yukleyin ve hedeflediginiz ise uygunlugunuzu analiz edin!")

is_tanimi = st.text_area("Hedeflediginiz Pozisyonun Aciklamasi / Is Tanimi:")
yuklenen_dosya = st.file_uploader("CV'nizi PDF formatinda yukleyin", type=["pdf"])

if st.button("CV'yi Analiz Et"):
    if is_tanimi and yuklenen_dosya:
        try:
            if "HF_TOKEN" not in st.secrets:
                st.error("API Anahtari bulunamadi!")
                st.stop()

            client = InferenceClient(
                provider="novita",
                api_key=st.secrets["HF_TOKEN"]
            )

            pdf_okuyucu = PdfReader(yuklenen_dosya)
            cv_metni = ""
            for sayfa in pdf_okuyucu.pages:
                metin = sayfa.extract_text() or ""
                cv_metni += metin.encode("ascii", "ignore").decode("ascii")

            is_tanimi_ascii = is_tanimi.encode("ascii", "ignore").decode("ascii")

            komut = f"Job Description: {is_tanimi_ascii}\n\nCV Text: {cv_metni}\n\nCreate a CV analysis report. Include compatibility score, strengths, weaknesses and improvement suggestions."

            cevap = client.chat.completions.create(
                model="meta-llama/llama-3.3-70b-instruct",
                messages=[{"role": "user", "content": komut}],
                max_tokens=1000
            )

            st.success("Analiz
