import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import ne_chunk, pos_tag
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
import string

# ==========================
# 1. Train + Save Classifier
# ==========================

# --- Load dataset ---
df = pd.read_csv("news-article-categories.csv")

# --- Clean missing values ---
df["title"] = df["title"].fillna("")
df["body"] = df["body"].fillna("")

# --- Features & labels ---
X = df["title"] + " " + df["body"]
y = df["category"]

# --- Vectorizer + Classifier ---
vectorizer = TfidfVectorizer(stop_words="english", max_features=2000)
X_tfidf = vectorizer.fit_transform(X)

clf = MultinomialNB()
clf.fit(X_tfidf, y)

# --- Save models for reuse ---
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("classifier.pkl", "wb") as f:
    pickle.dump(clf, f)


# ==========================
# 2. NLP Analysis (NLTK)
# ==========================

# Download required resources (first run only)
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)
nltk.download("averaged_perceptron_tagger_eng", quiet=True)
nltk.download("maxent_ne_chunker", quiet=True)
nltk.download("maxent_ne_chunker_tab", quiet=True)
nltk.download("words", quiet=True)
nltk.download("vader_lexicon", quiet=True)


# ---------- INPUT TEXT ----------
text = """
Apple announced the release of the new iPhone today. 
Investors reacted positively, and Apple stock surged by 5%. 
Meanwhile, Samsung is preparing for its own product launch next week. 
Many users are excited about the new features, but some critics argue the design hasn’t changed much. 
The tech industry continues to grow rapidly in the United States and Europe.
"""

# ---------- 1. SENTIMENT ANALYSIS ----------
sia = SentimentIntensityAnalyzer()
sentiment = sia.polarity_scores(text)
print("📌 Sentiment Analysis:", sentiment)

# ---------- 2. KEY INFORMATION EXTRACTION (Named Entities) ----------
tokens = word_tokenize(text)
tags = pos_tag(tokens)
chunks = ne_chunk(tags, binary=False)
print("\n📌 Key Information (Named Entities):")
for chunk in chunks:
    if hasattr(chunk, "label"):
        print(f"{chunk.label()} → {' '.join(c[0] for c in chunk)}")

# ---------- 3. SUMMARIZATION ----------
stop_words = set(stopwords.words("english"))
words = word_tokenize(text.lower())

# Remove stopwords & punctuation
filtered_words = [w for w in words if w not in stop_words and w not in string.punctuation]

# Word frequencies
freq = Counter(filtered_words)

# Sentence scoring
sentence_scores = {}
for sent in sent_tokenize(text):
    for word in word_tokenize(sent.lower()):
        if word in freq:
            sentence_scores[sent] = sentence_scores.get(sent, 0) + freq[word]

# Select top 2 sentences as summary
summary = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:2]
print("\n📌 Summary:")
for s in summary:
    print("-", s)

# ---------- 4. TREND ANALYSIS (Word Frequency) ----------
print("\n📌 Trend Analysis (Most Common Words):")
for word, count in freq.most_common(5):
    print(f"{word}: {count}")
