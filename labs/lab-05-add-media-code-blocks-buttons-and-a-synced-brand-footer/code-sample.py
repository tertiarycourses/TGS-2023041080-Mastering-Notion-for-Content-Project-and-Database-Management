"""UTM tagging helper used in Brightwave's tracking script examples."""
from urllib.parse import urlencode

def utm_link(url: str, source: str, medium: str, campaign: str) -> str:
    """Return the URL with UTM parameters appended."""
    params = {"utm_source": source, "utm_medium": medium, "utm_campaign": campaign}
    joiner = "&" if "?" in url else "?"
    return f"{url}{joiner}{urlencode(params)}"

if __name__ == "__main__":
    print(utm_link("https://brightwave.notion.site/five-content-trends", "newsletter", "email", "trends-2027"))
