import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

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

# Key stats
st.markdown("### 📈 Key Statistics")
st.write(f"**Total respondents:** {len(df)}")
st.write(f"**Samsung users:** {(df['Are you a Samsung user?'].str.lower() == 'yes').sum()} ({(df['Are you a Samsung user?'].str.lower() == 'yes').mean():.1%})")
st.write(f"**Most used platform:** {df['What is your primary social media platform?'].mode()[0]}")

# Analytics options
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

# Plotting with Plotly for interactivity
plot_column_map = {
    "Demographic Distribution": 'What is your age group?',
    "Social Media Behavior": 'How frequently do you interact with brands on social media?',
    "Brand Perception": 'How would you describe your perception of Samsung as a brand?',
    "Engagement and Interactivity": "How visually appealing is Samsung's social media content?",
    "Inspired Actions": "Have you ever taken action (e.g., visited a website, purchased a product) due to Samsung's social media content?",
    "Customer Service and Responsiveness": 'How well does Samsung address customer feedback and inquiries on social media?',
    "Marketing Strategy": "Do you believe Samsung's social media marketing aligns with its brand image?",
    "Relevance and Trends": "How relevant is Samsung's content to the  trends in the moment ",
    "Use of Customer Data": "Do you believe Samsung uses customer data effectively to improve its social media strategies?",
    "Regulation and Cultural Sensitivity": "How well do you think Samsung adapts its social media strategies to comply with local regulations (e.g., data privacy laws, advertising policies)",
    "Pricing and Perceived Value": "Does Samsung's pricing strategy, as presented on social media, align with the perceived value of its products?",
    "Inclusivity and Innovation": "How inclusive do you find Samsung's social media campaigns (e.g., representing diverse groups and lifestyles)?"
}

selected_column = plot_column_map.get(analytics_choice)

if analytics_choice == "Inspired Actions":
    chart_data = df[selected_column].value_counts().reset_index()
    chart_data.columns = ["Response", "Count"]
    fig = px.bar(chart_data, x="Response", y="Count", hover_data=['Count'], text="Count",
                 labels={"Response": selected_column}, title=analytics_choice)
else:
    chart_data = df[selected_column].value_counts().reset_index()
    chart_data.columns = ["Response", "Count"]
    fig = px.bar(chart_data, x="Count", y="Response", orientation='h', hover_data=['Count'], text="Count",
                 labels={"Response": selected_column}, title=analytics_choice)

fig.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig, use_container_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made by Zineb")
