import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout='wide')

# Charger les données
@st.cache_data
def load_data():
    return pd.read_excel(r"thesis.xlsx", sheet_name='Réponses au formulaire 1')

df = load_data()

# Title and description
st.title("📊 Samsung Social Media Analytics")
st.markdown("#### Interactive Analysis of Samsung's Social Media Questionnaire Responses")

# Sidebar filters
st.sidebar.header("Filters")
age_group = st.sidebar.selectbox('Age Group', ['All'] + list(df['What is your age group?'].unique()))
social_platform = st.sidebar.selectbox('Primary Social Media Platform', ['All'] + list(df['What is your primary social media platform?'].unique()))

# Apply filters
if age_group != 'All':
    df = df[df['What is your age group?'] == age_group]

if social_platform != 'All':
    df = df[df['What is your primary social media platform?'] == social_platform]

# Analytics
analytics_options = [
    "Demographic Distribution",
    "Social Media Behavior",
    "Brand Perception",
    "Engagement and Interactivity",
    "Inspired Actions",
    "Customer Service and Responsiveness",
    "Marketing Strategy",
    "Relevance and Trends",
    "Use of Customer Data",
    "Regulation and Cultural Sensitivity",
    "Pricing and Perceived Value",
    "Inclusivity and Innovation"
]

analytics_choice = st.selectbox("Select Analysis to Display", analytics_options)

fig, ax = plt.subplots(figsize=(10, 6))

# Define the plot based on the user's selection
if analytics_choice == "Demographic Distribution":
    sns.countplot(y='What is your age group?', data=df, palette='coolwarm', ax=ax)
elif analytics_choice == "Social Media Behavior":
    sns.countplot(y='How frequently do you interact with brands on social media?', data=df, palette='mako', ax=ax)
elif analytics_choice == "Brand Perception":
    sns.countplot(y='How would you describe your perception of Samsung as a brand?', data=df, palette='cubehelix', ax=ax)
elif analytics_choice == "Engagement and Interactivity":
    sns.countplot(y="How visually appealing is Samsung's social media content?", data=df, palette='rocket', ax=ax)
elif analytics_choice == "Inspired Actions":
    action_counts = df["Have you ever taken action (e.g., visited a website, purchased a product) due to Samsung's social media content?"].value_counts()
    st.bar_chart(action_counts)
elif analytics_choice == "Customer Service and Responsiveness":
    sns.countplot(y='How well does Samsung address customer feedback and inquiries on social media?', data=df, palette='crest', ax=ax)
elif analytics_choice == "Marketing Strategy":
    sns.countplot(y="Do you believe Samsung's social media marketing aligns with its brand image?", data=df, palette='Blues', ax=ax)
elif analytics_choice == "Relevance and Trends":
    sns.countplot(y="How relevant is Samsung's content to the  trends in the moment ", data=df, palette='flare', ax=ax)
elif analytics_choice == "Use of Customer Data":
    sns.countplot(y="Do you believe Samsung uses customer data effectively to improve its social media strategies?", data=df, palette='icefire', ax=ax)
elif analytics_choice == "Regulation and Cultural Sensitivity":
    sns.countplot(y="How well do you think Samsung adapts its social media strategies to comply with local regulations (e.g., data privacy laws, advertising policies)", data=df, palette='Spectral', ax=ax)
elif analytics_choice == "Pricing and Perceived Value":
    sns.countplot(y="Does Samsung's pricing strategy, as presented on social media, align with the perceived value of its products?", data=df, palette='YlGnBu', ax=ax)
elif analytics_choice == "Inclusivity and Innovation":
    sns.countplot(y="How inclusive do you find Samsung's social media campaigns (e.g., representing diverse groups and lifestyles)?", data=df, palette='magma', ax=ax)

st.pyplot(fig)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made by Zineb")
