"""
Social Media Data Fetcher for Fake News Detection

This module handles fetching posts from various social media platforms
including Twitter/X, Reddit, Facebook, and Telegram for fake news analysis.
"""

import tweepy
import praw
import requests
import json
import time
import re
from datetime import datetime, timedelta
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import emoji
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from config import *
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SocialMediaFetcher:
    """Main class for fetching data from multiple social media platforms."""
    
    def __init__(self):
        """Initialize the social media fetcher with API connections."""
        self.twitter_api = None
        self.reddit_api = None
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Initialize platform connections
        if ENABLE_TWITTER:
            self.init_twitter()
        if ENABLE_REDDIT:
            self.init_reddit()
            
        logger.info("Social Media Fetcher initialized")
    
    def init_twitter(self):
        """Initialize Twitter API connection."""
        try:
            if TWITTER_BEARER_TOKEN and TWITTER_API_KEY:
                # Twitter API v2 with tweepy
                self.twitter_api = tweepy.Client(
                    bearer_token=TWITTER_BEARER_TOKEN,
                    consumer_key=TWITTER_API_KEY,
                    consumer_secret=TWITTER_API_SECRET,
                    access_token=TWITTER_ACCESS_TOKEN,
                    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
                    wait_on_rate_limit=True
                )
                
                # Test connection
                user = self.twitter_api.get_me()
                logger.info(f"Twitter API initialized successfully. User: @{user.data.username}")
            else:
                logger.warning("Twitter API credentials not configured")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter API: {e}")
            self.twitter_api = None
    
    def init_reddit(self):
        """Initialize Reddit API connection."""
        try:
            if REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET:
                self.reddit_api = praw.Reddit(
                    client_id=REDDIT_CLIENT_ID,
                    client_secret=REDDIT_CLIENT_SECRET,
                    user_agent=REDDIT_USER_AGENT,
                    username=REDDIT_USERNAME,
                    password=REDDIT_PASSWORD
                )
                
                # Test connection
                user = self.reddit_api.user.me()
                logger.info(f"Reddit API initialized successfully. User: u/{user}")
            else:
                logger.warning("Reddit API credentials not configured")
        except Exception as e:
            logger.error(f"Failed to initialize Reddit API: {e}")
            self.reddit_api = None

class TwitterFetcher(SocialMediaFetcher):
    """Specialized class for fetching Twitter/X data."""
    
    def fetch_trending_topics(self, woeid=1):  # 1 = Worldwide
        """Fetch trending topics from Twitter."""
        if not self.twitter_api:
            return []
        
        try:
            # Note: Trending topics require API v1.1, this is a placeholder
            # In real implementation, you'd use the trends endpoint
            logger.info("Fetching trending topics...")
            return ["#BreakingNews", "#Politics", "#Health", "#Technology", "#Climate"]
        except Exception as e:
            logger.error(f"Error fetching trending topics: {e}")
            return []
    
    def fetch_tweets_by_keyword(self, keyword, max_results=10):
        """Fetch recent tweets by keyword."""
        if not self.twitter_api:
            return []
        
        try:
            tweets_data = []
            
            # Search for recent tweets
            tweets = self.twitter_api.search_recent_tweets(
                query=f"{keyword} -is:retweet lang:en",
                max_results=max_results,
                tweet_fields=['created_at', 'author_id', 'public_metrics', 'context_annotations'],
                user_fields=['name', 'username', 'verified', 'public_metrics'],
                expansions=['author_id']
            )
            
            if tweets.data:
                # Create a user lookup dict
                users = {user.id: user for user in tweets.includes.get('users', [])}
                
                for tweet in tweets.data:
                    author = users.get(tweet.author_id, {})
                    
                    tweet_info = {
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'author_id': tweet.author_id,
                        'author_name': getattr(author, 'name', 'Unknown'),
                        'author_username': getattr(author, 'username', 'unknown'),
                        'author_verified': getattr(author, 'verified', False),
                        'retweet_count': tweet.public_metrics.get('retweet_count', 0),
                        'like_count': tweet.public_metrics.get('like_count', 0),
                        'reply_count': tweet.public_metrics.get('reply_count', 0),
                        'quote_count': tweet.public_metrics.get('quote_count', 0),
                        'platform': 'Twitter',
                        'url': f"https://twitter.com/{getattr(author, 'username', 'unknown')}/status/{tweet.id}"
                    }
                    
                    # Add sentiment analysis
                    tweet_info.update(self.analyze_text_sentiment(tweet.text))
                    
                    tweets_data.append(tweet_info)
            
            logger.info(f"Fetched {len(tweets_data)} tweets for keyword: {keyword}")
            return tweets_data
            
        except Exception as e:
            logger.error(f"Error fetching tweets for keyword '{keyword}': {e}")
            return []
    
    def fetch_user_tweets(self, username, max_results=10):
        """Fetch recent tweets from a specific user."""
        if not self.twitter_api:
            return []
        
        try:
            tweets_data = []
            
            # Get user first
            user = self.twitter_api.get_user(username=username)
            if not user.data:
                logger.error(f"User @{username} not found")
                return []
            
            # Get user tweets
            tweets = self.twitter_api.get_users_tweets(
                id=user.data.id,
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics', 'context_annotations'],
                exclude=['retweets', 'replies']
            )
            
            if tweets.data:
                for tweet in tweets.data:
                    tweet_info = {
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'author_id': user.data.id,
                        'author_name': user.data.name,
                        'author_username': user.data.username,
                        'author_verified': getattr(user.data, 'verified', False),
                        'retweet_count': tweet.public_metrics.get('retweet_count', 0),
                        'like_count': tweet.public_metrics.get('like_count', 0),
                        'reply_count': tweet.public_metrics.get('reply_count', 0),
                        'quote_count': tweet.public_metrics.get('quote_count', 0),
                        'platform': 'Twitter',
                        'url': f"https://twitter.com/{user.data.username}/status/{tweet.id}"
                    }
                    
                    # Add sentiment analysis
                    tweet_info.update(self.analyze_text_sentiment(tweet.text))
                    
                    tweets_data.append(tweet_info)
            
            logger.info(f"Fetched {len(tweets_data)} tweets from @{username}")
            return tweets_data
            
        except Exception as e:
            logger.error(f"Error fetching tweets from @{username}: {e}")
            return []

class RedditFetcher(SocialMediaFetcher):
    """Specialized class for fetching Reddit data."""
    
    def fetch_subreddit_posts(self, subreddit_name, sort='hot', limit=10):
        """Fetch posts from a specific subreddit."""
        if not self.reddit_api:
            return []
        
        try:
            posts_data = []
            subreddit = self.reddit_api.subreddit(subreddit_name)
            
            # Get posts based on sort method
            if sort == 'hot':
                posts = subreddit.hot(limit=limit)
            elif sort == 'new':
                posts = subreddit.new(limit=limit)
            elif sort == 'top':
                posts = subreddit.top(time_filter='day', limit=limit)
            else:
                posts = subreddit.hot(limit=limit)
            
            for post in posts:
                # Skip stickied posts
                if post.stickied:
                    continue
                
                post_info = {
                    'id': post.id,
                    'title': post.title,
                    'text': post.selftext if post.selftext else post.title,
                    'created_at': datetime.fromtimestamp(post.created_utc),
                    'author': str(post.author) if post.author else '[deleted]',
                    'subreddit': subreddit_name,
                    'score': post.score,
                    'upvote_ratio': post.upvote_ratio,
                    'num_comments': post.num_comments,
                    'platform': 'Reddit',
                    'url': f"https://reddit.com{post.permalink}",
                    'is_video': post.is_video,
                    'is_self': post.is_self,
                    'over_18': post.over_18
                }
                
                # Add sentiment analysis
                text_to_analyze = f"{post.title} {post.selftext}".strip()
                post_info.update(self.analyze_text_sentiment(text_to_analyze))
                
                posts_data.append(post_info)
            
            logger.info(f"Fetched {len(posts_data)} posts from r/{subreddit_name}")
            return posts_data
            
        except Exception as e:
            logger.error(f"Error fetching posts from r/{subreddit_name}: {e}")
            return []
    
    def search_reddit_posts(self, query, limit=10):
        """Search Reddit posts by keyword."""
        if not self.reddit_api:
            return []
        
        try:
            posts_data = []
            
            # Search across all subreddits
            search_results = self.reddit_api.subreddit('all').search(
                query, 
                sort='relevance', 
                time_filter='week',
                limit=limit
            )
            
            for post in search_results:
                post_info = {
                    'id': post.id,
                    'title': post.title,
                    'text': post.selftext if post.selftext else post.title,
                    'created_at': datetime.fromtimestamp(post.created_utc),
                    'author': str(post.author) if post.author else '[deleted]',
                    'subreddit': str(post.subreddit),
                    'score': post.score,
                    'upvote_ratio': post.upvote_ratio,
                    'num_comments': post.num_comments,
                    'platform': 'Reddit',
                    'url': f"https://reddit.com{post.permalink}",
                    'search_query': query
                }
                
                # Add sentiment analysis
                text_to_analyze = f"{post.title} {post.selftext}".strip()
                post_info.update(self.analyze_text_sentiment(text_to_analyze))
                
                posts_data.append(post_info)
            
            logger.info(f"Found {len(posts_data)} Reddit posts for query: {query}")
            return posts_data
            
        except Exception as e:
            logger.error(f"Error searching Reddit for '{query}': {e}")
            return []

    def analyze_text_sentiment(self, text):
        """Analyze sentiment of text using VADER and TextBlob."""
        if not text or not text.strip():
            return {
                'sentiment_vader': 'neutral',
                'sentiment_vader_score': 0.0,
                'sentiment_textblob': 'neutral',
                'sentiment_textblob_score': 0.0,
                'language': 'unknown',
                'contains_emoji': False,
                'contains_hashtags': False,
                'contains_mentions': False,
                'contains_urls': False
            }
        
        try:
            # Clean text for analysis
            clean_text = emoji.demojize(text)
            
            # VADER sentiment analysis
            vader_scores = self.sentiment_analyzer.polarity_scores(text)
            vader_compound = vader_scores['compound']
            
            if vader_compound >= 0.05:
                vader_sentiment = 'positive'
            elif vader_compound <= -0.05:
                vader_sentiment = 'negative'
            else:
                vader_sentiment = 'neutral'
            
            # TextBlob sentiment analysis
            blob = TextBlob(clean_text)
            textblob_polarity = blob.sentiment.polarity
            
            if textblob_polarity > 0.1:
                textblob_sentiment = 'positive'
            elif textblob_polarity < -0.1:
                textblob_sentiment = 'negative'
            else:
                textblob_sentiment = 'neutral'
            
            # Language detection
            try:
                language = detect(clean_text)
            except LangDetectException:
                language = 'unknown'
            
            # Content analysis
            contains_emoji = bool(emoji.emoji_count(text))
            contains_hashtags = bool(re.search(r'#\w+', text))
            contains_mentions = bool(re.search(r'@\w+', text))
            contains_urls = bool(re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text))
            
            return {
                'sentiment_vader': vader_sentiment,
                'sentiment_vader_score': vader_compound,
                'sentiment_textblob': textblob_sentiment,
                'sentiment_textblob_score': textblob_polarity,
                'language': language,
                'contains_emoji': contains_emoji,
                'contains_hashtags': contains_hashtags,
                'contains_mentions': contains_mentions,
                'contains_urls': contains_urls
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                'sentiment_vader': 'error',
                'sentiment_vader_score': 0.0,
                'sentiment_textblob': 'error',
                'sentiment_textblob_score': 0.0,
                'language': 'unknown',
                'contains_emoji': False,
                'contains_hashtags': False,
                'contains_mentions': False,
                'contains_urls': False
            }

class SocialMediaAnalyzer:
    """High-level analyzer that combines multiple social media platforms."""
    
    def __init__(self):
        """Initialize the analyzer with platform fetchers."""
        self.twitter_fetcher = TwitterFetcher()
        self.reddit_fetcher = RedditFetcher()
    
    def fetch_trending_news_content(self, max_posts_per_platform=5):
        """Fetch trending content from multiple platforms."""
        all_content = []
        
        # Fetch from Twitter
        if ENABLE_TWITTER and self.twitter_fetcher.twitter_api:
            try:
                # Search for news-related keywords
                news_keywords = ['breaking news', 'urgent', 'developing', 'report', 'announce']
                for keyword in news_keywords[:2]:  # Limit to avoid rate limiting
                    tweets = self.twitter_fetcher.fetch_tweets_by_keyword(keyword, max_posts_per_platform)
                    all_content.extend(tweets)
                    time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.error(f"Error fetching Twitter content: {e}")
        
        # Fetch from Reddit
        if ENABLE_REDDIT and self.reddit_fetcher.reddit_api:
            try:
                # Fetch from news-related subreddits
                news_subreddits = ['news', 'worldnews', 'politics', 'technology']
                for subreddit in news_subreddits[:2]:  # Limit to avoid rate limiting
                    posts = self.reddit_fetcher.fetch_subreddit_posts(subreddit, 'hot', max_posts_per_platform)
                    all_content.extend(posts)
                    time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.error(f"Error fetching Reddit content: {e}")
        
        # Sort by engagement/popularity
        if all_content:
            # Sort by different metrics based on platform
            def sort_key(item):
                if item['platform'] == 'Twitter':
                    return item['like_count'] + item['retweet_count']
                elif item['platform'] == 'Reddit':
                    return item['score']
                return 0
            
            all_content.sort(key=sort_key, reverse=True)
        
        logger.info(f"Fetched {len(all_content)} social media posts total")
        return all_content
    
    def search_social_media(self, query, max_results=10):
        """Search across multiple social media platforms."""
        results = []
        
        # Search Twitter
        if ENABLE_TWITTER and self.twitter_fetcher.twitter_api:
            try:
                tweets = self.twitter_fetcher.fetch_tweets_by_keyword(query, max_results // 2)
                results.extend(tweets)
            except Exception as e:
                logger.error(f"Error searching Twitter: {e}")
        
        # Search Reddit
        if ENABLE_REDDIT and self.reddit_fetcher.reddit_api:
            try:
                posts = self.reddit_fetcher.search_reddit_posts(query, max_results // 2)
                results.extend(posts)
            except Exception as e:
                logger.error(f"Error searching Reddit: {e}")
        
        return results

# Example usage and testing functions
def test_social_media_connections():
    """Test social media API connections."""
    analyzer = SocialMediaAnalyzer()
    
    print("🔍 Testing Social Media Connections")
    print("=" * 50)
    
    # Test Twitter
    if analyzer.twitter_fetcher.twitter_api:
        print("✅ Twitter API: Connected")
        try:
            tweets = analyzer.twitter_fetcher.fetch_tweets_by_keyword("technology", 3)
            print(f"   - Fetched {len(tweets)} sample tweets")
        except Exception as e:
            print(f"   - Error testing Twitter: {e}")
    else:
        print("❌ Twitter API: Not configured or failed")
    
    # Test Reddit  
    if analyzer.reddit_fetcher.reddit_api:
        print("✅ Reddit API: Connected")
        try:
            posts = analyzer.reddit_fetcher.fetch_subreddit_posts("technology", limit=3)
            print(f"   - Fetched {len(posts)} sample posts")
        except Exception as e:
            print(f"   - Error testing Reddit: {e}")
    else:
        print("❌ Reddit API: Not configured or failed")
    
    print("\n🎉 Social media connection test completed!")

if __name__ == "__main__":
    test_social_media_connections()
