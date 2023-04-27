import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.title('WW Papers')
path = pd.read_csv(r"C:\\Users\\dudgn\\Desktop\\wasianwilford\\Youngwho\\joined.csv")
booksToShow = st.multiselect(label='Which Books?', options= path['internal_id'].unique())

#path2 = path.query('internal_id in options').

displaydf = path.query('internal_id in @booksToShow').groupby('internal_id').verse_short_title.nunique().reset_index()

st.dataframe(displaydf)
                            
books = (alt.Chart(displaydf)
         .mark_bar(color='internal_id')
         .encode(
    x=alt.X('internal_id',axis=alt.Axis(title='Month and Year')),
    y=alt.Y('verse_short_title',axis=alt.Axis(title='Frequency of Book Reference'))
         )
)

st.altair_chart(books)
