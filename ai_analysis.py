from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import re
from collections import Counter

# Load models at startup
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
sentiment_analyzer = pipeline("sentiment-analysis")
classifier = pipeline("zero-shot-classification")  # For content classification

def analyze_text(text):
    # Clean and limit text
    clean_text = re.sub(r'\s+', ' ', text).strip()
    
    # Handle empty text case
    if not clean_text:
        return {
            "summary": "No text content available for analysis",
            "sentiment": {"label": "NEUTRAL", "score": 1.0},
            "topics": ["No topics available"],
            "keyword_density": {},
            "classification": {"labels": ["N/A"], "scores": [0.0]}
        }
    
    short_text = clean_text[:2000]  # Increased token limit
    
    # Run analyses
    summary = summarizer(short_text, max_length=150, min_length=50, do_sample=False)[0]['summary_text'] if len(short_text) > 50 else "Text too short for summarization"
    
    # Run sentiment analysis only if text is long enough
    if len(short_text.split()) > 3:
        sentiment = sentiment_analyzer(short_text)[0]
    else:
        sentiment = {"label": "NEUTRAL", "score": 1.0}
    
    # Keyword density
    words = re.findall(r'\b\w{3,}\b', clean_text.lower())
    word_freq = Counter(words)
    top_keywords = dict(word_freq.most_common(10))
    
    # Content classification (only if text is long enough)
    classification = {"labels": ["N/A"], "scores": [0.0]}
    if len(short_text.split()) > 5:
        try:
            categories = ["Technology", "Business", "Entertainment", "Health", "Education", "News"]
            classification = classifier(short_text, categories, multi_label=False)
        except Exception as e:
            print(f"Classification failed: {str(e)}")
    
    # Robust topic modeling for single documents
    topics = []
    try:
        # Adjust vectorizer for single document processing
        vectorizer = CountVectorizer(stop_words='english', max_features=500)
        tf = vectorizer.fit_transform([clean_text])
        
        if tf.shape[1] > 5:  # Ensure we have enough features
            n_components = min(3, tf.shape[1])
            lda = LatentDirichletAllocation(n_components=n_components, random_state=42)
            lda.fit(tf)
            
            for idx, topic in enumerate(lda.components_):
                top_words = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-5:]]
                topics.append(f"Topic {idx+1}: {', '.join(top_words)}")
        else:
            topics.append("Insufficient content for topic modeling")
            
    except ValueError as e:
        print(f"Topic modeling skipped: {str(e)}")
        topics.append("Topic modeling not available for this content")
    
    return {
        "summary": summary,
        "sentiment": sentiment,
        "topics": topics,
        "keyword_density": top_keywords,
        "classification": classification
    }