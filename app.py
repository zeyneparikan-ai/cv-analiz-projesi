import streamlit as st
from pypdf import PdfReader
import requests

st.set_page_config(page_title="CV Analizoru", layout="centered")
st.title("Yapay Zeka Destekli CV Analizoru")
st.write("CV'nizi yukleyin ve ise uygunlugunuzu analiz edin!")

is_tanimi = st.text_area("Is Tanimi:")
yuklenen_dosya = st.file_uploader("CV'nizi PDF olarak yukleyin", type=["pdf"])

if st.button("Analiz Et"):
    if is_tanimi and yuklened_dosya:
        try:
            if "HF_TOKEN" not in st.secrets:
                st.error("API Anahtari bulunamadi!")
                st.stop()

            pdf_okuyucu = PdfReader(yuklened_dosya)
            cv_metni = ""
            for sayfa in pdf_okuyucu.pages:
                cv_metni += sayfa.extract_text() or ""

            komut = f"Job Description: {is_tanimi}\n\nCV Text: {cv_metni}\n\nCreate a CV analysis report with compatibility score, strengths, weaknesses and suggestions."

            headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}
            payload = {
                "model": "meta-llama/Meta-Llama-3-8B-Instruct",
                "messages": [{"role": "user", "content": komut}],
                "max_tokens": 1000
            }

            response = requests.post(
                "https://api-inference.huggingface.co/v1/chat/completions",
                headers=headers,
                json=payload
            )

            result = response.json()
            st.success("Analiz Tamamlandi!")
            st.markdown("### Analiz Raporu")
            st.write(result["choices"][0]["message"]["content"])

        except Exception as e:
            st.error(f"Hata: {e}")
    else:
        st.warning("Is tanimini girin ve CV yukleyin!")
