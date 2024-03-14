import pandas as pd
import streamlit as st
import openai
import os


from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud



def main():
    st.title("Miuul Discord Destek Kanalı İçin Analiz Uygulaması")

    st.subheader("OpenAI API Anahtarınızı Girin")
    api_key = st.text_input("OpenAI API Anahtarı")

    if api_key:
        openai.api_key = api_key
        st.success("API anahtarı girişi yapıldı.")

        st.sidebar.header("Analiz etmek istediğiniz CSV dosyalarını ekleyin")
        #on = st.toggle('Soruları gör')

        uploaded_files = st.sidebar.file_uploader("CSV dosyası yükle", type="csv", accept_multiple_files=True)

        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                kurs_adi, _ = os.path.splitext(uploaded_file.name)
                dosya_adi = uploaded_file.name
                df = pd.read_csv(uploaded_file, sep="~")
                mentor=["gamzeakmannn","klncgty","pinarkilic","handekucukbulut","sebnemgurek"]
                df = df[~df["username"].isin(mentor)]
                df["time_stamp"] = pd.to_datetime(df["time_stamp"])
                df["tarih"] = df["time_stamp"].dt.date
                df["saat"] = df["time_stamp"].dt.time
                df['tarih'] = pd.to_datetime(df['tarih'])
                df.set_index('tarih', inplace=True)
                monthly_message_count = df.resample('M').size()
                st.markdown("AYLARA GÖRE MESAJ SAYISI")
                st.bar_chart(monthly_message_count, use_container_width=True)
                df.drop("time_stamp", axis=1, inplace=True)
                en_aktif_kullanıcı = df["username"].value_counts().idxmax()
                # her kullanıcı için mesajları birleştir
                df['message_content'] = df['message_content'].astype(str)

                # Her kullanıcı adı için mesaj içeriklerini birleştirelim
                df_grup = df.groupby('username')['message_content'].apply(lambda x: ' '.join(x)).reset_index()

                with st.spinner("Analiz başladı"):
                    st.subheader(f" {dosya_adi} dosyasını tarıyorum  :sunglasses:", divider="orange")
                    st.text(f" {kurs_adi} kanalındaki en aktif kullanıcı ----> {en_aktif_kullanıcı} ")
                    
                    evet_cümleleri = []
                    soru_sayisi = 0
                
                    for row in df_grup["message_content"]:
                        ### Boş değerleri kontrol ett
                        if isinstance(row, str):  # eğer normal istediğimiz gibi bir string ise devam et
                            cumleler = row.split(",")
                            for cumle in cumleler:
                                siniflandirma = openai.ChatCompletion.create(
                                    model="gpt-4",
                                    messages=[{"role": "system",
                                        "content": f"Anlam olarak, '{cumle}' bu cümle bir soru mu? Eğer öyleyse, sadece 'Evet' şeklinde cevap ver."}],
                                    max_tokens=4000,
                                    temperature=0.4,
                                    n=1,
                                    frequency_penalty=0.9,
                                    presence_penalty=0.0
                                )
                                if siniflandirma.choices[0].message.content == "Evet":
                                    soru_sayisi += 1
                                    evet_cümleleri.append(cumle)
                                    #if on:
                                    st.write(f"Cümle: {cumle}")
                                    st.write(f"Sınıflandırma: {siniflandirma.choices[0].message.content} ")
                                    st.write("----------------------------------")
                                        
                    st.write(f" {kurs_adi} kursu için  kanala toplam kişi bazında soru sayısı: ", soru_sayisi)
                    
                    evet_cümleleri_toplu = '\n'.join(evet_cümleleri)
                    
                    with st.spinner("Soruların analizi yapılıyor..."):
                        response = openai.ChatCompletion.create(
                                    model="gpt-4",
                                    messages=[{"role": "system",
                                        "content": f"Öğrenciler kurs ile ilgili bu soruları sormuşlar, en çok bu kursun neresinde sorun yaşamışlar? maddeler halinde yaz. \n\n{evet_cümleleri_toplu}"}],
                                    max_tokens=4000,
                                    temperature=0.4,
                                    n=1,
                                    frequency_penalty=0.9,
                                    presence_penalty=0.0
                                )
                    
                    st.subheader(f"{kurs_adi} kursunda sorun yaşanan noktalar",divider="rainbow")
                    st.write(response.choices[0].message.content)
                    
                    st.subheader(f"İşte {dosya_adi} dosyasının kelime bulutu :magic_wand:", divider="orange")
                    if evet_cümleleri:
                        try:
                            all_words = " ".join(i for i in evet_cümleleri)
                            word_counts = Counter(all_words.split())
                            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
                            fig, ax = plt.subplots()  
                            plt.imshow(wordcloud, interpolation='bilinear')
                            plt.axis('off')
                            st.pyplot(fig)
                        except:
                            pass
                        
                    st.success(f'{dosya_adi} analizi bitti!', icon="✅")

if __name__ == "__main__":
    main()
