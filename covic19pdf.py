import requests as req
from bs4 import BeautifulSoup
from tabula import read_pdf
import pandas as pd
import streamlit as st

url="https://www.pref.tochigi.lg.jp/e04/muryoukennsa.html"
res=req.get(url)
soup=BeautifulSoup(res.text,'html.parser')
result = soup.select("a[href]")

link_list =[]
for link in result:
    href = link.get("href")
    link_list.append(href)
    
pdf_list = [temp for temp in link_list if temp.endswith('pdf')]
# print(pdf_list[2])

url_covic_pdf='https://www.pref.tochigi.lg.jp'+f'{pdf_list[2]}'
area=[250,100,565,900]
df = read_pdf(url_covic_pdf,pages='all',area=area,lattice=True)
df_concat=pd.concat(df)
df_concat=df_concat.reset_index()

st.title('''
新型コロナウイルス
''')
st.header('''
栃木県内無料検査拠点検索システム
''')
st.write('#### 栃木県が公開するデータをもとに作成した検索システムです。')
st.write(url)

city=st.selectbox(
    '検索したい市町を選択してください。',
    ('すべて','宇都宮市','足利市','栃木市','佐野市','鹿沼市',
    '日光市','小山市','真岡市','大田原市','矢板市','那須塩原市',
    'さくら市','那須烏山市','下野市',
    '上三川町','益子町','茂木町','市貝町',
    '芳賀町','壬生町','野木町','塩谷町','高根沢町','那須町','那珂川町')
    )
method=st.selectbox(
    '検査方法を選択してください。',
    ('すべて','抗原','PCR')
)

if city=='すべて':
    df=df_concat
else:
    df=df_concat[df_concat['所在地'].str.contains(city)]

  # method=input('検査方法を選択してください。')
if method=='すべて':
    df=df
else:
    df=df[df['検査種類'].str.contains(method)]

st.dataframe(df[['検査拠点','検査種類']])
# ,'所在地','連絡先','備考']])
st.write('拠点数:'+str(len(df)))

st.write("""



""")
num=st.number_input('index番号を入力して詳細を表示する。',step=1)
num=int(num)
if num==None:
    st.write('番号を入力してください。')
else:
    st.write('###### 検査拠点')
    st.write(df_concat.loc[num,'検査拠点'])
    st.write('###### 検査種類')
    st.write(df_concat.loc[num,'検査種類'])
    st.write('###### 所在地')
    st.write(df_concat.loc[num,'所在地'])
    st.write('###### 連絡先')
    st.write(df_concat.loc[num,'連絡先'])
    st.write('###### 備考')
    st.write(df_concat.loc[num,'備考'])

st.write('vol.1.0     2022.5.2 ')
st.write('vol.1.0.1   2022.5.5 元データPDFの読み込み不具合を修正')
st.write('Copyright © kuboyemon')

