import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

#load the data
df = pd.read_csv('my_analysis_output.csv')

#title
st.title("Indian Movies Dashboard !!")
st.subheader("Created by Sahil Kasana")
#search
st.subheader("Search a movie!!")
search_query  = st.text_input("enter the movie name : ")
if search_query:
    search_results = df[df['Movie Name'].str.contains(search_query, case=False, na=False)]
    if not search_results.empty:
        st.write(f"found results are {len(search_results)} movies..")
        st.dataframe(search_results[['Movie Name', 'Year', 'Genre', 'Rating(10)', 'Votes', 'Language']])
    else:
        st.write("No movies are found!! try again")

#2. sidebar filter 
st.sidebar.header("Filter")
# filter by genre
genre_filter = st.sidebar.multiselect('Select Genre',df['Genre'].unique(),default =[])

#apply
if genre_filter:
    df = df[df['Genre'].isin(genre_filter)]

#filter by language
lang_filter = st.sidebar.multiselect('Select Language',df['Language'].unique(),default = [])

#apply
if lang_filter:
    df= df[df['Language'].isin(lang_filter)]

#filter by rating
rate_filter = st.sidebar.slider( 'select your rating',float(df['Rating(10)'].min()), float(df['Rating(10)'].max()), (0.0, 10.0))
df = df[df['Rating(10)'].between(*rate_filter)]


# Filter by Year , vote
year_range = st.sidebar.slider("Select Year Range", int(df['Year'].min()), int(df['Year'].max()), (1950, 2025))
df = df[df['Year'].between(*year_range)]
votes_range = st.sidebar.slider("Select Votes Range", int(df['Votes'].min()), int(df['Votes'].max()), (int(df['Votes'].min()), int(df['Votes'].max())))
df = df[df['Votes'].between(*votes_range)]

# Filtered Data Table
st.subheader("Filtered Movies Data")
st.dataframe(df)

#3, drop visualization
st.subheader("visualizations:-")
visual_option = st.selectbox(
    "Select a visual  !!!",
    [
        "Top 10 Movies by Rating",
        "Top 10 Movies by Votes",
        "Rating Distribution",
        "Votes Distribution",
        "Top Genres by Count",
        "Votes vs. Rating by Language"
    ]
)


# Display Visualizations and Tables Based on Selection
if visual_option == "Top 10 Movies by Rating":
    st.markdown("### Top 10 Movies by Rating")
    top_movies_by_rating = df.sort_values(by='Rating(10)', ascending=False).head(10)
    st.write("Table: Top 10 Movies by Rating")
    st.dataframe(top_movies_by_rating[['Movie Name', 'Rating(10)', 'Year', 'Genre']])
    st.write("Bar Chart: Top 10 Movies by Rating")
    st.write("This graph highlights the top 10 movies with the highest ratings from the dataset.")
    fig = px.bar(top_movies_by_rating, x='Movie Name', y='Rating(10)', title="Top 10 Movies by Rating")
    st.plotly_chart(fig)

elif visual_option == "Top 10 Movies by Votes":
    st.markdown("&&& Top 10 Movies by Votes")
    df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce')
    top_movies_by_votes = df.sort_values(by='Votes', ascending=False).head(10)
    st.write("Table: Top 10 Movies by Votes")
    st.dataframe(top_movies_by_votes[['Movie Name', 'Votes', 'Year', 'Genre']])
    st.write("Pie Chart: Top 10 Movies by Votes")
    st.write("This pie chart shows the top 10 movies with the highest number of votes, indicating their popularity.")
    fig = px.pie(top_movies_by_votes, names='Movie Name', values='Votes', title="Top 10 Movies by Votes")
    st.plotly_chart(fig)

elif visual_option == "Rating Distribution":
    st.markdown("### Rating Distribution")
    st.write("Table: Summary of Ratings")
    st.write(df['Rating(10)'].describe())
    st.write("Chart: Distribution of Ratings")
    st.write("This chart visualizes how movie ratings are distributed across the dataset.")
    fig = px.histogram(df, x='Rating(10)', nbins=20, title="Rating Distribution")
    st.plotly_chart(fig)

elif visual_option == "Votes Distribution":
    st.markdown("### Votes Distribution")
    st.write("Table: Summary of Votes")
    st.write(df['Votes'].describe())
    st.write("Chart: Distribution of Votes")
    st.write("This chart illustrates the distribution of votes received by movies, showcasing their popularity levels.")
    fig = px.histogram(df, x='Votes', nbins=20, log_y=True, title="Votes Distribution")
    st.plotly_chart(fig)

elif visual_option == "Top Genres by Count":
    st.markdown("$$$$ Top Genres by Count")
    genre_counts = df['Genre'].value_counts()
    st.write("Table: Count of Movies by Genre")
    st.dataframe(genre_counts)
    st.write("Chart: Top Genres by Count")
    st.write("This bar chart shows the number of movies in each genre, indicating the most frequent genres in the dataset.")
    fig = px.bar(x=genre_counts.index, y=genre_counts.values, title="Top Genres by Count", labels={'x': 'Genre', 'y': 'Count'})
    st.plotly_chart(fig)

elif visual_option == "Votes vs. Rating by Language":
    st.markdown("$$$$ Votes vs. Rating by Language")
    st.write("Table: Sample Data for Votes and Ratings")
    st.dataframe(df[['Movie Name', 'Votes', 'Rating(10)', 'Language']].head(10))
    st.write("Scatter Plot: Votes vs. Rating by Language")
    st.write("This scatter plot explores the relationship between votes and ratings for movies, categorized by language.")
    fig = px.scatter(
        df,
        x='Votes',
        y='Rating(10)',
        color='Language',
        size='Votes',
        hover_data=['Movie Name', 'Genre'],
        title="Votes vs. Rating by Language"
    )
    st.plotly_chart(fig)
