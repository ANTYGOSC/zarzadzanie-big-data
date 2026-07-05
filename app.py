import streamlit as st
import pandas as pd
import plotly.express as px

# Konfiguracja strony
st.set_page_config(page_title="Dashboard F1", layout="wide", page_icon="🏎️")

@st.cache_data
def load_data():
    df_races = pd.read_csv("races.csv")
    df_results = pd.read_csv("results.csv")
    df_drivers = pd.read_csv("drivers.csv")
    
    df = pd.merge(df_results, df_races, on="raceId", suffixes=("_result", "_race"))
    df = pd.merge(df, df_drivers, on="driverId")
    
    df["driver_name"] = df["forename"] + " " + df["surname"]
    df["date"] = pd.to_datetime(df["date"])
    
    df_clean = df[df["year"] >= 2000][
        ["year", "name", "date", "driver_name", "nationality", "grid", "positionOrder", "points"]
    ].copy()
    
    return df_clean.sort_values(by="date")

df = load_data()

# --- INTERFEJS UŻYTKOWNIKA ---
st.title("🏎️ Formuła 1: Interaktywna Analiza Wyścigów")
st.markdown("Dashboard eksploracyjny na podstawie wyników wyścigów Formuły 1 z lat 2000-2023. **Projekt zaliczeniowy z Big Data.**")

st.sidebar.header("🎛️ Filtry Dashboardu")

min_year, max_year = int(df["year"].min()), int(df["year"].max())
selected_years = st.sidebar.slider("Wybierz zakres lat", min_year, max_year, (2015, 2020))

narodowosci = df["nationality"].unique()
selected_nat = st.sidebar.multiselect("Narodowość kierowcy", options=narodowosci, default=["British", "German", "Finnish"])

search_driver = st.sidebar.text_input("Szukaj kierowcy (np. Hamilton, Vettel)", "")

# Zastosowanie filtrów
df_filtered = df[
    (df["year"] >= selected_years[0]) & 
    (df["year"] <= selected_years[1]) &
    (df["nationality"].isin(selected_nat))
]

if search_driver:
    df_filtered = df_filtered[df_filtered["driver_name"].str.contains(search_driver, case=False, na=False)]

# --- WSKAŹNIKI (KPI) ---
st.subheader("📊 Podsumowanie dla wybranych filtrów")
col1, col2, col3 = st.columns(3)
col1.metric("Wyścigi w bazie", df_filtered["name"].nunique())
col2.metric("Unikalni kierowcy", df_filtered["driver_name"].nunique())
col3.metric("Suma rozdanych punktów", f"{df_filtered['points'].sum():.0f}")

st.divider()

# --- WYKRESY (WYMÓG: MIN. 5 TYPÓW) ---
tab1, tab2 = st.tabs(["🏆 Zwycięstwa i Wyścigi", "📈 Trendy i Rozkłady"])

with tab1:
    colA, colB = st.columns(2)
    with colA:
        st.markdown("### 1. Zwycięstwa w wybranym okresie (Bar Chart)")
        wins = df_filtered[df_filtered["positionOrder"] == 1].groupby("driver_name").size().reset_index(name="wins")
        wins = wins.sort_values("wins", ascending=False).head(10)
        
        if not wins.empty:
            fig1 = px.bar(wins, x="driver_name", y="wins", color="wins", color_continuous_scale="Reds", template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("Brak zwycięstw dla wybranych kryteriów.")

    with colB:
        st.markdown("### 2. Pozycja startowa vs Meta (Scatter Plot)")
        if not df_filtered.empty:
            fig2 = px.scatter(df_filtered, x="grid", y="positionOrder", color="points", hover_data=["driver_name", "name", "year"], template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Brak danych.")

with tab2:
    st.markdown("### 3. Zdobyte punkty na przestrzeni lat (Line Chart)")
    if not df_filtered.empty:
        points_time = df_filtered.groupby(["year", "driver_name"])["points"].sum().reset_index()
        top_5_drivers = points_time.groupby("driver_name")["points"].sum().nlargest(5).index
        points_time = points_time[points_time["driver_name"].isin(top_5_drivers)]
        
        fig3 = px.line(points_time, x="year", y="points", color="driver_name", markers=True, template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)
    
    colC, colD = st.columns(2)
    with colC:
        st.markdown("### 4. Rozkład miejsc startowych (Histogram)")
        if not df_filtered.empty:
            fig4 = px.histogram(df_filtered, x="grid", nbins=24, color_discrete_sequence=["#3498DB"], template="plotly_dark")
            st.plotly_chart(fig4, use_container_width=True)
            
    with colD:
        st.markdown("### 5. Udział narodowości w punktach (Treemap)")
        if not df_filtered.empty:
            treemap_data = df_filtered.groupby(["nationality", "driver_name"])["points"].sum().reset_index()
            treemap_data = treemap_data[treemap_data["points"] > 0]
            if not treemap_data.empty:
                fig5 = px.treemap(treemap_data, path=[px.Constant("Kierowcy"), "nationality", "driver_name"], values="points", template="plotly_dark")
                st.plotly_chart(fig5, use_container_width=True)
            else:
                st.warning("Brak punktów do narysowania drzewa.")

with st.expander("📋 Pokaż surowe dane CSV"):
    st.dataframe(df_filtered)