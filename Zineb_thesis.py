import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout='wide')

# Charger les données
@st.cache_data
def load_data():
    return pd.read_excel(r"C:\Users\abder\Downloads\thesis.xlsx", sheet_name='Réponses au formulaire 1')

df = load_data()

df = load_data()

# Title and description
st.title("📊 Samsung Social Media Analytics")
st.markdown("#### Analyse interactive des réponses du questionnaire sur la présence sociale de Samsung")

# Sidebar filters
st.sidebar.header("Filtres")
age_group = st.sidebar.selectbox('Tranche d\'âge', ['Tous'] + list(df['What is your age group?'].unique()))
social_platform = st.sidebar.selectbox('Plateforme principale', ['Toutes'] + list(df['What is your primary social media platform?'].unique()))

# Apply filters
if age_group != 'Tous':
    df = df[df['What is your age group?'] == age_group]

if social_platform != 'Toutes':
    df = df[df['What is your primary social media platform?'] == social_platform]

# Analytics
analytics_options = [
    "Répartition démographique",
    "Comportement sur les réseaux sociaux",
    "Perception de la marque",
    "Engagement et Interactivité",
    "Actions inspirées",
    "Service client et réactivité",
    "Stratégie Marketing",
    "Pertinence et tendances",
    "Utilisation des données clients",
    "Réglementation et sensibilité culturelle",
    "Prix et valeur perçue",
    "Inclusivité et innovation"
]

analytics_choice = st.selectbox("Choisissez l'analyse à afficher", analytics_options)

fig, ax = plt.subplots(figsize=(10, 6))

# Define the plot based on the user's selection
if analytics_choice == "Répartition démographique":
    sns.countplot(y='What is your age group?', data=df, palette='coolwarm', ax=ax)
elif analytics_choice == "Comportement sur les réseaux sociaux":
    sns.countplot(y='How frequently do you interact with brands on social media?', data=df, palette='mako', ax=ax)
elif analytics_choice == "Perception de la marque":
    sns.countplot(y='How would you describe your perception of Samsung as a brand?', data=df, palette='cubehelix', ax=ax)
elif analytics_choice == "Engagement et Interactivité":
    sns.countplot(y="How visually appealing is Samsung's social media content?", data=df, palette='rocket', ax=ax)
elif analytics_choice == "Actions inspirées":
    action_counts = df["Have you ever taken action (e.g., visited a website, purchased a product) due to Samsung's social media content?"].value_counts()
    st.bar_chart(action_counts)
elif analytics_choice == "Service client et réactivité":
    sns.countplot(y='How well does Samsung address customer feedback and inquiries on social media?', data=df, palette='crest', ax=ax)
elif analytics_choice == "Stratégie Marketing":
    sns.countplot(y="Do you believe Samsung's social media marketing aligns with its brand image?", data=df, palette='Blues', ax=ax)
elif analytics_choice == "Pertinence et tendances":
    sns.countplot(y="How relevant is Samsung's content to the  trends in the moment ", data=df, palette='flare', ax=ax)
elif analytics_choice == "Utilisation des données clients":
    sns.countplot(y="Do you believe Samsung uses customer data effectively to improve its social media strategies?", data=df, palette='icefire', ax=ax)
elif analytics_choice == "Réglementation et sensibilité culturelle":
    sns.countplot(y="How well do you think Samsung adapts its social media strategies to comply with local regulations (e.g., data privacy laws, advertising policies)", data=df, palette='Spectral', ax=ax)
elif analytics_choice == "Prix et valeur perçue":
    sns.countplot(y="Does Samsung's pricing strategy, as presented on social media, align with the perceived value of its products?", data=df, palette='YlGnBu', ax=ax)
elif analytics_choice == "Inclusivité et innovation":
    sns.countplot(y="How inclusive do you find Samsung's social media campaigns (e.g., representing diverse groups and lifestyles)?", data=df, palette='magma', ax=ax)

st.pyplot(fig)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made by Zineb")
