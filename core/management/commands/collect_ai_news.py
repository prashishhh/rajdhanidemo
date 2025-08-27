from django.core.management.base import BaseCommand
import feedparser
import html
from langdetect import detect, LangDetectException
from core.models import NewsArticle

class Command(BaseCommand):
    help = "Collects news, detects language, and saves headlines/summaries to NewsArticle DB model."

    def handle(self, *args, **options):
        rss_feeds = [
            "http://feeds.bbci.co.uk/news/world/rss.xml",
            "https://rss.cnn.com/rss/edition_world.rss",
            "https://www.aljazeera.com/xml/rss/all.xml",
            "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
            "https://ekantipur.com/rss",
            "https://thehimalayantimes.com/rssfeed",
            "https://www.onlinekhabar.com/feed",
            "https://nagariknews.nagariknetwork.com/rss",
        ]

        for feed_url in rss_feeds:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:3]:
                title = entry.title.strip()
                summary = html.unescape(entry.get('summary', '')).strip()

                # Detect language on headline
                try:
                    lang = detect(title)
                except LangDetectException:
                    lang = "unknown"

                # Save to DB (avoid duplicates by headline)
                article, created = NewsArticle.objects.get_or_create(
                    headline=title,
                    defaults={
                        'summary': summary,
                        'language': lang,
                        'is_approved': False,
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Saved: {title}"))
                else:
                    self.stdout.write(self.style.NOTICE(f"Already exists: {title}"))

                self.stdout.write(self.style.NOTICE(f"Language: {lang.upper()}"))
                if summary:
                    self.stdout.write(f"Summary: {summary}")
                self.stdout.write('-' * 60)
