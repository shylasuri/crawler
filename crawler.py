"""
Business Intelligence Web Crawler
----------------------------------
Scrapes business news from multiple sources,
cleans the data with Pandas, summarizes articles,
and visualizes article distribution.

Run:
    python crawler.py

Requirements:
    pip install requests beautifulsoup4 pandas matplotlib sumy nltk
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
# import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')  # Headless backend for servers
import matplotlib.pyplot as plt
from datetime import datetime
import time
import os

# ── Summarizer (uses sumy - very simple NLP) ─────────────────────────────────
try:
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lsa import LsaSummarizer
    import nltk
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    SUMY_AVAILABLE = True
except ImportError:
    SUMY_AVAILABLE = False


def summarize_text(text, sentence_count=2):
    """Return a short summary of article text."""
    if not SUMY_AVAILABLE or len(text.split()) < 30:
        # Fallback: return first 150 characters
        return text[:150].rsplit(' ', 1)[0] + '...' if len(text) > 150 else text

    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentence_count)
        return ' '.join(str(s) for s in summary)
    except Exception:
        return text[:150] + '...'


# ── Scrapers for each news source ─────────────────────────────────────────────

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}


def scrape_moneycontrol():
    """Scrape headlines from Moneycontrol business section."""
    articles = []
    try:
        url = "https://www.moneycontrol.com/news/business/"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find news list items
        news_items = soup.find_all('li', class_='clearfix')[:10]

        for item in news_items:
            link_tag = item.find('a')
            if not link_tag:
                continue
            title = link_tag.get_text(strip=True)
            link = link_tag.get('href', '')
            if title and len(title) > 20:
                articles.append({
                    'source': 'Moneycontrol',
                    'title': title,
                    'url': link,
                    'category': 'Business',
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')
                })
    except Exception as e:
        print(f"  Moneycontrol error: {e}")
    return articles


def scrape_economic_times():
    """Scrape headlines from Economic Times."""
    articles = []
    try:
        url = "https://economictimes.indiatimes.com/news/economy"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # ET uses 'eachStory' divs
        stories = soup.find_all('div', class_='eachStory')[:10]

        for story in stories:
            link_tag = story.find('a')
            if not link_tag:
                continue
            title = link_tag.get_text(strip=True)
            href = link_tag.get('href', '')
            if href and not href.startswith('http'):
                href = 'https://economictimes.indiatimes.com' + href
            if title and len(title) > 20:
                articles.append({
                    'source': 'Economic Times',
                    'title': title,
                    'url': href,
                    'category': 'Economy',
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')
                })
    except Exception as e:
        print(f"  Economic Times error: {e}")
    return articles


def scrape_business_standard():
    """Scrape headlines from Business Standard."""
    articles = []
    try:
        url = "https://www.business-standard.com/finance"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        headlines = soup.find_all('h2')[:10]
        for h in headlines:
            link_tag = h.find('a')
            if not link_tag:
                continue
            title = h.get_text(strip=True)
            href = link_tag.get('href', '')
            if href and not href.startswith('http'):
                href = 'https://www.business-standard.com' + href
            if title and len(title) > 20:
                articles.append({
                    'source': 'Business Standard',
                    'title': title,
                    'url': href,
                    'category': 'Finance',
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')
                })
    except Exception as e:
        print(f"  Business Standard error: {e}")
    return articles


def scrape_livemint():
    """Scrape headlines from LiveMint."""
    articles = []
    try:
        url = "https://www.livemint.com/market"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        items = soup.find_all('h2', class_='headline')[:10]
        for item in items:
            link_tag = item.find('a')
            if not link_tag:
                continue
            title = item.get_text(strip=True)
            href = link_tag.get('href', '')
            if href and not href.startswith('http'):
                href = 'https://www.livemint.com' + href
            if title and len(title) > 20:
                articles.append({
                    'source': 'LiveMint',
                    'title': title,
                    'url': href,
                    'category': 'Markets',
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')
                })
    except Exception as e:
        print(f"  LiveMint error: {e}")
    return articles


def add_mock_articles_if_empty(all_articles):
    """
    If scraping returned nothing (sites blocked, etc.),
    add mock data so the pipeline still works for demo.
    """
    if len(all_articles) > 5:
        return all_articles

    print("\n  Note: Live scraping returned few results (site blocks bots).")
    print("  Adding mock data to demonstrate the pipeline.\n")

    mock = [
        {'source': 'Moneycontrol', 'title': 'RBI holds repo rate steady amid inflation concerns', 'url': '#', 'category': 'Business', 'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')},
        {'source': 'Moneycontrol', 'title': 'Sensex rises 400 points on foreign inflows', 'url': '#', 'category': 'Business', 'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')},
        {'source': 'Moneycontrol', 'title': 'HDFC Bank Q4 results beat analyst estimates', 'url': '#', 'category': 'Business', 'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')},
        {'source': 'Economic Times', 'title': 'India GDP growth projected at 6.8% for FY26', 'url': '#', 'category': 'Economy', 'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')},
        {'source': 'Economic Times', 'title': 'Startup funding rebounds in Q1 2025', 'url': '#', 'category': 'Economy', 'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')},
        {'source': 'Economic Times', 'title': 'India-UK free trade agreement finalised', 'url': '#', 'category': 'Economy', 'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')},
        {'source': 'Business Standard', 'title': 'Tata Motors electric vehicle sales hit record in March', 'url': '#', 'category': 'Finance', 'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')},
        {'source': 'Business Standard', 'title': 'SEBI tightens F&O regulations for retail investors', 'url': '#', 'category': 'Finance', 'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')},
        {'source': 'Business Standard', 'title': 'Reliance Jio files for IPO, valuation at $112bn', 'url': '#', 'category': 'Finance', 'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')},
        {'source': 'LiveMint', 'title': 'Gold prices cross Rs 95,000 per 10g mark', 'url': '#', 'category': 'Markets', 'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')},
        {'source': 'LiveMint', 'title': 'Nifty IT index surges 3% on strong US earnings', 'url': '#', 'category': 'Markets', 'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')},
        {'source': 'LiveMint', 'title': 'Oil prices dip below $78 on demand slowdown fears', 'url': '#', 'category': 'Markets', 'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M')},
    ]
    return all_articles + mock


# ── Data cleaning with Pandas ─────────────────────────────────────────────────

def clean_data(articles):
    """Use Pandas to clean and deduplicate scraped articles."""
    df = pd.DataFrame(articles)

    if df.empty:
        return df

    # Remove duplicates based on title
    df.drop_duplicates(subset='title', inplace=True)

    # Remove rows where title is too short (navigation links, etc.)
    df = df[df['title'].str.len() > 20]

    # Trim whitespace
    df['title'] = df['title'].str.strip()

    # Reset index
    df.reset_index(drop=True, inplace=True)

    print(f"  Cleaned: {len(df)} unique articles after deduplication")
    return df


# ── Analysis & Visualization ──────────────────────────────────────────────────

def analyze_and_plot(df):
    """Generate analysis charts and save them."""
    os.makedirs('output', exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Business News Intelligence Report', fontsize=16, fontweight='bold', y=1.02)

    # Chart 1: Articles per source (bar chart)
    source_counts = df['source'].value_counts()
    bars = axes[0].bar(source_counts.index, source_counts.values,
                       color=['#2563EB', '#16A34A', '#D97706', '#DC2626'])
    axes[0].set_title('Articles Scraped per Source', fontweight='bold')
    axes[0].set_xlabel('News Source')
    axes[0].set_ylabel('Number of Articles')
    axes[0].tick_params(axis='x', rotation=15)
    for bar, val in zip(bars, source_counts.values):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                     str(val), ha='center', fontsize=11, fontweight='bold')

    # Chart 2: Category distribution (pie chart)
    category_counts = df['category'].value_counts()
    axes[1].pie(category_counts.values, labels=category_counts.index,
                autopct='%1.0f%%', startangle=90,
                colors=['#2563EB', '#16A34A', '#D97706', '#DC2626'])
    axes[1].set_title('Article Distribution by Category', fontweight='bold')

    plt.tight_layout()
    plt.savefig('output/news_analysis.png', dpi=150, bbox_inches='tight')
    ##plt.show()
    print("  Chart saved to output/news_analysis.png")


def generate_brief(df):
    """Generate a structured intelligence brief from article titles."""
    print("\n" + "="*60)
    print("  BUSINESS INTELLIGENCE BRIEF")
    print(f"  Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}")
    print("="*60)

    for source in df['source'].unique():
        source_df = df[df['source'] == source]
        print(f"\n  [{source}] — {len(source_df)} articles")
        print("  " + "-"*40)
        for _, row in source_df.head(3).iterrows():
            print(f"  • {row['title']}")

    print("\n" + "="*60)
    print(f"  Total articles collected: {len(df)}")
    print(f"  Sources covered: {df['source'].nunique()}")
    print(f"  Categories: {', '.join(df['category'].unique())}")
    print("="*60)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("\n  Business Intelligence Web Crawler")
    print("  " + "="*40)
    print("  Scraping news sources...\n")

    all_articles = []

    scrapers = [
        ("Moneycontrol", scrape_moneycontrol),
        ("Economic Times", scrape_economic_times),
        ("Business Standard", scrape_business_standard),
        ("LiveMint", scrape_livemint),
    ]

    for name, scraper_fn in scrapers:
        print(f"  Scraping {name}...")
        articles = scraper_fn()
        print(f"    Found {len(articles)} articles")
        all_articles.extend(articles)
        time.sleep(1)  # polite delay between requests

    # Use mock data if live scraping didn't work
    all_articles = add_mock_articles_if_empty(all_articles)

    print("\n  Cleaning data with Pandas...")
    df = clean_data(all_articles)

    # Save raw data to CSV
    os.makedirs('output', exist_ok=True)
    df.to_csv('output/articles.csv', index=False)
    print("  Raw data saved to output/articles.csv")

    # Generate brief
    generate_brief(df)

    # Plot
    print("\n  Generating analysis charts...")
    analyze_and_plot(df)

    print("\n  Done. Check the 'output/' folder for results.\n")

    
def scrape_news():
    """Called by app.py to get cleaned articles as a list of dicts."""
    all_articles = []

    scrapers = [
        ("Moneycontrol", scrape_moneycontrol),
        ("Economic Times", scrape_economic_times),
        ("Business Standard", scrape_business_standard),
        ("LiveMint", scrape_livemint),
    ]

    for name, scraper_fn in scrapers:
        articles = scraper_fn()
        all_articles.extend(articles)

    all_articles = add_mock_articles_if_empty(all_articles)
    df = clean_data(all_articles)
    return df.to_dict(orient='records')



if __name__ == "__main__":
    main()
    # ── Flask-compatible entry point ──────────────────────────────────────────────
