import streamlit as str
import google.generativeai as genai
import pypdf

# 1. YAPAY ZEKA AYARI
# Alttaki tırnak işaretlerinin içine kendi aldığın API anahtarını yapıştır!
API_KEY = "AIzaSyD9Ve3JUkTAx4T60G1upoMTrjf9NL3Ahyg"
genai.configure(api_key=API_KEY)

# 2. WEB SİTESİNİN BAŞLIĞI VE TASARIMI
str.set_page_config(page_title="AI Resume Analyzer", layout="centered")
str.title("🤖 Yapay Zeka Destekli CV Analizörü")
str.write("CV'nizi yükleyin ve hedeflediğiniz işe ne kadar uygun olduğunuzu yapay zeka analiz etsin!")

# 3. İŞ TANIMI GİRİŞ ALANI
is_tanimi = str.text_area("Hedeflediğiniz Pozisyonun Açıklaması / İş Tanımı:", placeholder="Örn: Python bilen, veri analitiği yapabilen stajyer aranıyor...")

# 4. DOSYA YÜKLEME ALANI
yuklenen_dosya = str.file_uploader("CV'nizi PDF formatında yükleyin", type=["pdf"])

# 5. İŞLEM BUTONU VE ARKA PLAN PLANI
if str.button("CV'yi Analiz Et ✨"):
    if yuklenen_dosya is not None and is_tanimi != "":
        with str.spinner("Yapay zeka CV'nizi inceliyor, lütfen bekleyin..."):
            try:
                # PDF dosyasındaki metinleri okuma
                pdf_okuyucu = pypdf.PdfReader(yuklenen_dosya)
                cv_metni = ""
                for sayfa in pdf_okuyucu.pages:
                    cv_metni += sayfa.extract_text()
                
                # Yapay zekaya gönderilecek komut (Prompt)
                komut = f"""
                Sen profesyonel bir İnsan Kaynakları (İK) yapay zeka asistanısın. 
                Aşağıdaki CV metnini, verilen İş Tanımı ile kıyasla.
                
                İş Tanımı: {is_tanimi}
                CV Metni: {cv_metni}
                
                Lütfen şu formatta bir analiz raporu çıkar:
                1. Uygunluk Skoru: (100 üzerinden bir puan ver)
                2. Güçlü Yönler: (Adayın bu işe uyan en iyi 3 özelliği)
                3. Eksik Yönler: (Adayın bu iş için geliştirmesi gereken veya CV'de eksik olan yönler)
                4. Gelişim Tavsiyeleri: (Adaya kariyer tavsiyeleri)
                """
                
                # Modeli çağırma ve çalıştırma
                model = genai.GenerativeModel('gemini-pro')
                cevap = model.generate_content(komut)
                
                # Sonucu ekrana yazdırma
                str.success("Analiz Tamamlandı!")
                str.markdown("### 📋 Yapay Zeka Analiz Raporu")
                str.write(cevap.text)
                
            except Exception as e:
                str.error(f"Bir hata oluştu: {e}")
    else:
        str.warning("Lütfen hem iş tanımını girin hem de CV'nizi yükleyin!")


