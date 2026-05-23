# PDF metnini daha efektif bir şekilde birleştiriyoruz
pdf_okuyucu = PdfReader(yuklenen_dosya)
cv_metni = ""
for sayfa in pdf_okuyucu.pages:
    metin = sayfa.extract_text() or ""
    cv_metni += metin + "\n"  # Sayfalar arasına boşluk bırakmak iyi bir pratiktir

# Prompt tanımı
komut = f"Job Description: {is_tanimi}\n\nCV Text: {cv_metni}\n\nCreate a CV analysis"

# Payload'u ham bir Python dict (sözlük) olarak bırakıyoruz
payload = {
    "model": "meta-llama/Meta-Llama-3-8B-Instruct",
    "messages": [{"role": "user", "content": komut}],
    "max_tokens": 1000
}

# Header'lar (Content-Type'ı requests kendisi halledecek)
headers = {
    "Authorization": f"Bearer {st.secrets['HF_TOKEN']}"
}

# İsteği json= parametresi ile gönderiyoruz
response = requests.post(
    "https://router.huggingface.co/v1/chat/completions",
    headers=headers,
    json=payload  # data=payload yerine json=payload
)
