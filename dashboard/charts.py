import plotly.express as px


def sentiment_pie_chart(df):

    sentiment_counts = df['Sentiment'].value_counts()

    fig = px.pie(
        names=sentiment_counts.index,
        values=sentiment_counts.values,
        title="Sentiment Distribution"
    )

    return fig


def sentiment_bar_chart(df):

    sentiment_counts = df['Sentiment'].value_counts()

    fig = px.bar(
        x=sentiment_counts.index,
        y=sentiment_counts.values,
        labels={
            'x': 'Sentiment',
            'y': 'Count'
        },
        title='Sentiment Count'
    )

    return fig


def rating_distribution(df):

    ratings = df['overall'].value_counts().sort_index()

    fig = px.bar(
        x=ratings.index,
        y=ratings.values,
        labels={
            'x': 'Star Rating',
            'y': 'Number of Reviews'
        },
        title='Rating Distribution'
    )

    return fig


def sentiment_by_rating(df):

    grouped = (
        df.groupby(['overall', 'Sentiment'])
        .size()
        .reset_index(name='Count')
    )

    fig = px.bar(
        grouped,
        x='overall',
        y='Count',
        color='Sentiment',
        barmode='group',
        title='Sentiment by Rating'
    )

    return fig


def review_length_distribution(df):

    df['review_length'] = (
        df['reviewText']
        .astype(str)
        .apply(len)
    )

    fig = px.histogram(
        df,
        x='review_length',
        nbins=30,
        title='Review Length Distribution'
    )

    return fig