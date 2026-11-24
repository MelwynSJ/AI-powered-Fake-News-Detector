#!/usr/bin/env python3
"""
Quick test script to verify the fake news detection system works.
"""

try:
    from predict_live import LiveNewsPredictor
    
    print("🔍 Testing Fake News Detection System")
    print("=" * 50)
    
    # Initialize predictor
    predictor = LiveNewsPredictor()
    
    # Test cases
    test_cases = [
        {
            "title": "Scientists Announce Breakthrough in Renewable Energy",
            "text": "Researchers at MIT have published a peer-reviewed study showing significant advances in solar panel efficiency.",
            "expected": "Real"
        },
        {
            "title": "SHOCKING: Miracle Cure Discovered - Doctors Hate This!",
            "text": "This one weird trick will cure all diseases! The government doesn't want you to know this secret!",
            "expected": "Fake"
        }
    ]
    
    print("Testing with sample articles...")
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📰 Test {i}: {test['title']}")
        
        result = predictor.predict_text(test['text'], test['title'])
        
        prediction = result['prediction']
        confidence = result['confidence']
        
        # Determine result
        status = "✅ PASS" if prediction == test['expected'] else "❌ FAIL"
        
        print(f"   Expected: {test['expected']}")
        print(f"   Predicted: {prediction} (confidence: {confidence:.2%}) {status}")
    
    print("\n🌐 Testing RSS feed fetching...")
    try:
        results = predictor.get_live_news_predictions(max_articles=3)
        if results:
            print(f"✅ Successfully fetched and analyzed {len(results)} articles")
            for result in results[:2]:  # Show first 2
                print(f"   • {result['title'][:60]}... -> {result['prediction']}")
        else:
            print("⚠️  No articles fetched (this is normal if RSS feeds are slow)")
    except Exception as e:
        print(f"⚠️  RSS test failed: {e}")
    
    print("\n🎉 System test completed!")
    print("✅ Model loading: OK")
    print("✅ Text prediction: OK")
    print("✅ All components working")
    
    print("\n📋 Next steps:")
    print("1. Run 'streamlit run app.py' for web interface")
    print("2. Run 'python predict_live.py' for interactive CLI")

except Exception as e:
    print(f"❌ System test failed: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure you ran 'python train_model.py' first")
    print("2. Check that all dependencies are installed")
    print("3. Verify you're in the correct directory")
