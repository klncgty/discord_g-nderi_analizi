from datetime import datetime
#### veri hazırlığı !!!!!!!
import pandas as pd
#df = pd.read_csv("Output_CSVs\ms-sql-sorgulama.csv",sep="~")
df['message_content'] = df['message_content'].astype(str)
df['mentions'] = df['mentions'].astype(str)
mentor=["gamzeakmannn","klncgty","pinarkilic","handekucukbulut","sebnemgurek","guldenizcanatan"]
for index, row in df.iterrows():
    mention_str = row['mentions']
    if mention_str == "[]":
        df.at[index, 'mentions'] = ""
    else:
        mention_str = mention_str.strip("[]'")  # Köşeli parantezleri ve tırnak işaretlerini kaldır
        df.at[index, 'mentions'] = mention_str
        
import numpy as np
df['mentions'].replace('', np.nan, inplace=True)    
pd.set_option('display.max_columns', None )
pd.set_option('display.max_rows', None)
df["time_stamp"] = pd.to_datetime(df["time_stamp"])

#df["tarih"] = df["time_stamp"].dt.date
#df["saat"] = df["time_stamp"].dt.time
#df["tarih"] = pd.to_datetime(df["tarih"])
#df["saat"] = pd.to_datetime(df["saat"])
#df['saat'] = pd.to_datetime(df['saat'], format='%H:%M:%S').dt.time
df.drop(["disc","Unnamed: 0"],axis=1,inplace=True)

#df['saat'] = pd.to_datetime(df['saat'], format='%H:%M:%S')

df['mentions'].fillna('', inplace=True)
#df = df.groupby('username').agg({
#    'message_content': ' '.join,  # message_content sütununu birleştir
#    'mentions':" ".join ,          # mentions sütununu birleştir
#    'tarih': 'min',                # En küçük tarih değerini al
#    'saat': 'min'                  # En küçük saat değerini al
#}).reset_index()


av = []
username_index = 0
idx = 0
time_differences = []
try:
    for i in df["username"]:
    
        if i not in mentor:
            username_value = i
            mentions_index = username_index  # İlk başta mentions sütununda aynı indexten başlayacağız
            for row in df["mentions"][mentions_index:]:
            
                if row == username_value:  # Eğer bulunan değer username ile aynıysa
                    row_index = df.loc[df["mentions"] == row].index[idx]
                    time_stamp_username = df["time_stamp"][username_index]
                    time_stamp_mentions = df["time_stamp"][row_index]
                    
                    time_difference = time_stamp_username - time_stamp_mentions   
                    time_difference_seconds = time_difference.total_seconds()
                    time_differences.append(time_difference_seconds)
                    average_time_difference = sum(time_differences) / len(time_differences)
                    av.append(average_time_difference)
                    #print("Average time difference:", average_time_difference, "seconds")

                    # Ortalama zaman farkını yazdırın
                               
             
                    #print(f"Time difference for {row}: ({time_stamp_username.strftime('%Y-%m-%d %H:%M:%S')} - {time_stamp_mentions.strftime('%Y-%m-%d %H:%M:%S')})")
                    idx += 1
                    break  # Bulunduğunda döngüden çık
    
                mentions_index += 1 # Döngüde sonraki indekse geç
     
        username_index += 1  # Sonraki kullanıcıya geç
   
except:
    
    print("Tüm tarama yapıldı!")
print("Ortalama cevap süresi", int(av[-1]/60/60),"saat")


Ortalama_cevap_süresi = int(av[-1]/60/60)
ay_farki = (df["time_stamp"].max().year - df["time_stamp"].min().year) * 12 + df["time_stamp"].max().month - df["time_stamp"].min().month
ay_farki
