import streamlit as st
import requests
import json
from pypdf import PdfReader

# Başlık
st.title("🤖 Yapay Zeka Destekli CV Analizörü")
st.write("CV'nizi yükleyin ve hedeflediğiniz işe ne kadar uygun olduğunuzu yapay zeka analiz etsin!")

# Kullanıcı Girişleri
is_tanimi = st.text_area("Hedeflediğiniz Pozisyonun Açıklaması / İş Tanımı:")
yuklenen_dosya = st.file_uploader("CV'nizi PDF formatında yükleyin", type=["pdf"])

if st.button("CV'yi Analiz Et ✨"):
    if is_tanimi and yuklenen_dosya:
        try:
            # Secrets kontrolü
            if "GEMINI_API_KEY" not in st.secrets:
                st.error("API Anahtarı bulunamadı! Lütfen Streamlit Secrets kısmını kontrol edin.")
            else:
                api_key = st.secrets["GEMINI_API_KEY"]
                
                # PDF okuma
                pdf_okuyucu = PdfReader(yuklenen_dosya)
                cv_metni = ""
                for sayfa in pdf_okuyucu.pages:
                    cv_metni += sayfa.extract_text() or ""
                
                # API için komut hazırlama
                komut = f"""
                Aşağıdaki iş tanımı ile CV metnini karşılaştır ve detaylı bir analiz raporu çıkar.
                
                İş Tanımı: {is_tanimi}
                CV Metni: {cv_metni}
                
                Lütfen şu formatta bir analiz raporu çıkar:
                1. Uygunluk Skoru: (100 üzerinden bir puan ver)
                2. Güçlü Yönler: (Adayın bu işe uyan en iyi 3 özelliği)
                3. Eksik Yönler: (Adayın bu iş için geliştirmesi gereken veya CV'de eksik olan noktalar)
                4. Gelişim Tavsiyeleri: (Adaya kariyer tavsiyeleri)
                """
                
                # Doğrudan HTTP Request ile Gemini Çağırma (Kütüphanesiz)
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={api_key}"
                headers = {'Content-Type': 'application/json'}
                data = {"contents": [{"parts": [{"text": komut}]}]}
                
                response = requests.post(url, headers=headers, json=data)
                
                if response.status_code == 200:
                    cevap_json = response.json()
                    analiz_sonucu = cevap_json['candidates'][0]['content']['parts'][0]['text']
                    
                    st.success("Analiz Tamamlandı!")
                    st.markdown("### 📋 Yapay Zeka Analiz Raporu")
                    st.write(analiz_sonucu)
                else:
                    st.error(f"Google API Hatası: {response.status_code} - {response.text}")
                    
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen hem iş tanımını girin hem de CV'nizi yükleyin!")


