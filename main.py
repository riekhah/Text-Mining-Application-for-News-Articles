from flask import Flask, render_template, request, jsonify
import pickle
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import word_tokenize, pos_tag, ne_chunk, sent_tokenize
from nltk.corpus import stopwords
import string
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load vectorizer and classifier
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("classifier.pkl", "rb") as f:
    clf = pickle.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/button_clicked", methods=["POST"])
def button_clicked():
    print("clicked")
    data = request.get_json()  # receive JSON from JS

    results = {}
    texts = []   # store all news article texts
    keys = []    # track their IDs (news1, news2, ...)

    for key, text in data.items():
        keys.append(key)
        texts.append(text)

        print("\n============================")
        print(f"🔹 Processing {key}: {text}")

        # ---------- 1. CATEGORY PREDICTION ----------
        tfidf = vectorizer.transform([text])
        prediction = clf.predict(tfidf)[0]
        print(f"📌 Predicted Category: {prediction}")

        # ---------- 2. SENTIMENT ANALYSIS ----------
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(text)
        print("📌 Sentiment Analysis:", sentiment)

        # ---------- 3. KEY INFORMATION EXTRACTION ----------
        tokens = word_tokenize(text)
        tags = pos_tag(tokens)
        chunks = ne_chunk(tags, binary=False)
        print("\n📌 Named Entities:")
        entities = []
        for chunk in chunks:
            if hasattr(chunk, "label"):
                entity_text = " ".join(c[0] for c in chunk)
                print(f"{chunk.label()} → {entity_text}")
                entities.append({chunk.label(): entity_text})

        # ---------- 4. SUMMARIZATION ----------
        stop_words = set(stopwords.words("english"))
        words = word_tokenize(text.lower())
        filtered_words = [w for w in words if w not in stop_words and w not in string.punctuation]
        freq = Counter(filtered_words)

        sentence_scores = {}
        for sent in sent_tokenize(text):
            for word in word_tokenize(sent.lower()):
                if word in freq:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + freq[word]

        summary = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:2]
        print("\n📌 Summary:")
        for s in summary:
            print("-", s)

        # ---------- 5. TREND ANALYSIS ----------
        print("\n📌 Trend Analysis (Top Words):")
        common_words = freq.most_common(5)
        for word, count in common_words:
            print(f"{word}: {count}")

        # Save results for this article
        results[key] = {
            "prediction": prediction,
            "sentiment": sentiment,
            "entities": entities,
            "summary": summary,
            "trends": common_words
        }

    # ---------- 6. SIMILARITY ANALYSIS (AFTER LOOP) ----------
    if texts:
        tfidf_matrix = vectorizer.transform(texts)
        sim_matrix = cosine_similarity(tfidf_matrix)

        similarity_results = {}
        for i, k1 in enumerate(keys):
            similarity_results[k1] = {}
            for j, k2 in enumerate(keys):
                if i != j:  # skip self-comparison
                    similarity_results[k1][k2] = round(float(sim_matrix[i, j]), 3)

        results["similarity"] = similarity_results

    return jsonify({
        "message": "Analysis complete!",
        "results": results
    })

if __name__ == "__main__":
    app.run(debug=True)
