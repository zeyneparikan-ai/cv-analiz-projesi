import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="CV Analizörü", page_icon="🤖")

st.title("🤖 Yapay Zeka Destekli CV Analizörü")
st.write("CV'nizi yükleyin ve hedeflediğiniz işe uygunluğunuzu analiz edin!")

# Kullanıcı Girişleri
is_tanimi = st.text_area("Hedeflediğiniz Pozisyonun Açıklaması / İş Tanımı:")
yuklenen_dosya = st.file_uploader("CV'nizi PDF formatında yükleyin", type=["pdf"])

if st.button("CV'yi Analiz Et ✨"):
    if is_tanimi and yuklenen_dosya:
        try:
            # Secrets kontrolü ve API Yapılandırması
            if "GEMINI_API_KEY" not in st.secrets:
                st.error("API Anahtarı bulunamadı! Lütfen Streamlit Secrets kısmını kontrol edin.")
            else:
                # En güncel yapılandırma metodu
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                
                # PDF okuma işlemi
                pdf_okuyucu = PdfReader(yuklenen_dosya)
                cv_metni = ""
                for sayfa in pdf_okuyucu.pages:
                    cv_metni += sayfa.extract_text() or ""
                
                # Prompt hazırlama
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
                
                # KÖKDEN ÇÖZÜM: API Sürümünü v1'e (Stabil) zorlayarak modeli başlatıyoruz
            os.environ["DEFAULT_API_VERSION"] = "v1"
                    model = genai.GenerativeModel("models/gemini-1.5-flash")
                cevap = model.generate_content(komut)
                
                st.success("Analiz Tamamlandı!")
                st.markdown("### 📝 Yapay Zeka Analiz Raporu")
                st.write(cevap.text)
                
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen hem iş tanımını girin hem de CV'nizi yükleyin!")
