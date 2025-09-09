import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import ne_chunk, pos_tag
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
import string

# Download required resources (first run only)
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("words")
nltk.download("vader_lexicon")

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

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)
nltk.download("maxent_ne_chunker", quiet=True)
nltk.download("words", quiet=True)
nltk.download("vader_lexicon", quiet=True)
