"""
Live News Prediction Script

This script fetches live news from NewsAPI or RSS feeds and uses the trained
fake news detection model to classify each article as real or fake.
"""

import pandas as pd
import numpy as np
import joblib
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False
import re
import string
from datetime import datetime, timedelta
from config import *
import os
import sys

try:
    from newsapi import NewsApiClient
    NEWSAPI_AVAILABLE = True
except ImportError:
    NEWSAPI_AVAILABLE = False
    print("NewsAPI client not available. Will use RSS feeds only.")

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    print("NLTK not available. Using basic text processing.")

class LiveNewsPredictor:
    """
    A class for fetching live news and predicting fake news.
    """
    
    def __init__(self):
        """Initialize the predictor with pre-trained model."""
        self.model = None
        self.vectorizer = None
        self.newsapi = None
        
        # Initialize text processing tools
        if NLTK_AVAILABLE:
            try:
                self.stop_words = set(stopwords.words('english'))
                self.lemmatizer = WordNetLemmatizer()
            except:
                self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
                self.lemmatizer = None
        else:
            self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
            self.lemmatizer = None
        
        # Initialize NewsAPI client
        if NEWSAPI_AVAILABLE and NEWSAPI_KEY != 'your_newsapi_key_here':
            try:
                self.newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
                print("NewsAPI client initialized successfully.")
            except Exception as e:
                print(f"Failed to initialize NewsAPI: {e}")
                self.newsapi = None
        else:
            print("NewsAPI key not configured. Using RSS feeds only.")
        
        # Load pre-trained model and vectorizer
        self.load_model()
    
    def load_model(self):
        """Load the pre-trained model and vectorizer."""
        try:
            m_path = MODEL_PATH
            v_path = VECTORIZER_PATH
            if not os.path.exists(m_path):
                m_path = os.path.join('fake-news-detector', MODEL_PATH)
                v_path = os.path.join('fake-news-detector', VECTORIZER_PATH)
            
            if os.path.exists(m_path) and os.path.exists(v_path):
                self.model = joblib.load(m_path)
                self.vectorizer = joblib.load(v_path)
                print(f"Model and vectorizer loaded successfully from {m_path}!")
            else:
                print("Model files not found. Please run 'python train_model.py' first.")
                sys.exit(1)
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Please run 'python train_model.py' first.")
            sys.exit(1)
    
    def preprocess_text(self, text):
        """
        Preprocess text data for prediction (same as training).
        
        Args:
            text (str): Raw text to preprocess
            
        Returns:
            str: Preprocessed text
        """
        if pd.isna(text) or not text:
            return ""
        
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove wire datelines and publisher signatures
        text = re.sub(r'^[a-z\s,./\-]+?\s*\((?:reuters)\)\s*[-—–]+\s*', '', text)
        text = re.sub(r'\b(?:reuters|reuter)\b', '', text)
        text = re.sub(r'\b(?:featured image|image via|photo by|read more at|source:|via twitter)\b[^\n.]*', '', text)
        text = re.sub(r'21st century wire', '', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S*@\S*\s?', '', text)
        
        # Remove punctuation and numbers
        text = re.sub(f'[{string.punctuation}0-9]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenization and lemmatization
        if NLTK_AVAILABLE:
            try:
                tokens = word_tokenize(text)
                tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
                
                if self.lemmatizer:
                    tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
                
                return ' '.join(tokens)
            except:
                pass
        
        # Fallback processing
        words = text.split()
        words = [word for word in words if word not in self.stop_words and len(word) > 2]
        return ' '.join(words)
    
    def predict_text(self, text, title=""):
        """
        Predict if a text is fake news or not.
        
        Args:
            text (str): Text content to classify
            title (str): Title of the article (optional)
            
        Returns:
            dict: Prediction results with probability scores
        """
        if not text:
            return {
                'prediction': 'Unknown',
                'confidence': 0.0,
                'fake_probability': 0.5,
                'real_probability': 0.5
            }
        
        # Combine title and text
        combined_text = f"{title} {text}".strip()
        
        # Preprocess text
        processed_text = self.preprocess_text(combined_text)
        
        if not processed_text:
            return {
                'prediction': 'Unknown',
                'confidence': 0.0,
                'fake_probability': 0.5,
                'real_probability': 0.5
            }
        
        try:
            # Vectorize text
            text_tfidf = self.vectorizer.transform([processed_text])
            
            # Get prediction probabilities
            probabilities = self.model.predict_proba(text_tfidf)[0]
            real_prob = probabilities[0]
            fake_prob = probabilities[1]
            
            # Make prediction
            prediction = "Fake" if fake_prob > FAKE_THRESHOLD else "Real"
            confidence = max(real_prob, fake_prob)
            
            return {
                'prediction': prediction,
                'confidence': confidence,
                'fake_probability': fake_prob,
                'real_probability': real_prob
            }
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            return {
                'prediction': 'Error',
                'confidence': 0.0,
                'fake_probability': 0.0,
                'real_probability': 0.0
            }
    
    def fetch_news_from_newsapi(self, query="", max_articles=20):
        """
        Fetch news articles from NewsAPI.
        
        Args:
            query (str): Search query (optional)
            max_articles (int): Maximum number of articles to fetch
            
        Returns:
            list: List of news articles
        """
        articles = []
        
        if self.newsapi is None:
            print("NewsAPI client not initialized. Cannot fetch from NewsAPI.")
            return articles
        
        try:
            # Get top headlines for general news
            if not query:
                print("Fetching top headlines from NewsAPI...")
                response = self.newsapi.get_top_headlines(language='en', page_size=max_articles)
            else:
                # Search for specific query
                print(f"Searching NewsAPI for: {query}")
                response = self.newsapi.get_everything(q=query, language='en', page_size=max_articles, sort_by='relevancy')
            
            if response and 'articles' in response:
                for article in response['articles']:
                    source_name = article['source']['name'] if article['source'] else 'Unknown Source'
                    
                    # Extract article information
                    articles.append({
                        'title': article.get('title', 'No title'),
                        'description': article.get('description', ''),
                        'content': article.get('content', article.get('description', '')),
                        'url': article.get('url', ''),
                        'source': source_name,
                        'published_at': article.get('publishedAt', ''),
                        'url_to_image': article.get('urlToImage', '')
                    })
            
            print(f"Fetched {len(articles)} articles from NewsAPI")
            return articles
            
        except Exception as e:
            print(f"Error fetching from NewsAPI: {e}")
            return articles
    
    def fetch_news_from_rss(self, max_articles=20):
        """
        Fetch news articles from RSS feeds.
        
        Args:
            max_articles (int): Maximum number of articles to fetch
            
        Returns:
            list: List of news articles
        """
        articles = []
        
        for feed_url in RSS_FEEDS:
            try:
                print(f"Fetching from RSS: {feed_url}")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:5]:  # Limit per feed
                    if len(articles) >= max_articles:
                        break
                    
                    # Extract article information
                    title = entry.get('title', 'No title')
                    description = entry.get('description', entry.get('summary', ''))
                    content = description  # RSS usually doesn't have full content
                    url = entry.get('link', '')
                    source = feed.feed.get('title', 'Unknown')
                    published = entry.get('published', '')
                    
                    articles.append({
                        'title': title,
                        'description': description,
                        'content': content,
                        'url': url,
                        'source': source,
                        'published_at': published,
                        'url_to_image': ''
                    })
                
            except Exception as e:
                print(f"Error fetching RSS feed {feed_url}: {e}")
                continue
        
        print(f"Fetched {len(articles)} articles from RSS feeds")
        return articles
    
    def get_live_news_predictions(self, query="", source="auto", max_articles=20):
        """
        Fetch live news and predict fake news.
        
        Args:
            query (str): Search query 
            source (str): News source ('auto', 'newsapi', or 'rss')
            max_articles (int): Maximum articles to process
            
        Returns:
            list: List of articles with predictions
        """
        articles = []
        
        # Auto-select source (prioritizing NewsAPI if available)
        if source == "auto":
            if self.newsapi is not None:
                source = "newsapi"
            else:
                source = "rss"
        
        # Fetch from NewsAPI
        if source == 'newsapi':
            if self.newsapi is not None:
                newsapi_articles = self.fetch_news_from_newsapi(query, max_articles)
                articles.extend(newsapi_articles)
            else:
                print("NewsAPI not available. Falling back to RSS feeds.")
                rss_articles = self.fetch_news_from_rss(max_articles)
                articles.extend(rss_articles)
        
        # Fetch from RSS feeds
        elif source == 'rss':
            rss_articles = self.fetch_news_from_rss(max_articles)
            articles.extend(rss_articles)
        
        # Limit total articles
        articles = articles[:max_articles]
        
        # Make predictions for each article
        results = []
        print(f"\nMaking predictions for {len(articles)} articles...")
        
        for i, article in enumerate(articles, 1):
            print(f"Processing article {i}/{len(articles)}...", end="\r")
            
            # Get prediction
            prediction_result = self.predict_text(
                text=article['content'],
                title=article['title']
            )
            
            # Combine article info with prediction
            result = {
                'title': article['title'],
                'description': article['description'][:200] + '...' if len(article['description']) > 200 else article['description'],
                'source': article['source'],
                'url': article['url'],
                'published_at': article['published_at'],
                'prediction': prediction_result['prediction'],
                'confidence': prediction_result['confidence'],
                'fake_probability': prediction_result['fake_probability'],
                'real_probability': prediction_result['real_probability']
            }
            
            results.append(result)
        
        print(f"\nCompleted predictions for {len(results)} articles.")
        return results
    
    def display_results(self, results, show_details=True):
        """
        Display prediction results in a formatted way.
        
        Args:
            results (list): List of prediction results
            show_details (bool): Whether to show detailed information
        """
        if not results:
            print("No articles found.")
            return
        
        print("\n" + "="*80)
        print(f"FAKE NEWS DETECTION RESULTS - {len(results)} ARTICLES")
        print("="*80)
        
        fake_count = sum(1 for r in results if r['prediction'] == 'Fake')
        real_count = len(results) - fake_count
        
        print(f"Summary: {fake_count} Fake, {real_count} Real")
        print("="*80)
        
        for i, result in enumerate(results, 1):
            status_emoji = "FAKE" if result['prediction'] == 'Fake' else "REAL"
            confidence_bar = "█" * int(result['confidence'] * 10) + "░" * (10 - int(result['confidence'] * 10))
            
            print(f"\n{i}. [{status_emoji}] {confidence_bar} {result['confidence']:.2%}")
            print(f"Title: {result['title']}")
            print(f"Source: {result['source']}")
            
            if show_details:
                print(f"Description: {result['description']}")
                print(f"Fake Probability: {result['fake_probability']:.3f}")
                print(f"Real Probability: {result['real_probability']:.3f}")
                print(f"URL: {result['url'][:60]}..." if len(result['url']) > 60 else f"URL: {result['url']}")
                print("-" * 60)
        
        print("\n" + "="*80)
    
    def get_top_influential_words(self, text, title="", top_n=10):
        """
        Get the most influential words for a prediction.
        
        Args:
            text (str): Article text
            title (str): Article title
            top_n (int): Number of top words to return
            
        Returns:
            dict: Top words with their influence scores
        """
        combined_text = f"{title} {text}".strip()
        processed_text = self.preprocess_text(combined_text)
        
        if not processed_text:
            return {'fake_indicators': [], 'real_indicators': []}
        
        try:
            # Vectorize text
            text_tfidf = self.vectorizer.transform([processed_text])
            
            # Get feature names and their TF-IDF scores
            feature_names = self.vectorizer.get_feature_names_out()
            tfidf_scores = text_tfidf.toarray()[0]
            
            # Get model coefficients
            coefficients = self.model.coef_[0]
            
            # Calculate influence scores (TF-IDF * coefficient)
            influence_scores = tfidf_scores * coefficients
            
            # Create list of (word, influence_score) pairs
            word_influences = [(feature_names[i], influence_scores[i]) 
                             for i in range(len(feature_names)) 
                             if tfidf_scores[i] > 0]
            
            # Sort by influence score
            word_influences.sort(key=lambda x: abs(x[1]), reverse=True)
            
            # Separate fake and real indicators
            fake_indicators = [(word, score) for word, score in word_influences 
                             if score > 0][:top_n]
            real_indicators = [(word, score) for word, score in word_influences 
                             if score < 0][:top_n]
            
            return {
                'fake_indicators': fake_indicators,
                'real_indicators': real_indicators
            }
            
        except Exception as e:
            print(f"Error getting influential words: {e}")
            return {'fake_indicators': [], 'real_indicators': []}

def main():
    """
    Main function to demonstrate live news prediction.
    """
    print("Real-Time Fake News Detection")
    print("=" * 50)
    
    # Initialize predictor
    predictor = LiveNewsPredictor()
    
    while True:
        print("\nOptions:")
        print("1. Fetch and analyze live news")
        print("2. Analyze custom text")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            print("\nFetching live news...")
            max_articles = input("Number of articles to analyze (default 10): ").strip()
            max_articles = int(max_articles) if max_articles.isdigit() else 10
            
            # Get predictions
            results = predictor.get_live_news_predictions(
                query="",
                source="auto",  # Will prioritize NewsAPI if available
                max_articles=max_articles
            )
            
            # Display results
            predictor.display_results(results)
            
        elif choice == '2':
            print("\nCustom Text Analysis")
            title = input("Enter article title: ").strip()
            text = input("Enter article text: ").strip()
            
            if text:
                result = predictor.predict_text(text, title)
                
                print("\n" + "=" * 50)
                print("PREDICTION RESULT")
                print("=" * 50)
                print(f"Prediction: {result['prediction']}")
                print(f"Confidence: {result['confidence']:.2%}")
                print(f"Fake Probability: {result['fake_probability']:.3f}")
                print(f"Real Probability: {result['real_probability']:.3f}")
                
                # Show influential words
                influential = predictor.get_top_influential_words(text, title, top_n=5)
                
                if influential['fake_indicators']:
                    print("\nTop words suggesting FAKE news:")
                    for word, score in influential['fake_indicators']:
                        print(f"  • {word}: {score:.3f}")
                
                if influential['real_indicators']:
                    print("\nTop words suggesting REAL news:")
                    for word, score in influential['real_indicators']:
                        print(f"  • {word}: {abs(score):.3f}")
                
            else:
                print("Please enter some text to analyze.")
            
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
