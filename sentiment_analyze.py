# import nltk
# nltk.download('vader_lexicon')
# Have to install 'vader_lexicon' otherwise this will not work. 

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
import requests


from api_access import google_search

def analyzeTextSentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    
    if compound_score > 0.05:
        return "Positive Sentiment"
    elif compound_score < -0.05:
        return "Negative Sentiment"
    else:
        return "Neutral Sentiment"
    
def scrape_internet():
    search_results = google_search()
    for result in search_results:
        print(f"Title: {result['title']}")
        print(f"URL: {result['link']}")
        print(f"Snippet: {result['snippet']}")
        print()

    for result in search_results:
        url = result['link']
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract main content (adjust based on website structure)
        main_content = extract_main_content(soup)  # Example selector
        if main_content is None:
            pass
        sentiment = analyzeTextSentiment(main_content)
        print(f"Sentiment for {url}: {sentiment}")
        
def extract_main_content(soup):
    # Prioritize article elements
    article = soup.find('article')
    if article:
        return article.get_text()

    # If no article, try common content containers
    main_content = soup.find('div', {'id': 'main-content'}) or \
                    soup.find('div', {'class': 'article-body'})

    # If still not found, extract all text from the body
    if not main_content:
        body = soup.find('body')
        if body:
            main_content = body.get_text()
    else:
        return None

    return main_content.strip()
            
if __name__ == "__main__":
    scrape_internet()
    
