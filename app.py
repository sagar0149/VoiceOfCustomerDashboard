
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from models.preprocessing import clean_text
from models.sentiment import get_sentiment
from models.topic_model import extract_keywords

from dashboard.charts import (
    sentiment_pie_chart,
    sentiment_bar_chart,
    rating_distribution,
    sentiment_by_rating,
    review_length_distribution
)

from dashboard.wordcloud_generator import create_wordcloud

st.set_page_config(
    page_title="Voice of Customer Dashboard",
    layout="wide"
)

st.title("📊 Voice of Customer Dashboard")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Detect review column automatically
    possible_review_columns = [
        'reviewText',
        'review',
        'Review',
        'text',
        'comment',
        'feedback'
    ]

    review_column = None

    for col in possible_review_columns:
        if col in df.columns:
            review_column = col
            break

    if review_column is None:
        st.error(
            "No review column found. Please upload a CSV containing a review column."
        )
        st.stop()

    # Clean Reviews
    df['clean_review'] = (
        df[review_column]
        .astype(str)
        .apply(clean_text)
    )

    # Sentiment Analysis
    df['Sentiment'] = (
        df['clean_review']
        .apply(get_sentiment)
    )

    # Dataset Preview
    st.subheader("Dataset Preview")

    columns_to_hide = [
        'unixReviewTime',
        'reviewerID',
        'reviewTime',
        'helpful',
        'asin',
        'clean_review',
        'Unnamed: 0'
    ]

    preview_df = df.drop(
        columns=[col for col in columns_to_hide if col in df.columns]
    )

    preview_columns = []

    if 'overall' in preview_df.columns:
        preview_columns.append('overall')

    if 'summary' in preview_df.columns:
        preview_columns.append('summary')

    preview_columns.append(review_column)
    preview_columns.append('Sentiment')

    st.dataframe(
        preview_df[preview_columns].head(10),
        use_container_width=True
    )

    st.write(f"### Total Reviews: {len(df)}")

    # Metrics
    positive = len(df[df['Sentiment'] == "Positive"])
    negative = len(df[df['Sentiment'] == "Negative"])
    neutral = len(df[df['Sentiment'] == "Neutral"])

    col1, col2, col3 = st.columns(3)

    col1.metric("Positive Reviews", positive)
    col2.metric("Negative Reviews", negative)
    col3.metric("Neutral Reviews", neutral)

    st.divider()

    st.subheader("📈 Analytics Dashboard")

    # Pie Chart + Bar Chart
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            sentiment_pie_chart(df),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            sentiment_bar_chart(df),
            use_container_width=True
        )

    # Rating Distribution
    if 'overall' in df.columns:
        st.plotly_chart(
            rating_distribution(df),
            use_container_width=True
        )

        st.plotly_chart(
            sentiment_by_rating(df),
            use_container_width=True
        )

    # Review Length Distribution
    if review_column == 'reviewText':
        st.plotly_chart(
            review_length_distribution(df),
            use_container_width=True
        )

    st.divider()

    # Keywords
    keywords = extract_keywords(
        df[review_column].astype(str)
    )

    st.subheader("🔑 Top Keywords")

    st.write(list(keywords))

    st.divider()

    # Word Cloud
    all_text = " ".join(
        df[review_column].astype(str)
    )

    wc = create_wordcloud(all_text)

    fig2, ax = plt.subplots(figsize=(12, 6))

    ax.imshow(wc)

    ax.axis("off")

    st.subheader("☁️ Word Cloud")

    st.pyplot(fig2)

    st.divider()

    # Download Report
    csv = df.to_csv(index=False)

    st.download_button(
        label="📥 Download Analysis Report",
        data=csv,
        file_name="analysis_report.csv",
        mime="text/csv"
    )

