import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import json
import sys

def fetch_recent_papers(query):
    query_encoded = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query={query_encoded}&start=0&max_results=50&sortBy=submittedDate&sortOrder=descending"
    
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode("utf-8")
            root = ET.fromstring(content)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            
            papers = []
            # We want recent papers (last 7 days)
            seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
            
            for entry in root.findall("atom:entry", ns):
                published_str = entry.find("atom:published", ns).text
                published_dt = datetime.strptime(published_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                
                title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
                id_full = entry.find("atom:id", ns).text
                id_short = id_full.split("/")[-1]
                summary = entry.find("atom:summary", ns).text.strip().replace("\n", " ")
                
                papers.append({
                    "title": title,
                    "id": id_short,
                    "summary": summary,
                    "published": published_str,
                    "recent": published_dt >= seven_days_ago
                })
            # Prioritize recent ones, but return top 15
            return [p for p in papers if p["recent"]][:15] if any(p["recent"] for p in papers) else papers[:15]
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    # Query: Multimodal Embodied AI
    query = 'all:"embodied" AND (all:"multimodal" OR all:"vision-language" OR all:"VLA")'
    papers = fetch_recent_papers(query)
    
    if not papers:
        print("未找到符合条件的论文。")
    else:
        print(f"🚀 **太棒了！我已经为您在 arXiv 上检索了关于多模态学习和具身智能的最新进展。**\n")
        recent_count = sum(1 for p in papers if p["recent"])
        print(f"针对您的选题，我为您精选了以下 **{len(papers)}** 篇最具代表性的论文：\n")
        
        for i, paper in enumerate(papers):
            summary_short = paper["summary"][:200] + "..."
            mark = "🔥 [近7天内]" if paper["recent"] else "📅"
            print(f"{i+1}. **{paper['title']}** ({paper['id']})")
            print(f"   - 💡 **核心亮点**: {summary_short}")
            print(f"   - {mark} **发布日期**: {paper['published']}\n")
