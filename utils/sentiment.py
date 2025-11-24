try:
    from textblob import TextBlob
    from textblob_fr import PatternTagger, PatternAnalyzer
except ImportError:
    # Fallback if textblob_fr is not available
    from textblob import TextBlob
    PatternTagger, PatternAnalyzer = None, None

import re

def analyze_sentiment(text):
    """
    Analyze sentiment of French text using TextBlob with French language support.
    
    Args:
        text (str): Text to analyze
    
    Returns:
        float: Polarity score between -1.0 (Negative) and +1.0 (Positive)
    """
    try:
        # Clean the text - remove HTML tags
        clean_text = re.sub('<[^<]+?>', '', text)
        
        # Create TextBlob with French analyzer if available
        if PatternTagger and PatternAnalyzer:
            blob = TextBlob(clean_text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        else:
            # Fallback to default analyzer
            blob = TextBlob(clean_text)
        
        # Return polarity score
        return blob.sentiment.polarity
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return 0.0  # Return neutral score on error