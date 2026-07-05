# 🏎️ Formuła 1 - Interaktywny Dashboard Analityczny

## Info o projekcie
Projekt zaliczeniowy z przedmiotu Big Data. Aplikacja jest interaktywnym dashboardem stworzonym w Streamlit, który pozwala na eksplorację prawdziwych danych o wyścigach Formuły 1 z lat 2000-2023. 

## Wykorzystane technologie:
* **Python** (Pandas do czyszczenia i agregacji danych)
* **Plotly Express** (5 różnych typów wykresów interaktywnych)
* **Streamlit** (Frontend, layout z zakładkami, filtry boczne, cachowanie danych)

## Źródło danych
Dane pochodzą z oficjalnego i darmowego zbioru "Formula 1 World Championship (1950 - 2023)" dostępnego na platformie Kaggle. Zostały pobrane lokalnie, połączone w locie za pomocą funkcji `pd.merge()` i oczyszczone (wyselekcjonowano dane od roku 2000 dla zachowania czytelności).

## Jak uruchomić lokalnie?
1. Sklonuj repozytorium.
2. Zainstaluj wymagane pakiety: `pip install -r requirements.txt` (lub przez `uv`).
3. Uruchom polecenie: `streamlit run app.py`.