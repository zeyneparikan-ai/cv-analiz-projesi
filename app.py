import streamlit as st
import requests
from pypdf import PdfReader

# --- SAYFA AYARLARI VE BAŞLIK ---
st.set_page_config(page_title="CV Analiz Projesi", page_icon="📄", layout="centered")
st.title("📄 Yapay Zeka Destekli CV Analiz Assistanı")

# --- KULLANICI GİRDİLERİ ---
is_tanimi = st.text_area("İş Tanımını (Job Description) Buraya Yapıştırın:", height=150)
yuklenen_dosya = st.file_uploader("CV'nizi PDF formatında yükleyin:", type=["pdf"])

# --- ANALİZ SÜRECİ ---
if yuklenen_dosya and is_tanimi:
    if st.button("CV'yi Analiz Et"):
        with st.spinner("CV okunuyor ve analiz ediliyor..."):
            try:
                # 1. PDF Okuma İşlemi
                pdf_okuyucu = PdfReader(yuklenen_dosya)
                cv_metni = ""
                for sayfa in pdf_okuyucu.pages:
                    metin = sayfa.extract_text() or ""
                    cv_metni += metin + "\n"  # Sayfa geçişlerinde boşluk bırakıyoruz
                
                # 2. Prompt (Komut) Hazırlama
                komut = f"Job Description: {is_tanimi}\n\nCV Text: {cv_metni}\n\nCreate a CV analysis"
                
                # 3. API Payload Yapılandırması
                payload = {
                    "model": "meta-llama/Meta-Llama-3-8B-Instruct",
                    "messages": [{"role": "user", "content": komut}],
                    "max_tokens": 1000
                }
                
                # 4. API Anahtarı Temizliği (Latin-1/Türkçe karakter hatasını önlemek için)
                hf_token = str(st.secrets["HF_TOKEN"]).strip()
                
                headers = {
                    "Authorization": f"Bearer {hf_token}"
                }
                
                # 5. Hugging Face Router API İsteği
                response = requests.post(
                    "https://router.huggingface.co/v1/chat/completions",
                    headers=headers,
                    json=payload  # Veriyi güvenli JSON formatında gönderiyoruz
                )
                
                # 6. Yanıtı Ekrana Yazdırma
                if response.status_code == 200:
                    sonuc = response.json()
                    analiz_metni = sonuc["choices"][0]["message"]["content"]
                    
                    st.success("Analiz Başarıyla Tamamlandı!")
                    st.subheader("📊 Analiz Sonuçları")
                    st.write(analiz_metni)
                else:
                    st.error(f"API Hatası Oluştu! Kod: {response.status_code}")
                    st.error(response.text)
                    
            except Exception as e:
                st.error(f"Bir hata meydana geldi: {e}")

else:
    st.info("Lütfen analize başlamak için hem iş tanımını girin hem de CV'nizi yükleyin.")
