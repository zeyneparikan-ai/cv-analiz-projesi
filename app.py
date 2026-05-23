import streamlit as st
import os
from pypdf import PdfReader

# Sayfa Yapılandırması
st.set_page_config(page_title="Yapay Zeka Destekli CV Analizörü", layout="centered")

st.title("🤖 Yapay Zeka Destekli CV Analizörü")
st.write("CV'nizi yükleyin ve hedeflediğiniz işe uygunluğunuzu analiz edin!")

# Kullanıcı Girişleri
is_tanimi = st.text_area("Hedeflediğiniz Pozisyonun Açıklaması / İş Tanımı:")
yuklenen_dosya = st.file_uploader("CV'nizi PDF formatında yükleyin", type=["pdf"])

if st.button("CV'yi Analiz Et ✨"):
    if is_tanimi and yuklenen_dosya:
        try:
            # 1. API Anahtarı Kontrolü ve Yapılandırma
            if "GEMINI_API_KEY" not in st.secrets:
                st.error("API Anahtarı bulunamadı! Lütfen Streamlit Secrets kısmını kontrol edin.")
                st.stop()
            
            import google.generativeai as genai
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            
            # 2. PDF Okuma İşlemi
            pdf_okuyucu = PdfReader(yuklenen_dosya)
            cv_metni = ""
            for sayfa in pdf_okuyucu.pages:
                cv_metni += sayfa.extract_text() or ""
            
            # 3. Prompt Hazırlama
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
            
            # 4. Modeli Başlatma ve Yanıt Alma
            model = genai.GenerativeModel(
                model_name='models/gemini-1.5-flash'
            )
            
            cevap = model.generate_content(komut)
            
            st.success("Analiz Tamamlandı!")
            st.markdown("### 📄 Yapay Zeka Analiz Raporu")
            st.write(cevap.text)
            
            except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen hem iş tanımını girin hem de CV'nizi yükleyin!")
