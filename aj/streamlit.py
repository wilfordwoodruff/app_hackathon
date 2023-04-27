import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("C:/Users/Aj/Documents/GitHub/wasianwilford/Youngwho/joined2.csv")

# Set up streamlit app
st.title("Interactive Data Visualization")

# Filter by book
book_list = df.book_title.unique().tolist()
selected_book = st.sidebar.selectbox("Book", book_list)
filtered_df = df[df.book_title == selected_book]

# Filter by probability
min_prob, max_prob = st.sidebar.slider("Probability", 0.0, 1.0, (0.0, 1.0))
filtered_df = filtered_df[(filtered_df.probability >= min_prob) & (filtered_df.probability <= max_prob)]

# Show filtered data in a table
st.write(filtered_df.head())

# Create a scatter plot of probability vs. verse_short_title
fig = px.scatter(filtered_df, x="verse_short_title", y="probability")
st.plotly_chart(fig, use_container_width=True)

# Create a time series chart of probability over time
time_series_df = filtered_df.groupby("date").mean().reset_index()
fig = px.line(time_series_df, x="date", y="probability")
st.plotly_chart(fig, use_container_width=True)
