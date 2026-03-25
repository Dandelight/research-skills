import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone


def fetch_recent_papers(query, max_results=50, days_back=7):
    query_encoded = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query={query_encoded}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode("utf-8")
            root = ET.fromstring(content)
            ns = {"atom": "http://www.w3.org/2005/Atom"}

            papers = []
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)

            for entry in root.findall("atom:entry", ns):
                published_node = entry.find("atom:published", ns)
                if published_node is None:
                    continue

                published_str = published_node.text
                try:
                    published_dt = datetime.strptime(
                        published_str, "%Y-%m-%dT%H:%M:%SZ"
                    ).replace(tzinfo=timezone.utc)
                except ValueError:
                    continue

                title_node = entry.find("atom:title", ns)
                title = (
                    title_node.text.strip().replace("\n", " ")
                    if title_node is not None
                    else "No Title"
                )

                id_node = entry.find("atom:id", ns)
                id_full = id_node.text if id_node is not None else ""
                id_short = id_full.split("/")[-1] if id_full else "Unknown"

                summary_node = entry.find("atom:summary", ns)
                summary = (
                    summary_node.text.strip().replace("\n", " ")
                    if summary_node is not None
                    else ""
                )

                papers.append(
                    {
                        "title": title,
                        "id": id_short,
                        "summary": summary,
                        "published": published_str,
                        "recent": published_dt >= cutoff_date,
                    }
                )

            return [p for p in papers if p["recent"]]
    except Exception as e:
        print(f"Error fetching from arXiv: {e}", file=sys.stderr)
        return []


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_arxiv.py <query>")
        sys.exit(1)

    query = sys.argv[1]
    papers = fetch_recent_papers(query)
    print(json.dumps(papers, ensure_ascii=False, indent=2))
