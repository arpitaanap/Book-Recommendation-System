import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from src.recommend import recommend_books

# Load dataset
books = pd.read_csv('data/books.csv')

# Page config
st.set_page_config(page_title="Book Recommender", layout="wide")

# 🎨 Custom Header
st.markdown("<h1 style='color:#ff4b4b;'>📚 Book Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#00c4ff;'>Discover your next favorite book using AI ✨</p>", unsafe_allow_html=True)

# 🔷 Sidebar Navigation
st.sidebar.markdown("<h2 style='color:#ff4b4b;'>📚 Navigation</h2>", unsafe_allow_html=True)
option = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "🔍 Recommend", "🔥 Trending"]
)

# 🏠 HOME SECTION (WITH VISUALIZATION)
if option == "🏠 Home":
    st.markdown("<h2 style='color:#00c4ff;'>Welcome 👋</h2>", unsafe_allow_html=True)
    st.write("Find personalized book recommendations easily!")

    # 📊 KPIs
    st.markdown("<h3 style='color:#f1c40f;'>📊 Key Insights</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📚 Total Books", books.shape[0])

    with col2:
        st.metric("⭐ Avg Rating", round(books['average_rating'].mean(), 2))

    with col3:
        top_book = books.loc[books['average_rating'].idxmax()]['title']
        st.metric("🏆 Top Book", top_book[:20] + "...")

    # 📈 Rating Distribution
    st.markdown("<h3 style='color:#f1c40f;'>📈 Rating Distribution</h3>", unsafe_allow_html=True)
    st.bar_chart(books['average_rating'].value_counts().sort_index())

    # 🔥 Top 10 Books Chart
    st.markdown("<h3 style='color:#f1c40f;'>🔥 Top Rated Books</h3>", unsafe_allow_html=True)

    top10 = books.sort_values(by='average_rating', ascending=False).head(10)
    chart_data = top10[['title', 'average_rating']].set_index('title')

    st.bar_chart(chart_data)

# 🔍 RECOMMEND SECTION
elif option == "🔍 Recommend":

    st.markdown("<h2 style='color:#00c4ff;'>Find Similar Books 📖</h2>", unsafe_allow_html=True)

    book = st.selectbox("📖 Select a Book", books['title'].values)

    if st.button("🚀 Recommend"):
        with st.spinner("Finding best recommendations..."):
            results = recommend_books(book)

        st.info("💡 Recommendations based on user similarity and ratings")

        st.markdown("<h3 style='color:#f1c40f;'>✨ Recommended Books</h3>", unsafe_allow_html=True)

        cols = st.columns(5)

        for i, b in enumerate(results):
            book_data = books[books['title'] == b]

            with cols[i % 5]:
                if not book_data.empty:
                    st.image(book_data['image_url'].values[0], width=120)

                    st.markdown(f"""
                    <div style="background-color:#262730;padding:8px;border-radius:8px;text-align:center">
                        <p style="color:white;font-size:13px;margin:5px 0;">{b[:30]}...</p>
                        <p style="color:#f1c40f;font-size:12px;">⭐ {round(book_data['average_rating'].values[0], 2)}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write(b)

# 🔥 TRENDING SECTION
elif option == "🔥 Trending":

    st.markdown("<h2 style='color:#00c4ff;'>🔥 Trending Books</h2>", unsafe_allow_html=True)

    top_books = books.sort_values(by='average_rating', ascending=False).head(10)

    cols = st.columns(5)

    for i, (_, row) in enumerate(top_books.iterrows()):
        with cols[i % 5]:
            st.image(row['image_url'], width=120)

            st.markdown(f"""
            <div style="background-color:#262730;padding:8px;border-radius:8px;text-align:center">
                <p style="color:white;font-size:13px;margin:5px 0;">{row['title'][:30]}...</p>
                <p style="color:#f1c40f;font-size:12px;">⭐ {round(row['average_rating'], 2)}</p>
            </div>
            """, unsafe_allow_html=True)

# 🔻 Footer
st.markdown("---")
st.markdown("<p style='text-align:center;color:gray;'>Made with ❤️ by Arpita | Book Recommendation System</p>", unsafe_allow_html=True)