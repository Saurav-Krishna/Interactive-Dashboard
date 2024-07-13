import streamlit as st
import plotly.express as px 
import pandas as pd 
import os 
import warnings
warnings.filterwarnings('ignore')

# adding the title 
st.set_page_config(page_title='Superstore Interactive Dashboard',page_icon=':bar_chart:',layout='wide')



st.title(" :bar_chart: Sample Superstore EDA")
# css
st.markdown('<style>div.block-container{padding-top:1.8rem;}</style>',unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a File", type=(["csv","xlsx","xls"]))

if fl is not None:
    filename = fl.name
# write a logic to read identify csv , txt ,xlsx ,xls 
# also according to it pandas will use it based onthe type 
    st.write(filename)
    df = pd.read_csv(filename, encoding="ISO-8859-1")

else:
    df = pd.read_csv("Sample - Superstore.csv",encoding="ISO-8859-1")


# creating a date picker 

col1, col2 = st.columns((2))

df['Order Date'] = pd.to_datetime(df['Order Date'],format= "%d-%M-%Y")

# getting the min and max date from Order DATE column

# add drop down feature later
# min_date = df[(df["Order Date"]==)]

# max_date = df[(df['Order Date']== )]

start_date = pd.to_datetime(df['Order Date']).min()
end_date = pd.to_datetime(df['Order Date']).max()


with col1:
    date1 = pd.to_datetime(st.date_input(":small_red_triangle_down: Start Date",start_date))


with col2:
    date2 = pd.to_datetime(st.date_input(":small_red_triangle: Start Date",end_date))

# working on the specified date interval

df = df[(df['Order Date'] >= date1) & (df['Order Date'] <= date2 )].copy()




st.sidebar.header("Choose your filter: ")

region = st.sidebar.multiselect("Pick your region:", df['Region'].unique())

if not region:
    df2 = df.copy()
else:
    df2 = df[df['Region'].isin(region)]
    

# create for the state 
state = st.sidebar.multiselect("Pick your state:", df2['State'].unique())

if not state:
    df3 = df2.copy()
else:
    df3 = df2[(df['State'].isin(state))]

# create for city
city = st.sidebar.multiselect("Pick your city:", df3['City'].unique())

# if not city:
#     df4 = df3.copy()
# else:
#     df4 = df3[(df3['City'].isin(city))]



# for the one who doesnt input any region , state, city
# formulating the combinations according to the input 


if not region and not state and not city:
    filtered_df = df

elif not state and not city:
    filtered_df = df[(df['Region'].isin(region))]
elif not region and not city:
    filtered_df = df[(df['State'].isin(state))]
elif state and city:
    filterd_df = df3[(df['State'].isin(state))& (df3['City'].isin(city))]
elif region and city:
    filtered_df = df3[(df3['Region'].isin(region))& (df3['City'].isin(city))]
elif region and state:
    filtered_df = df3[(df['Region'].isin(region))& (df3['State'].isin(state))]
elif city:
    filtered_df = df3[df3['City'].isin(city)]

else:
    filtered_df = df3[(df3['Region'].isin(region))& (df3['State'].isin(state)) & (df['City'].isin(city))]



# creating column chart for category and region 
# st.column_config()

categorical_df = filtered_df.groupby(by = 'Category',as_index= False)['Sales'].sum()

with col1 :
    st.subheader("Category wise Sales")

    fig = px.bar(categorical_df,x='Category', y="Sales",
                 text=[f'${x:,.2f}'  for x in categorical_df['Sales']],
                  color='Category',
                                                                   template='seaborn')
    st.plotly_chart(fig, use_container_width=True,height=200)


# regional_sales = filtered_df.groupby(by='Region', as_index= False)['Sales'].sum()


with col2:
    st.subheader("Region wise Sales")

    fig = px.pie(filtered_df,values="Sales", names="Region",hole=0.5)
    fig.update_traces(text=filtered_df['Region'],textposition = "outside")

    st.plotly_chart(fig,use_container_width=True)

import matplotlib.pyplot as plt
# for live data

cl1,cl2  = st.columns((2))

with cl1:
    with st.expander("Category_View Data"):
        st.dataframe(categorical_df.style.background_gradient(cmap='Blues'))

        csv = categorical_df.to_csv(index=False).encode('utf-8')

        st.download_button("Download Data",data= csv,file_name="Category.csv",mime='txt/csv',
                           help="Click here to download the data in csv file")
        


with cl2:
    with st.expander("Region wise Data"):
        regional_df = filtered_df.groupby(by='Region',as_index=False)['Sales'].sum()
        st.dataframe(regional_df.style.background_gradient(cmap='plasma'))

        csv = regional_df.to_csv(index=False).encode('utf-8')

        st.download_button("Download Data",data= csv,file_name="Regional_sales.csv",mime='txt/csv',
                           help="Click here to download the data in csv file")