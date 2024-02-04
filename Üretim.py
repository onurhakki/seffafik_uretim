import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import streamlit.components.v1 as components


HtmlFile = open("footer.html", 'r', encoding='utf-8')
footer = HtmlFile.read() 

st.set_page_config(
    page_title="Üretim Miktarları",
    page_icon=":turtle:",
    layout="wide",
    #initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # },
)



container = """
        <style>
               .block-container {
                    padding-top: 2.5rem;
                    padding-bottom: 2.5rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """
st.markdown(container, unsafe_allow_html=True)


@st.cache_data  # 👈 Add the caching decorator
def load_data():
    excel = pd.read_excel("dataframe.xlsx")
    return excel


df = load_data()


month_to = {
    "Ocak":1,"Şubat":2,"Mart":3,"Nisan":4,"Mayıs":5,"Haziran":6,
    "Temmuz":7,"Ağustos":8,"Eylül":9,"Ekim":10,"Kasım":11,"Aralık":12}

year = st.sidebar.selectbox("Yıl",["Tümü",2020, 2021,2022,2023], index = 0, disabled=False)
month = st.sidebar.selectbox(
    "Ay",
    ["Tümü","Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"],
    index = 0, disabled=False)


if year != "Tümü" and month != "Tümü":
    selected_df = df[df["Yıl"] == year]
    selected_df = selected_df[selected_df["Ay"] == month_to[month]]
elif year == "Tümü" and month != "Tümü":
    selected_df = df[df["Ay"] == month_to[month]]
elif year != "Tümü" and month == "Tümü":
    selected_df = df[df["Yıl"] == year]
else:
    selected_df = df

shown_dataframe = selected_df.reset_index(drop=True).drop(
    ['Yıl', 'Haftanın günü', 'Ay', 'Saat', 'Gün', 'Yıl günü'], axis = 1).set_index("Tarih")


type_ = st.sidebar.selectbox("Sütun",list(
    shown_dataframe.drop(['Hafta sonu', 'Tatiller'], axis = 1).columns), index = 0, disabled=False)

weekends = st.sidebar.checkbox("Hafta sonu dahil", value = True)
if weekends != True:
    selected_df = selected_df[selected_df["Hafta sonu"] == 0]
    shown_dataframe = shown_dataframe[shown_dataframe["Hafta sonu"] == 0]



holidays = st.sidebar.checkbox("Tatiller dahil", value = True)
if holidays != True:
    selected_df = selected_df[selected_df["Tatiller"] == 0]
    shown_dataframe = shown_dataframe[shown_dataframe["Tatiller"] == 0]


#### Information

st.markdown('<div style="text-align: center;"><h1>2020-2023 yılları arasındaki<br>Üretim Miktarları</h1><br></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: left;">&#128072 Soldaki menüden ay, yıl, üretim türü, hafta sonu dahil olup olmaması ve tatil günlerinin dahil olup olmamasını seçebilirsiniz.<br><br></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: left;">&#128196 Veri kaynağı olarak <a href = "https://seffaflik.epias.com.tr/home">EPİAŞ Şeffaflık</a> sitesindeki Uzlaştırma Esas Veriş Miktarları (UEVM) kullanılmıştır.<br><br></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: left;">&#10071 Geçmişe Dönük Düzeltme Kalemi (GDDK) kapsamında üretim verileri değişebilmektedir. Görselleştirmede kullanılan veriler 01.02.2024 tarihinde alınmıştır. Burada sunulan görseller bilgilendirme amaçlıdır.<br><br></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: left;">&#128205 Veri kaynağına gitmek için <a href = "https://seffaflik.epias.com.tr/electricity/electricity-generation/ex-post-generation/injection-quantity">tıklayınız.</a><br><br></div>', unsafe_allow_html=True)


st.markdown('<div style="text-align: center;"><h2>{} (MWh)</h2></div>'.format(type_), unsafe_allow_html=True)
if weekends == True:
    st.markdown('<div style="text-align: left;"><i>• Hafta sonları dahil edilmiştir. (Menüden değişiklik yapabilirsiniz)</i></div>', unsafe_allow_html=True)
else:
    st.markdown('<div style="text-align: left;"><i>• Hafta sonları dahil edilmemiştir. (Menüden değişiklik yapabilirsiniz)</i></div>', unsafe_allow_html=True)
    
if holidays == True:
    st.markdown('<div style="text-align: left;"><i>• Resmi tatiller dahil edilmiştir. (Menüden değişiklik yapabilirsiniz)</i></div>', unsafe_allow_html=True)
else:
    st.markdown('<div style="text-align: left;"><i>• Resmi tatiller dahil edilmemiştir. (Menüden değişiklik yapabilirsiniz)</i></div>', unsafe_allow_html=True)



def create_3d(df, yaxis):
    fig = go.Figure(
        data=[
            go.Surface(
                y=yaxis,
                z=df.values,
                colorscale="RdYlGn",
                hovertemplate = '<i>Tarih</i>: %{y} %{x:02}:00<br>' +'<i>Miktar (MWh)</i>: <b>%{z:,.2f}</b>' + '<extra></extra>',

                )
                ])

    fig.update_layout(hovermode='x unified')

    fig.update_layout(
        autosize=False,
        scene_camera_eye=dict(x=-2, y=-0.9, z=1.5),
        #width=900,
        height=650,
        margin=dict(l=65, r=50, b=65, t=90),
        scene = dict(
                xaxis=dict(
                    title = "Saat",
                    range=[0, 23],
                    ticks='outside',
                    tickwidth=5,  
                    tickcolor='lightgray',
                    tickvals=[0,4,8,12,16,20],
                    ticktext=[0,4,8,12,16,20]),
                yaxis=dict(
                    title = "Tarih",
                    ticks='outside',
                    tickwidth=1,  
                    tickcolor='lightgray'),
                zaxis_title='MWh'),

    )
    return fig



if year != "Tümü" and month != "Tümü":
    st.markdown('<div style="text-align: left;"><br>{} yılı {} ayının {} üretim verileri saatlik kırılımda gösterilmektedir.</div>'.format(year, month, type_), unsafe_allow_html=True)

    avg_dataframe = selected_df[[type_, 'Gün', 'Saat']]
    avg_dataframe = avg_dataframe.groupby(['Gün', 'Saat'])[type_].mean().unstack("Saat")
    ind = avg_dataframe.index.tolist()
    index = ["{:02.0f}-{:02.0f}-{:4.0f}".format(
        i,month_to[month],year
        ) for i in ind]

    fig = create_3d(avg_dataframe, index)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Veri Seti"):
        st.dataframe(avg_dataframe)

elif year == "Tümü" and month != "Tümü":
    st.markdown('<div style="text-align: left;"><br>{} üretim verisinin 2020-2023 yıllarındaki {} ayı saatlik kırılımda gösterilmektedir.</div>'.format(type_, month), unsafe_allow_html=True)

    avg_dataframe = selected_df[[type_, 'Yıl', 'Gün', 'Saat']]
    avg_dataframe = avg_dataframe.groupby(['Yıl', 'Gün', 'Saat'])[type_].mean().unstack("Saat")
    ind = avg_dataframe.reset_index()[['Yıl', 'Gün']].drop_duplicates().values
    index = ["{:02.0f}-{:02.0f}-{:4.0f}".format(j-ind[0][1]+1,month_to[month],i) for i,j in ind]
   
    fig = create_3d(avg_dataframe, index)
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Veri Seti"):
        st.dataframe(avg_dataframe)


elif year != "Tümü" and month == "Tümü":
    st.markdown('<div style="text-align: left;"><br>{} üretim verisinin {} yılının tüm ayları saatlik kırılımda gösterilmektedir.</div>'.format(type_, year), unsafe_allow_html=True)

    avg_dataframe = selected_df[[type_, 'Ay', 'Gün', 'Saat']]
    avg_dataframe = avg_dataframe.groupby(['Ay', 'Gün', 'Saat'])[type_].mean().unstack("Saat")
    ind = avg_dataframe.reset_index()[['Ay', 'Gün']].drop_duplicates().values
    index = ["{:02.0f}-{:02.0f}-{:4.0f}".format(
        i,j,year
        ) for j,i in ind]

    fig = create_3d(avg_dataframe, index)
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Veri Seti"):
        st.dataframe(avg_dataframe)

else:
    st.markdown('<div style="text-align: left;"><br>{} üretim verisinin 2020-2023 yılları arasındaki tüm aylardaki günlerin saatlik ortalaması gösterilmektedir.</div>'.format(type_), unsafe_allow_html=True)

    avg_dataframe = selected_df[[type_, 'Yıl', 'Ay',  'Saat']]
    avg_dataframe = avg_dataframe.groupby(['Yıl', 'Ay', 'Saat'])[type_].mean().unstack("Saat")
    ind = avg_dataframe.reset_index()[['Yıl','Ay']].drop_duplicates().values
    index = ["{:02.0f}-{:02.0f}-{:4.0f}".format(
        1,i,j
        ) for j,i in ind]

    fig = create_3d(avg_dataframe, index)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Veri Seti"):
        st.dataframe(avg_dataframe)



### Footer
components.html(footer, height = 400)
