# Business Intelligence Web Crawler

A Python tool that scrapes business news from multiple Indian financial sources, cleans the data using Pandas, and generates structured intelligence briefs with visualizations.

Built as part of a data science internship portfolio.

---

## What it does

- Scrapes headlines from **Moneycontrol, Economic Times, Business Standard, LiveMint**
- Cleans and deduplicates articles using **Pandas**
- Summarizes content using **NLP (sumy / LSA algorithm)**
- Exports structured data to **CSV**
- Generates analysis charts: article distribution by source and category

## Tech Stack

| Tool | Purpose |
|------|---------|
| `requests` + `BeautifulSoup` | Web scraping |
| `Pandas` | Data cleaning, deduplication |
| `sumy` (LSA) | Automatic text summarization |
| `Matplotlib` | Visualization |
| `NLTK` | NLP tokenization |

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/bi-web-crawler
cd bi-web-crawler
pip install -r requirements.txt
python crawler.py
```

## Output

```
output/
├── articles.csv        # All scraped articles (title, source, category, url, timestamp)
└── news_analysis.png   # Bar chart + pie chart of article distribution
```

## Sample Output

```
==============================
  BUSINESS INTELLIGENCE BRIEF
  Generated: 25 March 2025, 14:32
==============================

  [Moneycontrol] — 8 articles
  ----------------------------------------
  • RBI holds repo rate steady amid inflation concerns
  • Sensex rises 400 points on foreign inflows
  • HDFC Bank Q4 results beat analyst estimates

  [Economic Times] — 6 articles
  ...

Total articles collected: 28
Sources covered: 4
```

## What I Learned

- How web scrapers handle HTML structure differently across sites
- Why polite delays between requests matter (rate limiting)
- How LSA summarization extracts key sentences using matrix decomposition
- Data pipeline design: scrape → clean → analyze → export

## Limitations & Next Steps

- Some sites block scrapers; mock data is used as fallback for demonstration
- Could add Selenium for JavaScript-rendered pages
- Could add sentiment analysis to classify articles as positive/negative
- Could schedule to run daily and track trends over time
