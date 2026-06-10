from wordcloud import WordCloud

def create_wordcloud(text):

    wc = WordCloud(
        width=800,
        height=400,
        background_color="white"
    )

    return wc.generate(text)