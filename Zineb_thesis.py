import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# 1) Define the exact age‐group order you want:
AGE_ORDER = [
    "under 18",
    "18-24",
    "25-34",
    "35-44",
    "45-54",
    "55+",
]

# 2) Load & cast your column to an ordered Categorical
@st.cache_data
def load_data():
    df = pd.read_excel("thesis.xlsx", sheet_name="Réponses au formulaire 1")
    # clean & standardize whitespace / case
    df["What is your age group?"] = (
        df["What is your age group?"]
        .astype(str)
        .str.strip()
        .str.lower()
    )
    # cast to ordered categorical
    cat_type = pd.CategoricalDtype(categories=AGE_ORDER, ordered=True)
    df["What is your age group?"] = df["What is your age group?"].astype(cat_type)
    return df

df = load_data()

# --- Sidebar filters ---
st.sidebar.header("Filters")
age_opts = ["All"] + AGE_ORDER
age_group = st.sidebar.selectbox("Age Group", age_opts)

platform_opts = ["All"] + sorted(df["What is your primary social media platform?"].dropna().unique())
social_platform = st.sidebar.selectbox("Primary Social Media Platform", platform_opts)

# Apply filters
filtered = df.copy()
if age_group != "All":
    filtered = filtered[filtered["What is your age group?"] == age_group]
if social_platform != "All":
    filtered = filtered[filtered["What is your primary social media platform?"] == social_platform]

# --- Key stats ---
st.title("📊 Samsung Social Media Analytics")
st.markdown("#### Interactive Analysis of Samsung's Social Media Questionnaire Responses")

st.markdown("### 📈 Key Statistics")
st.write(f"**Total respondents:** {len(filtered)}")
yes_samsung = (filtered["Are you a Samsung user?"].str.lower() == "yes").sum()
st.write(f"**Samsung users:** {yes_samsung} ({yes_samsung/len(filtered):.1%})")
if not filtered["What is your primary social media platform?"].mode().empty:
    st.write(f"**Most used platform:** {filtered['What is your primary social media platform?'].mode()[0]}")

# --- Analytics selector ---
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

# Map each choice to its DataFrame column
plot_column_map = {
    "Demographic Distribution": "What is your age group?",
    "Social Media Behavior": "How frequently do you interact with brands on social media?",
    "Brand Perception": "How would you describe your perception of Samsung as a brand?",
    "Engagement and Interactivity": "How visually appealing is Samsung's social media content?",
    "Inspired Actions": "Have you ever taken action (e.g., visited a website, purchased a product) due to Samsung's social media content?",
    "Customer Service and Responsiveness": "How well does Samsung address customer feedback and inquiries on social media?",
    "Marketing Strategy": "Do you believe Samsung's social media marketing aligns with its brand image?",
    "Relevance and Trends": "How relevant is Samsung's content to the trends in the moment?",
    "Use of Customer Data": "Do you believe Samsung uses customer data effectively to improve its social media strategies?",
    "Regulation and Cultural Sensitivity": "How well do you think Samsung adapts its social media strategies to comply with local regulations (e.g., data privacy laws, advertising policies)?",
    "Pricing and Perceived Value": "Does Samsung's pricing strategy, as presented on social media, align with the perceived value of its products?",
    "Inclusivity and Innovation": "How inclusive do you find Samsung's social media campaigns (e.g., representing diverse groups and lifestyles)?"
}
selected_col = plot_column_map[analytics_choice]

# --- Build & show the chart ---
if analytics_choice == "Demographic Distribution":
    # ensure every age bucket appears (even if count=0)
    counts = (
        filtered[selected_col]
        .value_counts()
        .reindex(AGE_ORDER, fill_value=0)
        .astype(int)
    )
    chart_data = (
        counts
        .rename_axis("Response")
        .reset_index(name="Count")
    )
    fig = px.bar(
        chart_data,
        x="Count",
        y="Response",
        orientation="h",
        text="Count",
        title="Demographic Distribution",
        category_orders={"Response": AGE_ORDER},
    )
    # enforce the array order on the y-axis
    fig.update_layout(
        yaxis=dict(
            categoryorder="array",
            categoryarray=AGE_ORDER
        )
    )
else:
    # generic value_counts for other questions
    chart_data = (
        filtered[selected_col]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Response", selected_col: "Count"})
    )
    if analytics_choice == "Inspired Actions":
        # vertical bar
        fig = px.bar(
            chart_data,
            x="Response",
            y="Count",
            text="Count",
            title=analytics_choice,
        )
    else:
        # horizontal bar
        fig = px.bar(
            chart_data,
            x="Count",
            y="Response",
            orientation="h",
            text="Count",
            title=analytics_choice,
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig, use_container_width=True)

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown("Made by Zineb")
