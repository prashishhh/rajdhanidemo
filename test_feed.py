

import feedparser
import html

rss_feeds = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",              
    "https://rss.cnn.com/rss/edition_world.rss",               
    "https://www.aljazeera.com/xml/rss/all.xml",               
    "https://feeds.a.dj.com/rss/RSSWorldNews.xml",             
    "https://ekantipur.com/rss",                               
    "https://thehimalayantimes.com/rssfeed",    
    "https://www.onlinekhabar.com/feed",                       # Online Khabar
    "https://nagariknews.nagariknetwork.com/rss",                  
]

for feed_url in rss_feeds:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:3]:  # Get top 3 from each feed
        title = entry.title
        summary = html.unescape(entry.get('summary', ''))
        # If you want, combine title and summary for more context
        combined = f"{title}. {summary}"
        print(combined)
        print('-' * 60)
