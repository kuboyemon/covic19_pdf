import requests as req
from bs4 import BeautifulSoup
from tabula import read_pdf
import pandas as pd
import streamlit as st
import streamlit.components.v1 as stc

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
# area=[330,150,1000,1200]
# df = read_pdf(url_covic_pdf,pages='all',area=area,lattice=True)
# df_concat=pd.concat(df)
# df_concat=df_concat.reset_index()
url_covic_pdf='https://www.pref.tochigi.lg.jp'+f'{pdf_list[2]}'
area=[180,70,1000,1200]
df = read_pdf(url_covic_pdf,pages='all',area=area,lattice=True)
df_concat=pd.concat(df)
df_concat=df_concat.reset_index()
df_concat=df_concat.rename(columns={'Unnamed: 0': '検査拠点','Unnamed: 1': '種別','Unnamed: 2': '検査方法','Unnamed: 3': '所在地','Unnamed: 4': '電話番号','Unnamed: 5': '備考'})


st.title('''
新型コロナウイルス
''')
st.header('''
栃木県内無料検査拠点検索システム
''')
st.subheader('栃木県が公開するデータを元に作成した検索システムです。ブックマーク登録してもらえるとうれしいです。')
st.write('元データ掲載URL')
st.write(url)
st.write('※元データ書式が変更された場合正常に起動しないことがあります。この場合元URLより元データを参照し電話番号等確認ください。')

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
    df=df[df['検査方法'].str.contains(method)]

st.dataframe(df[['検査拠点','検査方法']])
# ,'所在地','連絡先','備考']])
st.write('拠点数:'+str(len(df)))

st.write("""



""")
df_index=df.index.values

num=st.selectbox('index番号を選択して詳細を表示する。',
(i for i in df_index)
)
num=int(num)
if num==None:
    st.write('番号を入力してください。')
else:
    st.write('###### 検査拠点')
    st.write(df_concat.loc[num,'検査拠点'])
    st.write('###### 検査方法')
    st.write(df_concat.loc[num,'検査方法'])
    # st.write('###### 連絡先')
    # tel_num=df_concat.loc[num,'連絡先']
    # st.write('※長押しで電話発信可能')
    # stc.html("<a href='tel:{}'>{}</a>".format(tel_num,tel_num)) 
    st.write('###### 所在地')
    # st.write('※長押しでgoogle map表示')
    # stc.html("<a href='https://www.google.co.jp/maps/place/{}'>{}</a>".format(df_concat.loc[num,'所在地'],df_concat.loc[num,'所在地'])) 
    link='[{}](https://www.google.co.jp/maps/place/{})'.format(df_concat.loc[num,'所在地'],df_concat.loc[num,'所在地'])
    st.markdown(link, unsafe_allow_html=True)
    st.write('###### 備考')
    st.write(df_concat.loc[num,'備考'])
    st.write('###### 電話番号')
    tel_num=df_concat.loc[num,'電話番号']
    st.write('※長押しで電話発信可能')
    stc.html("<a href='tel:{}'>{}</a>".format(tel_num,tel_num)) 
st.write("""
""")

st.write('Ver.1.0     2022.5.2 ')
st.write('Ver.1.0.1   2022.5.5 元データPDFの読み込み不具合を修正')
st.write('Ver.1.1.0   2022.5.5 詳細表示選択部を入力式から選択式に修正')
st.write('Ver.1.2.0   2022.5.11 Tel link機能を追加')
st.write('Ver.1.3.0   2022.5.15 Google map link機能を追加')
st.write('Ver.1.3.1   2022.5.15 配置等微調整')
st.write('Ver.1.3.2   2022.6.1 元データPDF変更に伴い微調整')
st.write('Ver.1.3.3   2022.6.4 元データPDF変更に伴い微調整,冒頭注意書きを追加')
st.write('※iPhoneSE3にて動作確認')
st.write('Copyright © kuboyemon at Yaita PS from Tochigi PD')

