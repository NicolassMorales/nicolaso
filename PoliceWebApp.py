import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Police Reports",
                   page_icon=":police_car:",
                   layout="wide"
)
df = pd.read_excel("policereports.xlsx")

# ---- SIDEBAR ----

st.sidebar.header("Filtros")
day = st.sidebar.multiselect(
    "Select the day:",
    options=df["Incident Day of Week"].unique(),
    default=df["Incident Day of Week"].unique()
)

district = st.sidebar.multiselect(
    "Select the district:",
    options=df["Police District"].unique(),
    default=df["Police District"].unique()
)

category = st.sidebar.multiselect(
    "Select the category:",
    options=df["Incident Category"].unique(),
    default=df["Incident Category"].unique()
)

df_selection = df.query(
    "`Incident Day of Week` == @day and `Police District` == @district and `Incident Category` == @category"
)

st.dataframe(df_selection)


# ---- MAINPAGE ------

st.title("Police Reports Indexes :police_car:")
st.markdown("##")

# TOP Ins
count_district = df_selection['Police District'].value_counts()

percentage = count_district/len(df['Police District']) * 100

day_count = df_selection['Incident Day of Week'].value_counts()

percentage_2 = day_count/len(df['Incident Day of Week']) * 100

first_column, second_column, third_column, fourth_column = st.columns(4)

with first_column:
    st.subheader("Total robberies by district")
    st.subheader(count_district)

with second_column:
    st.subheader("Percentage of robberies by district")
    st.subheader(f"{percentage.round(1)}")

with third_column:
    st.subheader("Total robberies per day")
    st.subheader(day_count)

with fourth_column:
    st.subheader("Percentage of robberies per day")
    st.subheader(f"{percentage_2.round(1)}")

st.markdown("---")

# ---- Robberies per day ----

robberies_per_day = (
    df_selection.groupby('Incident Day of Week').size().reset_index(name='Total').sort_values(by="Total")
)
fig_robberies_per_day = px.bar(
    robberies_per_day,
    x="Total",
    y="Incident Day of Week",
    orientation="h",
    title="<b>Robberies per day</b>",
    color_discrete_sequence=["#EF280F"] * len(robberies_per_day),
    template="plotly_white"
)

categories = (
    df_selection.groupby('Incident Category').size().reset_index(name='Total').sort_values(by="Total")
)
fig_robberies_categories = px.bar(
    categories,
    x="Total",
    y="Incident Category",
    orientation="h",
    title="<b>Robberies by category</b>",
    color_discrete_sequence=["#024A86"] * len(categories),
    template="plotly_white"
)

#-----------Incident by Hour-----------

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

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_robberies_per_day, use_container_width=True)
right_column.plotly_chart(fig_robberies_categories, use_container_width=True)
left_column.plotly_chart(fig_hourly_incident, use_container_width=True)



# streamlit style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

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