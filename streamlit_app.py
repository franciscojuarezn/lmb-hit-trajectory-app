import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import numpy as np
from datetime import datetime

from forms.contact import contact_form

#Define text in n languages

text = {
    "en": {
        "title": "Batted Ball Distribution Visualization LMB",
        "description": """
        This app is designed to visualize the batted ball type and distribution for a selected player from the Liga Mexicana de Beisbol. 
        \nUsers can explore various outcomes such as singles, doubles, triples, home runs, and outs.  
        It also allows filtering based on batter splits, batted ball type and specific time frames, providing deeper insights into player performance.
        """,
        "disclaimer": """
        **Disclaimer:** The data source is MLB Gameday, which may not be perfectly accurate. However, it closely matches the data provided by Trackman.
        """,
        "player_select": "Player",
        "split_select": "Split",
        "event_select": "Event Types",
        "date_select": "Date Range",
        "batted_ball_select": "Batted Ball Type",
        "choose_plot" : "Choose Plot",
        "outcome_plot" : "Outcome Only",
        "outcome_trajectory" : "Outcome and Batted Ball Type",
        "outcome_text" : "Outcome distribution plot for",
        "trajectory_text" : "Batted Ball Type distribution",
        "socials": "Check out my socials",
        "contact_title": "Contact Me"
        # "email_me": "📧 [Email me](mailto:your_email@example.com)",        
    },
    "es": {
        "title": "Distribución de Pelota Bateada LMB",
        "description": """
        Esta aplicación está diseñada para visualizar la distribución de bateo y tipo de pelota bateada de un jugador de la Liga Mexicana de Beisbol. 
        \nLos usuarios pueden escoger entre diferentes resultados como sencillos, dobles, triples, jonrones y outs. 
        También permite filtrar por divididas del perfil, tipo de pelota bateada y periodos de tiempo específicos, proporcionando una visión más profunda del rendimiento del jugador.
        """,
        "disclaimer": """
        **Aviso:** La fuente de los datos es MLB Gameday, la que podría no ser completamente precisa. Sin embargo, coincide bastante con los datos proporcionados por Trackman, lo que lo convierte en una herramienta confiable para el análisis.
        """,
        "player_select": "Jugador",
        "split_select": "Split",
        "event_select": "Tipo de evento",
        "date_select": "Rango de fecha",
        "batted_ball_select": "Pelota Bateada",
        "choose_plot" : "Seleccionar gráfico",
        "outcome_plot" : "Solo Evento",
        "outcome_trajectory" : "Evento y Pelota Bateada",
        "outcome_text" : "Distribución por eventos de",
        "trajectory_text" : "Distribución por tipo de pelota bateada de",
        "socials": "Mis redes sociales",
        "contact_title": "Contáctame"
        # "email_me": "📧 [Envíame un correo](mailto:your_email@example.com)",        
    }
}

col1, col2 = st.columns([3, 1])

# Language selection
with col2:
    language = st.selectbox("Lang", ["English", "Español"], index=0)

lang_code = "en" if language == "English" else "es"

# Title 
with col1:
    st.title(text[lang_code]["title"])

# Desctiption and disclaimer
st.write(text[lang_code]["description"])
st.write("\n")
st.write(text[lang_code]["disclaimer"])

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('hit_trajectory.csv')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file not found.")
except pd.errors.ParserError:
    st.error("Error parsing the data file.")

# Player Selection
players = df['batter_name'].unique().tolist()

# Set a default player
default_player = 'Robinson Canó'
default_index = players.index(default_player) if default_player in players else 0

col1, col2 = st.columns(2)
with col1:
    selected_batter = st.selectbox(text[lang_code]["player_select"], players, index=default_index)
with col2:
    
    # Date range
    date_min = pd.to_datetime(df['date']).min().date()
    date_max = pd.to_datetime(df['date']).max().date()
    selected_dates = st.date_input(text[lang_code]["date_select"], [date_min, date_max], min_value=date_min, max_value=date_max)
    selected_dates = [pd.to_datetime(d) for d in selected_dates]
    selected_dates = [d.strftime("%Y-%m-%d") for d in selected_dates]

# Create columns
col1, col2, col3 = st.columns(3)

with col1:
    # Seles split
    split_options = df['split_batter'].unique()
    selected_splits = st.multiselect(text[lang_code]["split_select"], split_options, default=split_options)

event_types = ['single', 'double', 'triple', 'home_run', 'out']

with col2:
    selected_events = st.multiselect(text[lang_code]["event_select"], event_types, default=event_types)

# Toggle
plot_choice = st.radio(f"{text[lang_code]['choose_plot']}", [f"{text[lang_code]['outcome_plot']}", f"{text[lang_code]['outcome_trajectory']}"], index=0)

if plot_choice == f"{text[lang_code]['outcome_trajectory']}":
    with col3:
        trajectory_markers = ['line_drive', 'fly_ball', 'ground_ball', 'popup']
        selected_trajectory = st.multiselect(f"{text[lang_code]['batted_ball_select']}", trajectory_markers, default=trajectory_markers)

# All 'outs'
out_events = ['field_out', 'double_play', 'force_out', 'sac_bunt', 'grounded_into_double_play', 'sac_fly', 'fielders_choice_out', 'field_error', 'sac_fly_double_play']
df['event'] = df['event'].apply(lambda x: 'out' if x in out_events else x)

# filter 
filtered_df_outcome  = df[
    (df['batter_name'] == selected_batter) &
    (df['event'].isin(selected_events)) &
    (pd.to_datetime(df['date']).between(selected_dates[0], selected_dates[1])) &
    (df['split_batter'].isin(selected_splits))
]

filtered_df_trajectory = pd.DataFrame()
if plot_choice == f"{text[lang_code]['outcome_trajectory']}":
    filtered_df_trajectory = df[
        (df['batter_name'] == selected_batter) &
        (df['event'].isin(selected_events)) &
        (df['batted_ball_type'].isin(['line_drive', 'fly_ball', 'ground_ball', 'popup'])) &
        (pd.to_datetime(df['date']).between(selected_dates[0], selected_dates[1])) &
        (df['split_batter'].isin(selected_splits))
    ]
team_data = pd.read_csv('stadium_2.csv')

# subheader
if lang_code == 'en':
    st.subheader(f"Batted Ball Distribution for {selected_batter} from {selected_dates[0]} to {selected_dates[1]}")
else:
    st.subheader(f"Distribución Pelota Bateada de {selected_batter} desde {selected_dates[0]} a {selected_dates[1]}")

# Plot the data
def plot_field_and_hits(team_data, hit_data, selected_column, palette, plot_title):
    plt.figure(figsize=(15,15))
    y_offset = 275
    excluded_segments = ['outfield_inner']
    for segment_name in team_data['segment'].unique():
        if segment_name not in excluded_segments:
            segment_data = team_data[team_data['segment'] == segment_name]
            plt.plot(segment_data['x'], -segment_data['y'] + y_offset, linewidth=4, zorder=1, color='forestgreen', alpha=0.5)

    hit_data['adj_coordY'] = -hit_data['coordY'] + y_offset
    sns.scatterplot(data=hit_data, x='coordX', y='adj_coordY', hue=selected_column, palette=palette, edgecolor='black', s=100, alpha=0.7)

    plt.title(plot_title, fontsize=15)

    # Distance and watermark
    plt.text(125, -25 + y_offset, '410', fontsize=12, ha='center')
    plt.text(230, -90 + y_offset, '330', fontsize=12, ha='center')
    plt.text(20, -90 + y_offset, '330', fontsize=12, ha='center')
    plt.text(295, 23, 'Created by: @iamfrankjuarez', fontsize=12, color='grey', alpha=0.5, ha='right')

    plt.xlabel("")
    plt.ylabel("")
    plt.legend(
        title=selected_column, 
        title_fontsize='14',
        fontsize='14',
        borderpad=1         
    )

    plt.xticks([])
    plt.yticks([])
    plt.xlim(-50, 300)
    plt.ylim(20, 300)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(False)
    st.pyplot(plt)
    
if plot_choice == "Outcome Only":
    if not filtered_df_outcome.empty:
        plot_title = f"{text[lang_code]['outcome_text']} {selected_batter}"
        st.subheader(plot_title)
        plot_field_and_hits(team_data, filtered_df_outcome, 'event', {
            'single': 'darkorange', 'double': 'purple', 'triple': 'yellow', 'home_run': 'red', 'out': 'grey'
        }, plot_title)
    else:
        st.write("No data available for the selected filters.")
else:
    if not filtered_df_outcome.empty:
        plot_title = f"{text[lang_code]['outcome_text']} {selected_batter}"
        st.subheader(plot_title)
        plot_field_and_hits(team_data, filtered_df_outcome, 'event', {
            'single': 'darkorange', 'double': 'purple', 'triple': 'yellow', 'home_run': 'red', 'out': 'grey'
        }, plot_title)
    
    if not filtered_df_trajectory.empty:
        plot_title = f"{text[lang_code]['trajectory_text']} {selected_batter}"
        st.subheader(f"{text[lang_code]['trajectory_text']} {selected_batter}")
        plot_field_and_hits(team_data, filtered_df_trajectory, 'batted_ball_type', {
            'line_drive': 'blue', 'fly_ball': 'cyan', 'ground_ball': 'brown', 'popup': 'magenta'
        }, plot_title)
    elif filtered_df_outcome.empty:
        st.write("No data available for the selected filters.")
@st.dialog(text[lang_code]['contact_title'])
def show_contact_form():
    contact_form(lang_code)

# Socials function
def open_socials():
    st.write(f"{text[lang_code]['socials']}")
    st.markdown("[Twitter](https://twitter.com/iamfrankjuarez)")
    st.markdown("[LinkedIn](https://linkedin.com/in/francisco-juarez-niebla-4b6271147)")
    st.markdown("[GitHub](https://github.com/franciscojuarezn)")

# Contact section
col1, col2, col3 = st.columns([4,1,1], gap="small")

with col2:
    if st.button("🔗 Socials"):
        open_socials()    

with col3:
    if st.button("📧 Contact"):
        show_contact_form()