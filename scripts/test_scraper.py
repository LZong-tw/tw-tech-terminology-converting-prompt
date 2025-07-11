#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試爬蟲功能
"""

import sys
import os

# 添加父目錄到路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.scrape_wiki_terms import WikiTermsScraper

def test_scraper():
    """測試爬蟲功能"""
    print("開始測試爬蟲功能...")
    
    scraper = WikiTermsScraper()
    
    # 測試取得頁面
    print("1. 測試取得維基百科頁面...")
    html_content = scraper.fetch_wiki_page()
    if html_content:
        print("✓ 成功取得頁面")
    else:
        print("✗ 取得頁面失敗")
        return False
    
    # 測試解析術語
    print("2. 測試解析術語對照表...")
    terms = scraper.parse_terms_table(html_content)
    if terms:
        print(f"✓ 成功解析 {len(terms)} 個術語")
        # 顯示前幾個術語作為範例
        print("前 5 個術語範例:")
        for i, (cn, tw) in enumerate(terms[:5]):
            print(f"  {cn} → {tw}")
    else:
        print("✗ 解析術語失敗")
        return False
    
    # 測試載入現有術語
    print("3. 測試載入現有術語...")
    existing_terms = scraper.load_existing_terms()
    print(f"✓ 載入現有術語 {len(existing_terms)} 個")
    
    # 測試合併術語
    print("4. 測試合併術語...")
    merged_terms = scraper.merge_terms(terms, existing_terms)
    print(f"✓ 合併後共有 {len(merged_terms)} 個術語")
    
    print("\n所有測試通過！爬蟲功能正常。")
    return True

if __name__ == "__main__":
    test_scraper() 