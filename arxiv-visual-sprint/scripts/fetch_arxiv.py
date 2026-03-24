import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

def fetch_recent_papers(query):
    query_encoded = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query={query_encoded}&start=0&max_results=50&sortBy=submittedDate&sortOrder=descending"
    
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode("utf-8")
            root = ET.fromstring(content)
            ns = {"atom": "http://www.w3.org/2005/Atom"\}
            
            papers = []
            seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
            
            for entry in root.findall("atom:entry", ns):
                published_str = entry.find("atom:published", ns).text
                published_dt = datetime.strptime(published_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=tiimport urllib.request
import urllib.parse
import xml.etree.t import urllib.parse
  import xml.etree.Entfrom datetime import datetime, ti  
def fetch_recent_papers(query):
    query_encodestr    query_encoded = urllib.par      url = f"http://export.arxiv.org/api/querte    
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response:
            content = response.re")         try:
        with urllib.requestap                     content = response.read().decode("utf-8"              root = ET.fromstring(content)
          ry            ns = {"atom": "http://www.w3sh            
            papers = []
            seven_]
           Ex            seven_dayspr            
            for entry in root.findall("atom:entry", ns):
    an           fo                published_str = entry.find("atom:publisle                published_dt = datetime.strptime(published_str, "%Y-"import urllib.parse