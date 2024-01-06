import pandas as pd 
import numpy as np 
import streamlit as st 
from streamlit_option_menu import option_menu 
import matplotlib.pyplot as plt 
import seaborn as sns 
import plotly.express as px 
import altair as alt 


st.set_page_config(page_title="Football Dashboard",page_icon='football',layout='wide')
st.title(':red[ Stats Comparison between Messi and Ronaldo]')

st.markdown(
    """
    <style>
    div[data-testid="stApp"]  {
        background:url("Football/image/bg.jpg");
    }
   </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
div[data-testid="column"] {
   background-color: rgba(0,128,128, 0.4);
   border: 3px solid rgba(64,224,208,0.9);
   padding: 5% 2% 7% 1%;
   border-radius:7px;
   color: rgb((255,0,0));
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="element-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: black;
}
</style>
"""
, unsafe_allow_html=True)


df=pd.read_csv('Football_new.csv')
df.head()


#df=df.drop(columns=['Matchday'])
df=df.drop(columns=['Goal_assist'])

df.info()
df.isnull().sum()

df['Type'].mode()
# df['Type'].value_counts()
df['Type']=df['Type'].fillna('Left-footed shot')

df['Playing_Position'].mode()
# df['Playing_Position'].value_counts()
df['Playing_Position']=df['Playing_Position'].fillna('CF')

# df['Date'] = pd.to_datetime(df.Date)
# df['Year']=df['Date'].dt.year
# df=df.drop(columns=['Date'])
df['Result']=df['Result'].map({'WON':1,'LOST':0})
df['Rslt']=df['Result'].map({1:'Won',0:'Lost'})
df['Venue']=df['Venue'].map({'A':'Away','H':'Home'})
df['Playing_Position']=df['Playing_Position'].map({'CF':'CF','LW':'LW','RW':'RW','SS':'SS','AM':'AM'})
df.Result.value_counts()
# tee=int(df[(df["Result"] == 1)]["Result"].count())
df.rename(columns={'Type1':'Goals'},inplace=True)
df.rename(columns={'Competition_country':'Country'},inplace=True)

Category_C=[]

for i in df['Minute']:
      if i <45:
            Category_C.append('First Half')
      elif i>=45 and i<49:
            Category_C.append('Extra Time')
      elif i>=49 and i<90:
            Category_C.append('Second Half')
      else:
            Category_C.append('Extra Time')

df['Minute_cat']=Category_C
df.Minute_cat.value_counts()


with st.sidebar:
    st.markdown('### :red[A dashboard comparing the feats of Ronaldo and Messi based on their goals]')
    # selected=option_menu(
    #     menu_title="Menu",
    #     options=["KPI and Tables","Charts"],
    #     icons=["table","bar-chart"],
    #     menu_icon="trophy",
    #     default_index=0,
        
        # orientation="horizontal"

    

# top-level filters

    # player_filter = st.selectbox("Select Player", pd.unique(df['Player']))
    # Match_filter = st.selectbox("Match Type", pd.unique(df['Matchday']))

with st.sidebar:
  player_filter = st.selectbox("Select Player", pd.unique(df['Player']))
  Match_filter = st.selectbox("Match Type", pd.unique(df['Matchday']))




# if selected=="KPI and Tables": 

placeholder = st.empty()

# creating a single-element container


# # dataframe filter
df = df[df["Player"] == player_filter]

df=df[df["Matchday"]== Match_filter]

with placeholder.container():
        col1,kpi1, col2,kpi2, col3,col4,kpi3 = st.columns(7)
        col1.metric(label="Home Games",
        value=int(df.Venue.value_counts()['Home']))
        kpi1.metric(label="Home wins",
                value=df.query("Venue=='Home'")["Result"].sum())
        col2.metric(label="Away Games",
        value=int(df.Venue.value_counts()['Away']))
        kpi2.metric(label="Away wins",
                value=df.query("Venue=='Away'")["Result"].sum())
        col3.metric(label="Goals Count",
        value=int(df.Goals.value_counts()[1]))
        col4.metric(label="Total Wins",
                    value=df.Result.value_counts()[1])
        kpi3.metric(label="Lost Games",
                value=df.Result.value_counts()[0])      
    

        
        tb1,tb2,tb3=st.tabs(['Goals for Each Club','Goals in Each League','Goals in Each Country'])
        with tb1:
            st.markdown("### Goals for Each Club")
            st.write(df.groupby("Club")["Goals"].sum())
        with tb2:
            st.markdown('### Goals in Each League')
            st.write(df.groupby("Competition")["Goals"].sum())
        with tb3:
            st.markdown('### Goals in Each Country')
            st.write(df.groupby("Country")["Goals"].sum())
        
        fig1,fig2,fig3=st.tabs(["Type of Goals in Each Country","Goals scored during","Goals Scored Home Vs Away"])

        
        chart = alt.Chart(df).mark_bar().encode(
        x='Country',
        y='sum(Goals)',
        color='Type',
        ).interactive()
        
        with fig1:
            st.altair_chart(chart, theme="streamlit", use_container_width=True)

        bart = alt.Chart(df).mark_bar().encode(
        x='Rslt',
        y='sum(Goals)',
        color='Minute_cat',
        ).interactive()
        
        with fig2:
            st.altair_chart(bart, theme="streamlit", use_container_width=True)

        cart = alt.Chart(df).mark_bar().encode(
        x='Venue',
        y='sum(Goals)',
        # color='Minute_cat',
        ).interactive()
        
        with fig3:
            st.altair_chart(cart, theme="streamlit", use_container_width=True)



        # fig1,fig2=st.columns(2)
        # with fig1:
        #         st.markdown("### Second Chart")
        #         fig1 = px.bar(data_frame=df, x="Club")
        #         st.write(fig1)
