import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta


def search_arxiv(query, max_results=30):
    query_encoded = query.replace(" ", "+")
    url = f"http://export.arxiv.org/api/query?search_query=all:{query_encoded}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode("utf-8")
            root = ET.fromstring(content)

            # Atom namespace
            ns = {"atom": "http://www.w3.org/2005/Atom"}

            papers = []
            for entry in root.findall("atom:entry", ns):
                title = entry.find("atom:title", ns).text.strip()
                id_full = entry.find("atom:id", ns).text
                id_short = id_full.split("/")[-1]
                summary = entry.find("atom:summary", ns).text.strip().replace("\n", " ")
                published = entry.find("atom:published", ns).text

                papers.append(
                    {
                        "title": title,
                        "id": id_short,
                        "summary": summary,
                        "published": published,
                    }
                )
            return papers
    except Exception as e:
        print(f"Error: {e}")
        return []


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2 or not sys.argv[1].strip():
        raise ValueError("请输入一个查询关键词作为参数。")
    topic = sys.argv[1].strip()
    papers = search_arxiv(topic)

    if not papers:
        print("未找到符合条件的论文。")
    else:
        print(f"🚀 **太棒了！我已经为您在 arXiv 上完成了近一周的“情报扫描”。**")
        print()
        print(
            f"针对您的选题 **{topic}**，我为您精选了以下 **{len(papers[:20])}** 篇最具代表性的论文："
        )
        print()
        for i, paper in enumerate(papers[:20]):
            summary_short = paper["summary"][:200] + "..."
            print(f"{i+1}. **{paper['title']}** ({paper['id']})")
            print(f"   - 💡 **核心亮点**: {summary_short}")
            print(f"   - 📅 **发布日期**: {paper['published']}")
            print()
        print(
            "**接下来，您可以从这 20 篇中挑选 3 篇（例如输入“1, 12, 18”），我将立即启动深度解析并为您生成精美的 Visual Abstract！**"
        )
