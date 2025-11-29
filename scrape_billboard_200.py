import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import sys

# --- Configuration ---
CHART_URL = "https://www.billboard.com/charts/billboard-200/"
OUTPUT_FILE = "billboard_200.json"
# ---------------------

def parse_date(date_str):
    """Parses date string like '10/18/25' to '2025-10-18'"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str.strip(), "%m/%d/%y").strftime("%Y-%m-%d")
    except ValueError:
        return None

def scrape():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    
    print(f"Fetching {CHART_URL}...")
    try:
        response = requests.get(CHART_URL, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch page: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 1. Extract Chart Date
    chart_date = datetime.now().strftime("%Y-%m-%d")
    date_element = soup.find(string=re.compile(r"Week of "))
    if date_element:
        try:
            clean_date = date_element.strip().replace("Week of ", "")
            chart_date = datetime.strptime(clean_date, "%B %d, %Y").strftime("%Y-%m-%d")
        except:
            pass
    
    print(f"Chart Date: {chart_date}")

    # 2. Parse Songs
    chart_data = []
    rows = soup.find_all("div", class_="o-chart-results-list-row-container")
    
    print(f"Found {len(rows)} entries. Parsing details...")

    for row in rows:
        try:
            # Basic Info
            rank_wrapper = row.find("span", class_="c-label")
            rank = int(rank_wrapper.get_text(strip=True)) if rank_wrapper and rank_wrapper.get_text(strip=True).isdigit() else 0
            
            title_h3 = row.find("h3", id="title-of-a-story")
            song_title = title_h3.get_text(strip=True) if title_h3 else "Unknown"
            
            artist_span = title_h3.find_next_sibling("span") if title_h3 else None
            artist = artist_span.get_text(strip=True) if artist_span else "Unknown"
            
            # Image Extraction
            image_url = None
            img_tag = row.find("img", class_="c-lazy-image__img")
            if img_tag:
                if img_tag.get("data-lazy-src"):
                    image_url = img_tag.get("data-lazy-src")
                elif img_tag.get("src"):
                    image_url = img_tag.get("src")
            
            # Extended Stats
            debut_container = row.find("div", class_="o-chart-position-stats__debut")
            peak_container = row.find("div", class_="o-chart-position-stats__peak")
            
            debut_pos = None
            debut_date = None
            peak_pos = None
            peak_date = None
            
            if debut_container:
                d_num = debut_container.find("span", class_="c-label")
                if d_num and d_num.get_text(strip=True).isdigit(): 
                    debut_pos = int(d_num.get_text(strip=True))
                
                d_date_div = debut_container.find("div", class_="o-chart-position-stats__date")
                if d_date_div and d_date_div.find("a"):
                    debut_date = parse_date(d_date_div.find("a").get_text(strip=True))

            if peak_container:
                p_num = peak_container.find("span", class_="c-label")
                if p_num and p_num.get_text(strip=True).isdigit(): 
                    peak_pos = int(p_num.get_text(strip=True))
                
                p_date_div = peak_container.find("div", class_="o-chart-position-stats__date")
                if p_date_div and p_date_div.find("a"):
                    peak_date = parse_date(p_date_div.find("a").get_text(strip=True))
            
            # Standard Stats (Fallback/Verification)
            last_week = None
            weeks_on_chart = None
            
            text_content = row.get_text(" ", strip=True)
            stats_match = re.search(r"LW\s+(\d+|-)\s+PEAK\s+(\d+)\s+WEEKS\s+(\d+)", text_content)
            
            if stats_match:
                lw_val = stats_match.group(1)
                last_week = int(lw_val) if lw_val.isdigit() else None
                
                if peak_pos is None:
                    peak_pos = int(stats_match.group(2))
                    
                weeks_on_chart = int(stats_match.group(3))
            
            entry = {
                "rank": rank,
                "title": song_title,
                "artist": artist,
                "image": image_url,
                "last_week": last_week,
                "peak_position": peak_pos,
                "weeks_on_chart": weeks_on_chart,
                "debut_position": debut_pos,
                "debut_date": debut_date,
                "peak_date": peak_date
            }
            
            chart_data.append(entry)
            
        except Exception as e:
            print(f"Error parsing row rank {rank}: {e}")
            continue

    # Construct Final JSON
    final_json = {
        "date": chart_date,
        "data": chart_data
    }
    
    with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
        json.dump(final_json, f, indent=4, ensure_ascii=False)
        
    print(f"Done! Saved {len(chart_data)} entries to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape()