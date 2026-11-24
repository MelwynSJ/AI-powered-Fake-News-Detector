from predict_live import LiveNewsPredictor
import sys

print('Testing updated NewsAPI integration...')
predictor = LiveNewsPredictor()

if predictor.newsapi:
    print('✅ NewsAPI client initialized successfully')
    print('Testing news fetch...')
    articles = predictor.fetch_news_from_newsapi('', 5)
    if articles:
        print(f'✅ Fetched {len(articles)} articles from NewsAPI')
        title = articles[0]['title']
        source = articles[0]['source']
        print(f'First article: {title[:100]}...')
        print(f'Source: {source}')
        print('✅ NewsAPI integration working correctly!')
    else:
        print('❌ No articles fetched')
else:
    print('❌ NewsAPI client not initialized')
    sys.exit(1)

print('\nTesting auto-prioritization...')
results = predictor.get_live_news_predictions(query="", source="auto", max_articles=3)
if results:
    print(f'✅ Auto-prioritization working - got {len(results)} articles')
    for i, result in enumerate(results[:2], 1):
        title = result['title']
        prediction = result['prediction']
        confidence = result['confidence']
        print(f'{i}. [{prediction}] {confidence:.2%} - {title[:80]}...')
else:
    print('❌ Auto-prioritization failed')
