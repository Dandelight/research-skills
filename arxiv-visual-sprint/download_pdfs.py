import urllib.request
import os

papers = ["2603.21341v1", "2603.20711v1", "2603.20668v1"]
os.makedirs("pdfs", exist_ok=True)

for p in papers:
    url = f"https://arxiv.org/pdf/{p}.pdf"
    print(f"Downloading {p}...")
    try:
        urllib.request.urlretrieve(url, f"pdfs/{p}.pdf")
        print(f"Success: {p}")
    except Exception as e:
        print(f"Failed {p}: {e}")
