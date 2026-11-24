"""
Configuration file for the Fake News Detection system.
API keys are loaded from .env file for security.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ========================================
# NEWS API CONFIGURATION
# ========================================
# Get your free API key from: https://newsapi.org/
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')

# ========================================
# SOCIAL MEDIA API CONFIGURATIONS
# ========================================

# Twitter/X API v2 Configuration
# Get your API keys from: https://developer.twitter.com/
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Reddit API Configuration
# Get your API credentials from: https://www.reddit.com/prefs/apps
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'fake_news_detector_v1.0')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')

# Facebook API Configuration (optional)
FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')

# Telegram Bot Configuration (optional)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Feature flags
ENABLE_TWITTER = os.getenv('ENABLE_TWITTER', 'true').lower() == 'true'
ENABLE_REDDIT = os.getenv('ENABLE_REDDIT', 'true').lower() == 'true'
ENABLE_FACEBOOK = os.getenv('ENABLE_FACEBOOK', 'false').lower() == 'true'
ENABLE_TELEGRAM = os.getenv('ENABLE_TELEGRAM', 'false').lower() == 'true'
ENABLE_NEWSAPI = os.getenv('ENABLE_NEWSAPI', 'true').lower() == 'true'

# RSS Feeds as fallback (only used when NewsAPI is not available)
# These provide limited content compared to original sources via NewsAPI
RSS_FEEDS = [
    'https://feeds.bbci.co.uk/news/rss.xml',
    'https://rss.cnn.com/rss/edition.rss',
    'https://feeds.reuters.com/reuters/topNews',
    'https://feeds.npr.org/1001/rss.xml',
    'https://feeds.washingtonpost.com/rss/world'
]

# Model Configuration
MODEL_PATH = 'models/fake_news_model.joblib'
VECTORIZER_PATH = 'models/tfidf_vectorizer.joblib'

# Data Configuration
DATASET_PATH = 'data/fake_news_dataset.csv'

# Streamlit Configuration
APP_TITLE = "Real-Time Fake News Detection"
APP_DESCRIPTION = """
This application uses Natural Language Processing to detect fake news in real-time.
It features a machine learning model trained on a large dataset of news articles.
"""

# Text preprocessing settings
MAX_FEATURES = 10000
MIN_DF = 2
MAX_DF = 0.95
NGRAM_RANGE = (1, 2)

# Classification threshold
FAKE_THRESHOLD = 0.5  # Probability threshold for fake news classification
