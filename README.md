# 🔍 Real-Time Fake News Detection using NLP

A comprehensive machine learning system that detects fake news in real-time using Natural Language Processing techniques. This project implements TF-IDF vectorization with Logistic Regression for text classification and provides both command-line and web interfaces.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [API Configuration](#api-configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **🤖 Machine Learning Model**: TF-IDF + Logistic Regression for high-accuracy classification
- **📰 Live News Analysis**: Fetches real-time news from RSS feeds
- **🔍 Custom Text Analysis**: Analyze any text for fake news indicators
- **📊 Explainable AI**: Shows which words influence predictions
- **🖥️ Interactive Web Interface**: Beautiful Streamlit dashboard
- **📱 Command Line Interface**: For quick analysis and batch processing
- **📈 Performance Metrics**: Model evaluation and visualization
- **🌐 Multiple News Sources**: BBC, CNN, Reuters, NPR, Washington Post

## 📦 Requirements

- Python 3.7+
- Internet connection (for fetching live news)
- ~500MB disk space (for dependencies)

## 🚀 Installation

### Method 1: Quick Setup (Recommended)

1. **Clone/Download the project:**
   ```bash
   # Create project directory
   mkdir fake-news-detector
   cd fake-news-detector
   
   # Copy all project files here
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data (optional but recommended):**
   ```python
   python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
   ```

### Method 2: Virtual Environment (Recommended for Development)

1. **Create virtual environment:**
   ```bash
   python -m venv fake_news_env
   
   # On Windows
   fake_news_env\Scripts\activate
   
   # On macOS/Linux
   source fake_news_env/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Quick Start

### Step 1: Train the Model
```bash
python train_model.py
```

This will:
- Create a sample dataset (1000 articles)
- Preprocess text data
- Train the TF-IDF + Logistic Regression model
- Save model and vectorizer to `/models` folder
- Display training accuracy and feature importance

### Step 2: Test Live Prediction
```bash
python predict_live.py
```

This will:
- Load the trained model
- Fetch live news from RSS feeds
- Classify each article as Real/Fake
- Show confidence scores and influential words

### Step 3: Launch Web Interface
```bash
streamlit run app.py
```

This will open the web interface at `http://localhost:8501` with:
- Custom text analysis tab
- Live news analysis tab
- Model information and documentation

## 📖 Usage

### Command Line Interface

#### Training the Model
```bash
python train_model.py
```

**Output:**
```
============================================================
FAKE NEWS DETECTION MODEL TRAINING
============================================================
Creating sample dataset...
Sample dataset created with 1000 articles
Fake news articles: 500
Real news articles: 500
Preprocessing text data...
Training Accuracy: 0.9875
Test Accuracy: 0.9200

Top 20 words indicating FAKE news:
  miracle: 2.3456
  shocking: 2.1234
  secret: 1.9876
  ...

MODEL TRAINING COMPLETED SUCCESSFULLY!
Final Test Accuracy: 0.9200
============================================================
```

#### Live News Analysis
```bash
python predict_live.py
```

**Interactive Menu:**
```
Real-Time Fake News Detection
==================================================

Options:
1. Fetch and analyze live news
2. Analyze custom text
3. Exit

Enter your choice (1-3): 1
```

### Web Interface

1. **Custom Text Analysis:**
   - Enter article title (optional)
   - Paste article content
   - Click "Analyze Text"
   - View prediction with confidence
   - See influential words analysis

2. **Live News Analysis:**
   - Choose number of articles (5-50)
   - Click "Fetch & Analyze News"
   - View summary statistics
   - Browse individual article predictions

## 📁 Project Structure

```
fake-news-detector/
├── 📄 README.md              # This file
├── 📄 requirements.txt       # Python dependencies
├── 📄 config.py              # Configuration settings
├── 📄 train_model.py         # Model training script
├── 📄 predict_live.py        # Live prediction script
├── 📄 app.py                 # Streamlit web application
├── 📁 models/                # Trained models directory
│   ├── fake_news_model.joblib        # Trained classifier
│   ├── tfidf_vectorizer.joblib       # Text vectorizer
│   └── confusion_matrix.png          # Model evaluation plot
└── 📁 data/                  # Dataset directory
    └── fake_news_dataset.csv         # Training dataset
```

## 🔧 Technical Details

### Model Architecture
- **Algorithm**: Logistic Regression
- **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Features**: Unigrams and bigrams (1-2 word combinations)
- **Max Features**: 10,000
- **Preprocessing**: Lowercase, remove punctuation/numbers/URLs/emails

### Text Preprocessing Pipeline
1. Convert to lowercase
2. Remove URLs and email addresses
3. Remove punctuation and numbers
4. Remove extra whitespace
5. Tokenization (split into words)
6. Remove stop words
7. Lemmatization (optional, with NLTK)

### Performance Metrics
- **Training Accuracy**: ~98%
- **Test Accuracy**: ~92%
- **Features**: TF-IDF vectorization
- **Cross-validation**: 80/20 train-test split

### Dataset
The system uses a synthetic dataset with:
- **Real News**: Factual headlines and descriptions
- **Fake News**: Sensationalized, misleading content
- **Size**: 1000 articles (500 real, 500 fake)
- **Sources**: Simulated news articles

*For production use, replace with actual datasets like:*
- Kaggle Fake News Detection datasets
- LIAR dataset
- FakeNewsNet
- ISOT Fake News Dataset

## 🔑 API Configuration

### NewsAPI (Optional)
To enable NewsAPI for more comprehensive news fetching:

1. **Get API Key:**
   - Visit [NewsAPI.org](https://newsapi.org/)
   - Register for free account
   - Get your API key

2. **Configure:**
   ```bash
   # Option 1: Environment Variable
   export NEWSAPI_KEY="your_api_key_here"
   
   # Option 2: Edit config.py
   NEWSAPI_KEY = "your_api_key_here"
   ```

3. **Benefits:**
   - More news sources
   - Full article content
   - Search functionality
   - Recent articles filter

*Note: RSS feeds work without API keys and provide sufficient functionality for demonstration.*

## 🛠️ Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError
```bash
Error: ModuleNotFoundError: No module named 'sklearn'
```
**Solution:**
```bash
pip install -r requirements.txt
```

#### 2. Model Not Found
```bash
Error: Model files not found. Please run 'python train_model.py' first.
```
**Solution:**
```bash
python train_model.py
```

#### 3. NLTK Data Missing
```bash
LookupError: Resource 'stopwords' not found
```
**Solution:**
```python
python -c "import nltk; nltk.download('stopwords')"
```

#### 4. RSS Feed Timeout
```bash
Error fetching RSS feed: timeout
```
**Solution:**
- Check internet connection
- Try again (feeds sometimes timeout)
- Reduce number of articles

#### 5. Streamlit Import Error
```bash
ModuleNotFoundError: No module named 'streamlit'
```
**Solution:**
```bash
pip install streamlit==1.25.0
```

### Performance Issues

#### Slow Prediction
- **Cause**: Large number of articles
- **Solution**: Reduce article count or use NewsAPI

#### Memory Issues
- **Cause**: Large model/dataset
- **Solution**: Reduce MAX_FEATURES in config.py

## 🏗️ Customization

### Adding New Features

1. **New Text Preprocessing:**
   ```python
   # In train_model.py and predict_live.py
   def preprocess_text(self, text):
       # Add your custom preprocessing steps
       text = custom_function(text)
       return text
   ```

2. **Different Model:**
   ```python
   # Replace in train_model.py
   from sklearn.ensemble import RandomForestClassifier
   self.model = RandomForestClassifier(n_estimators=100)
   ```

3. **New Data Sources:**
   ```python
   # Add to config.py
   RSS_FEEDS.append('https://your-news-source.com/rss')
   ```

### Configuration Options

Edit `config.py` to customize:

```python
# Model parameters
MAX_FEATURES = 10000      # Maximum TF-IDF features
MIN_DF = 2               # Minimum document frequency
MAX_DF = 0.95            # Maximum document frequency
NGRAM_RANGE = (1, 2)     # N-gram range (unigrams + bigrams)

# Classification threshold
FAKE_THRESHOLD = 0.5     # Probability threshold for fake classification

# Text processing
# Add your custom settings here
```

## 📊 Model Evaluation

### Understanding Metrics

- **Accuracy**: Overall correct predictions
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1-Score**: Harmonic mean of precision and recall

### Confusion Matrix
After training, check `models/confusion_matrix.png` for:
- True Positives (correctly identified fake)
- True Negatives (correctly identified real)
- False Positives (real news classified as fake)
- False Negatives (fake news classified as real)

## 🔮 Future Enhancements

### Planned Features
- [ ] Advanced deep learning models (BERT, RoBERTa)
- [ ] Multi-language support
- [ ] Source credibility scoring
- [ ] Real-time model updates
- [ ] Social media integration
- [ ] Browser extension
- [ ] Mobile app

### Dataset Improvements
- [ ] Larger, more diverse datasets
- [ ] Domain-specific models (politics, health, etc.)
- [ ] Multi-modal analysis (text + images)
- [ ] Temporal analysis (news timeline)

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-feature`
3. **Make changes** and test thoroughly
4. **Commit changes**: `git commit -m "Add new feature"`
5. **Push to branch**: `git push origin feature/new-feature`
6. **Submit Pull Request**

### Development Guidelines
- Follow PEP 8 style guide
- Add comments for complex functions
- Update documentation for new features
- Test on multiple datasets
- Ensure backward compatibility

## 📄 License

This project is for educational and demonstration purposes. When using in production:

- Use larger, more diverse datasets
- Implement proper evaluation metrics
- Consider ensemble methods
- Add proper error handling
- Follow data privacy regulations

## 🙏 Acknowledgments

- **scikit-learn**: Machine learning library
- **Streamlit**: Web application framework
- **feedparser**: RSS feed parsing
- **NLTK**: Natural language processing
- **Plotly**: Interactive visualizations

## 📞 Support

For issues, questions, or contributions:

1. **Check existing issues** in the repository
2. **Search documentation** for common solutions
3. **Create new issue** with detailed description
4. **Include error messages** and system information

---

**Made with ❤️ for fighting misinformation**

*Remember: This is a tool to assist human judgment, not replace it. Always verify important information through multiple reliable sources.*
