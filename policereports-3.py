import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Police Reports",
                   page_icon=":police_car:",
                   layout="wide"
)
df = pd.read_excel("policereports.xlsx")

# ---- SIDEBAR ----

st.sidebar.header("Filters: ")
day = st.sidebar.multiselect(
    "Day:",
    options=df["Incident Day"].unique(),
    default=df["Incident Day"].unique()
)

district = st.sidebar.multiselect(
    "District:",
    options=df["District"].unique(),
    default=df["District"].unique()
)

category = st.sidebar.multiselect(
    "Category:",
    options=df["Incident Category"].unique(),
    default=df["Incident Category"].unique()
)

df_selection = df.query(
    "`Incident Day` == @day and `District` == @district and `Incident Category` == @category"
)

st.dataframe(df_selection)


# ---- MAINPAGE ------

st.title("Police Reports Indexes :police_car:")
st.markdown("---")

# TOP KPI´s
conteo_district = df_selection['District'].value_counts()

porcentaje = conteo_district/len(df['District']) * 100

conteo_dia = df_selection['Incident Day'].value_counts()

porcentaje2 = conteo_dia/len(df['Incident Day']) * 100

first_column, second_column, third_column, fourth_column = st.columns(4)

with first_column:
    st.subheader("Total robberies by district")
    st.subheader(conteo_district)

with second_column:
    st.subheader("Percentage of robberies by district")
    st.subheader(f"{porcentaje.round(1)}")

with third_column:
    st.subheader("Total robberies per day")
    st.subheader(conteo_dia)

with fourth_column:
    st.subheader("Percentage of robberies per day")
    st.subheader(f"{porcentaje2.round(1)}")

st.markdown("---")

# ---- Robberies per day ----

robberies_per_day = (
    df_selection.groupby('Incident Day').size().reset_index(name='Total').sort_values(by="Total")
)
fig_robberies_per_day = px.bar(
    robberies_per_day,
    x="Total",
    y="Incident Day",
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

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_robberies_per_day, use_container_width=True)
right_column.plotly_chart(fig_robberies_categories, use_container_width=True)

# Esconder streamlit style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)