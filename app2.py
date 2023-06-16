import pandas as pd
import plotly.express as px
import streamlit as st
import statistics as sts
import numpy as np
import folium
from streamlit_folium import st_folium, folium_static


st.set_page_config(page_title='Police Department Incident Reports 2018',
                   page_icon=':bar_chart:',
                   layout='wide'
)

#@st.cache
def get_data_from_csv():
    df=pd.read_xslx(
        'policereports.xlsx'
    )

    #Add 'hour' column to dataframe
    df['hour']=pd.to_datetime(df['Incident_Time'], format='mixed').dt.hour
    return df
df=get_data_from_csv()
#st.dataframe(df)

#--------SIDEBAR-------------
st.sidebar.header('Please Filter Here:')
incident_year= st.sidebar.multiselect(
    'Select the Incident Year:',
    options=df['Incident_Year'].unique(),
    default=df['Incident_Year'].unique()
)

report_type_code= st.sidebar.multiselect(
    'Select the Report Type Code:',
    options=df['Report_Type_Code'].unique(),
    default=df['Report_Type_Code'].unique()
)

report_type_description= st.sidebar.multiselect(
    'Select the Report Type Description:',
    options=df['Report_Type_Description'].unique(),
    default=df['Report_Type_Description'].unique()
)

resolution= st.sidebar.multiselect(
    'Select the Resolution:',
    options=df['Resolution'].unique(),
    default=df['Resolution'].unique()
)

df_selection=df.query(
    'Incident_Year == @incident_year & Report_Type_Code == @report_type_code & Report_Type_Description == @report_type_description & Resolution == @resolution' 
)

#st.dataframe(df_selection)

#-------MAINPAGE-------------

st.title(':police_car: Police Department Incident Dashboard')
st.markdown('---')

IN_count = int(df_selection['Incident_Number'].count())
IC_mode=sts.mode(df_selection['Incident_Category'])
ISubC_mode=sts.mode(df_selection['Incident_Subcategory'])
AN_mode=sts.mode(df_selection['Analysis_Neighborhood'])
SD_mode=int(sts.mode(df_selection['Supervisor_District']))

left_column, middle_column, middle_column2, middle_column3, right_column = st.columns(5)
with left_column:
    st.subheader('Incident Cases:')
    st.subheader(f'Cases # {IN_count:,}')
with middle_column:
    st.subheader('Incident Category:')
    st.subheader(f'Mode: {IC_mode}')
with middle_column2:
    st.subheader('Incident Subcategory:')
    st.subheader(f'Mode: {ISubC_mode}')
with middle_column3:
    st.subheader('Analysis Neighborhood:')
    st.subheader(f'Mode: {AN_mode}')
with right_column:
    st.subheader('Supervisor District:')
    st.subheader(f'Mode: {SD_mode}')
st.markdown('---')

#-----------Incident Day of Week [BAR CHART]---------

incident_cases_by_day_of_week=(
    df_selection.groupby(by=['Incident_Day_of_Week'])[['Incident_Number']].count().sort_values(by='Incident_Number')
)
fig_day_of_week_incident = px.bar(
    incident_cases_by_day_of_week,
    x='Incident_Number',
    y=incident_cases_by_day_of_week.index,
    orientation='h',
    title='<b>Incident Cases by Day of Week</b>',
    color_discrete_sequence=['#0083B8'] * len(incident_cases_by_day_of_week),
    template='plotly_white',
)
fig_day_of_week_incident.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False))
)

#st.plotly_chart(fig_day_of_week_incident)

#-----------Incident by Hour [BAR CHART]-----------

incident_by_hour = df_selection.groupby(by=['hour'])[['Incident_Number']].count()
fig_hourly_incident=px.bar(
    incident_by_hour,
    x=incident_by_hour.index,
    y='Incident_Number',
    title='<b>Incident Cases by Hour</b>',
    color_discrete_sequence=['#0083B8'] * len(incident_by_hour),
    template='plotly_white',
)
fig_hourly_incident.update_layout(
    xaxis=dict(tickmode='linear'),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=(dict(showgrid=False))
)

#st.plotly_chart(fig_hourly_incident)

#-----------Incident by Police District-----------

incident_by_police_district=(
    df_selection.groupby(by=['Police_District'])[['Incident_Number']].count().sort_values(by='Incident_Number')
)
fig_police_district_incident = px.bar(
    incident_by_police_district,
    x='Incident_Number',
    y=incident_by_police_district.index,
    orientation='h',
    title='<b>Incident Cases by Police District</b>',
    color_discrete_sequence=['#0083B8'] * len(incident_by_police_district),
    template='plotly_white',
)
fig_police_district_incident.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False))
)

#st.plotly_chart(fig_police_district)

#---------------Graficas---------------------

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_incident, use_container_width=True)
left_column.plotly_chart(fig_police_district_incident, use_container_width=True)
right_column.plotly_chart(fig_day_of_week_incident, use_container_width=True)

#---------------Global World---------------------

df.dropna(subset=['Latitude','Latitude'],inplace=True)
df.rename(columns={'Latitude':'latitude'},inplace=True)
df.rename(columns={'Longitude':'longitude'},inplace=True)

st.map(df, use_container_width=True)

#----------------------Ejemplo usado para mostrar varios punto con la libreria folium, pero se tarda mucho en cargar------------------
#Link de ejemplo: https://towardsdatascience.com/3-easy-ways-to-include-interactive-maps-in-a-streamlit-app-b49f6a22a636


'''m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], 
                 zoom_start=3, control_scale=True)
#Loop through each row in the dataframe
for i,row in df.iterrows():
    #Setup the content of the popup
    iframe = folium.IFrame('Row_ID:' + str(row["Row_ID"]))
    
    #Initialise the popup using the iframe
    popup = folium.Popup(iframe, min_width=300, max_width=300)
    
    #Add each row to the map
    folium.Marker(location=[row['latitude'],row['longitude']],
                  popup = popup, c=row['Row_ID']).add_to(m)

st_data = st_folium(m, width=700)

folium_static(m, width=700)

import plotly.express as px

fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", zoom=3)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)

fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", 
hover_name='Well Name', zoom=3)'''

#---------------------------------Ejemplo usado para mostrar 1 punto con la libreria folium------------------

'''map=folium.Map(location=[40.965, -5.664], zoom_start=16)
folium.Marker(
    [40.965, -5.664],
    popup='Liberty Bell',
    tooltip='Liberty Bell',
).add_to(map)
st_data=st_folium(map, width=725)'''

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """

st.markdown(hide_st_style, unsafe_allow_html=True)
#print(df)