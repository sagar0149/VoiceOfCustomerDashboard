from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(reviews):

    vectorizer = TfidfVectorizer(max_features=20)

    X = vectorizer.fit_transform(reviews)

    return vectorizer.get_feature_names_out()