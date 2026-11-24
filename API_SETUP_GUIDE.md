# 🔑 API Keys Setup Guide

## Complete Guide to Setting Up Social Media APIs for Fake News Detection

This guide will walk you through obtaining API keys for all supported platforms and configuring your `.env` file securely.

---

## 📋 Quick Setup Checklist

- [ ] NewsAPI (Free - 1000 requests/day)
- [ ] Twitter/X API (Free tier available)
- [ ] Reddit API (Free)
- [ ] Configure `.env` file
- [ ] Test connections

---

## 📰 NewsAPI Setup (Required)

**What it provides:** Access to 80,000+ news sources worldwide

### Step 1: Get NewsAPI Key
1. Visit [newsapi.org](https://newsapi.org/)
2. Click "Get API Key"
3. Sign up with your email
4. Verify your email
5. Copy your API key

### Step 2: Add to .env file
```env
NEWSAPI_KEY=your_actual_newsapi_key_here
ENABLE_NEWSAPI=true
```

**Free Tier Limits:**
- 1,000 requests per day
- Up to 1 month of historical data
- All news sources included

---

## 🐦 Twitter/X API v2 Setup (Optional but Recommended)

**What it provides:** Real-time tweets, trending topics, user data

### Step 1: Apply for Developer Account
1. Visit [developer.twitter.com](https://developer.twitter.com/)
2. Click "Apply for a developer account"
3. Fill out the application form:
   - **Use Case:** Academic research/Educational project
   - **Description:** "Building a fake news detection system for educational purposes"
   - **Will you analyze Twitter data?** Yes
   - **Will you use Tweet, Retweet, Like, Follow, or Direct Message functionality?** No (just reading)

### Step 2: Create an App
1. Once approved, go to the Developer Portal
2. Click "Create an App"
3. Fill out app details:
   - **App Name:** `Fake-News-Detector-YourName`
   - **Description:** "Educational fake news detection system using NLP"
   - **Website URL:** `https://github.com/yourusername/fake-news-detector` (or your GitHub)

### Step 3: Generate Keys
1. Go to your app settings
2. Navigate to "Keys and tokens" tab
3. Generate:
   - API Key and Secret
   - Bearer Token
   - Access Token and Secret (if needed)

### Step 4: Add to .env file
```env
TWITTER_BEARER_TOKEN=your_bearer_token_here
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
ENABLE_TWITTER=true
```

**Free Tier Limits (Essential Access):**
- 500,000 tweets per month
- 300 requests per 15 minutes (search)
- Real-time tweet access

---

## 🤖 Reddit API Setup (Recommended)

**What it provides:** Reddit posts, comments, subreddit data

### Step 1: Create Reddit App
1. Visit [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Scroll down and click "Create App" or "Create Another App"
3. Fill out the form:
   - **Name:** `fake-news-detector`
   - **App type:** Choose "script"
   - **Description:** "Educational fake news detection system"
   - **About URL:** (leave blank)
   - **Redirect URI:** `http://localhost:8080`
4. Click "Create app"

### Step 2: Get Credentials
After creating the app, you'll see:
- **Client ID:** The string under your app name (looks like: `abcdefg123456`)
- **Client Secret:** Click "edit" to reveal the secret

### Step 3: Add to .env file
```env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=fake_news_detector_v1.0_by_YourRedditUsername
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
ENABLE_REDDIT=true
```

**Free Tier Limits:**
- 100 requests per minute
- No daily limits
- Full access to public Reddit data

---

## 📱 Facebook API Setup (Optional)

**What it provides:** Facebook posts, pages, public content

### Step 1: Create Facebook Developer Account
1. Visit [developers.facebook.com](https://developers.facebook.com/)
2. Click "Get Started"
3. Log in with your Facebook account
4. Complete developer registration

### Step 2: Create an App
1. Click "Create App"
2. Choose "Consumer" or "Business"
3. Fill out app details:
   - **Display Name:** `Fake News Detector`
   - **Contact Email:** Your email
   - **App Purpose:** Research or Educational

### Step 3: Get Access Token
1. Go to Graph API Explorer
2. Generate a User Access Token
3. Select permissions: `pages_read_engagement`, `pages_show_list`

### Step 4: Add to .env file
```env
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token_here
ENABLE_FACEBOOK=true
```

---

## 🔔 Telegram Bot Setup (Optional)

**What it provides:** Telegram channel monitoring, bot notifications

### Step 1: Create Bot
1. Open Telegram and search for `@BotFather`
2. Start a conversation and send `/newbot`
3. Follow the instructions to name your bot
4. Copy the provided bot token

### Step 2: Add to .env file
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
ENABLE_TELEGRAM=true
```

---

## ⚙️ Complete .env File Template

Create a `.env` file in your project directory and fill it with your actual API keys:

```env
# ========================================
# FAKE NEWS DETECTION - API KEYS
# ========================================

# News API (Required)
NEWSAPI_KEY=your_actual_newsapi_key_here
ENABLE_NEWSAPI=true

# Twitter/X API (Recommended)
TWITTER_BEARER_TOKEN=your_actual_bearer_token_here
TWITTER_API_KEY=your_actual_api_key_here
TWITTER_API_SECRET=your_actual_api_secret_here
TWITTER_ACCESS_TOKEN=your_actual_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_actual_access_token_secret_here
ENABLE_TWITTER=true

# Reddit API (Recommended)
REDDIT_CLIENT_ID=your_actual_client_id_here
REDDIT_CLIENT_SECRET=your_actual_client_secret_here
REDDIT_USER_AGENT=fake_news_detector_v1.0_by_YourRedditUsername
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
ENABLE_REDDIT=true

# Facebook API (Optional)
FACEBOOK_ACCESS_TOKEN=your_actual_facebook_token_here
ENABLE_FACEBOOK=false

# Telegram Bot (Optional)
TELEGRAM_BOT_TOKEN=your_actual_telegram_token_here
ENABLE_TELEGRAM=false

# Security Settings
MAX_REQUESTS_PER_HOUR=100
ENABLE_CONTENT_FILTERING=true
MIN_ACCOUNT_AGE_DAYS=30
```

---

## 🧪 Testing Your API Setup

Once you've configured your `.env` file, test your connections:

```bash
# Install dependencies first
pip install -r requirements.txt

# Test social media connections
python social_media_fetcher.py

# Test the complete system
python test_system.py
```

---

## 🚨 Security Best Practices

### 1. Keep .env File Private
- **NEVER** commit `.env` to version control
- The `.gitignore` file already excludes it
- Share API keys only through secure channels

### 2. Use Environment Variables in Production
```bash
# On Linux/Mac
export NEWSAPI_KEY="your_key_here"

# On Windows PowerShell
$env:NEWSAPI_KEY="your_key_here"
```

### 3. Rotate Keys Regularly
- Change API keys every 3-6 months
- Immediately rotate if compromised
- Monitor usage in each platform's dashboard

### 4. Respect Rate Limits
- The system automatically handles rate limiting
- Don't make excessive requests
- Monitor your API usage dashboards

---

## 💡 Cost-Free Setup (Minimum Viable)

If you want to try the system without signing up for additional APIs:

```env
# Minimum setup - works with RSS feeds only
NEWSAPI_KEY=your_newsapi_key_here
ENABLE_NEWSAPI=true
ENABLE_TWITTER=false
ENABLE_REDDIT=false
ENABLE_FACEBOOK=false
ENABLE_TELEGRAM=false
```

The system will still work with:
- RSS feeds from major news sources
- NewsAPI integration
- All ML and web interface features

---

## 🔧 Troubleshooting

### Common Issues:

**1. "Invalid API Key" Errors:**
- Double-check key is copied correctly (no extra spaces)
- Verify key is active in the platform's dashboard
- Check if key has required permissions

**2. "Rate Limit Exceeded":**
- Wait for the limit to reset
- Reduce the number of requests
- Upgrade to a paid tier if needed

**3. "Authentication Failed":**
- Verify all required credentials are provided
- Check username/password for Reddit
- Ensure app permissions are correct

**4. "Module Import Errors":**
```bash
pip install -r requirements.txt
```

### Getting Help:

1. Check the platform's documentation
2. Visit their developer forums
3. Contact API support if issues persist

---

## 🎯 What Each API Enables

| Platform | Features | Best For |
|----------|----------|----------|
| **NewsAPI** | 80k+ news sources, headlines, full articles | Professional news analysis |
| **Twitter** | Real-time tweets, trending topics, viral content | Breaking news, public opinion |
| **Reddit** | Discussion threads, community posts | In-depth analysis, niche topics |
| **Facebook** | Pages, public posts | Mainstream social content |
| **Telegram** | Channel monitoring | Alternative news sources |

---

## 🚀 Ready to Launch!

Once you've configured your API keys:

1. **Test the setup:**
   ```bash
   python social_media_fetcher.py
   ```

2. **Launch the web interface:**
   ```bash
   streamlit run app.py
   ```

3. **Try the command line:**
   ```bash
   python predict_live.py
   ```

Your fake news detection system now has access to real-time social media data from multiple platforms! 🎉

---

**Remember:** This is for educational purposes. Always respect platform terms of service and rate limits.
