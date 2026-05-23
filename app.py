# -*- coding: utf-8 -*-
import streamlit as st
from pypdf import PdfReader
import requests
import json

st.set_page_config(page_title="CV Analizoru", layout="centered")
st.title("Yapay Zeka Destekli CV Analizoru")
st.write("CV yukleyin ve ise uygunlugunuzu analiz edin!")

is_tanimi = st.text_area("Is Tanimi:")
yuklenen_dosya = st.file_uploader("CV PDF olarak yukleyin", type=["pdf"])

if st.button("Analiz Et"):
    if is_tanimi and yuklenen_dosya:
        try:
            if "HF_TOKEN" not in st.secrets:
                st.error("API Anahtari bulunamadi!")
                st.stop()

            pdf_okuyucu = PdfReader(yuklenen_dosya)
            cv_metni = ""
            for sayfa in pdf_okuyucu.pages:
                metin = sayfa.extract_text() or ""
                cv_metni += metin

            komut = "Job Description: " + is_tanimi + "\n\nCV Text: " + cv_metni + "\n\nCreate a CV analysis report with compatibility score, strengths, weaknesses and improvement suggestions. Reply in the same language as the job description."

            payload = json.dumps({
                "model": "meta-llama/Meta-Llama-3-8B-Instruct",
                "messages": [{"role": "user", "content": komut}],
                "max_tokens": 1000
            }, ensure_ascii=False).encode("utf-8")

            headers = {
                "Authorization": "Bearer " + st.secrets["HF_TOKEN"],
                "Content-Type": "application/json; charset=utf-8"
            }

            response = requests.post(
                "https://router.
