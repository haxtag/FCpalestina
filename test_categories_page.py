#!/usr/bin/env python3
"""Test script to analyze categories page structure"""

import requests
from bs4 import BeautifulSoup
import time

def test_categories_page():
    url = "https://shixingtiyu.x.yupoo.com/categories/?page=1"
    print(f"Analyzing: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print(f"Page title: {soup.title.get_text() if soup.title else 'N/A'}")
        print(f"Page size: {len(response.content)} bytes")
        
        # Try different selectors for album links
        selectors = [
            'a[href*="/albums/"]',
            '.album-item a', 
            '.photo-item a',
            'a[class*="album"]',
            'div[class*="album"] a'
        ]
        
        for selector in selectors:
            try:
                links = soup.select(selector)
                print(f"\nSelector '{selector}': {len(links)} results")
                
                for i, link in enumerate(links[:3]):  # First 3
                    href = link.get('href', '')
                    text = link.get_text().strip()
                    title_attr = link.get('title', '')
                    
                    print(f"  {i+1}. URL: {href}")
                    print(f"     Text: '{text}'")
                    print(f"     Title: '{title_attr}'")
                    print()
                    
                if links:
                    break
                    
            except Exception as e:
                print(f"Error with selector '{selector}': {e}")
        
        # Also check for any Chinese text patterns
        all_text = soup.get_text()
        chinese_chars = [c for c in all_text if '\u4e00' <= c <= '\u9fff']
        print(f"Chinese characters found: {len(chinese_chars)}")
        
        # Look for specific patterns
        import re
        patterns = [
            r'25\d{2}',  # 2526, 2525, etc.
            r'巴萨|巴塞罗那',  # Barcelona
            r'主场|客场|第三',  # home, away, third  
            r'S-\w+L',  # Size patterns
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, all_text)
            if matches:
                print(f"Pattern '{pattern}': {matches[:5]}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_categories_page()