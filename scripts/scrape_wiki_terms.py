#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
維基教科書術語對照表爬蟲
自動從維基教科書爬取中國大陸台灣計算機術語對照表並更新本地 CSV 檔案
"""

import requests
from bs4 import BeautifulSoup
import csv
import re
import logging
from datetime import datetime
import os

# 設定記錄
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WikiTermsScraper:
    def __init__(self):
        self.url = "https://zh.wikibooks.org/w/index.php?title=%E5%A4%A7%E9%99%86%E5%8F%B0%E6%B9%BE%E8%AE%A1%E7%AE%97%E6%9C%BA%E6%9C%AF%E8%AF%AD%E5%AF%B9%E7%85%A7%E8%A1%A8&variant=zh"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.terms_file = 'terms.csv'
        self.wiki_snapshot_file = 'wiki_terms_snapshot.csv'  # 新增快照檔案
        self.deleted_terms_file = 'deleted_terms.txt'  # 新增刪除詞彙記錄檔
        
    def fetch_wiki_page(self):
        """取得維基教科書頁面內容"""
        try:
            logger.info(f"正在取得頁面: {self.url}")
            response = requests.get(self.url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.RequestException as e:
            logger.error(f"取得頁面失敗: {e}")
            return None
            
    def parse_terms_table(self, html_content):
        """解析頁面中的術語對照表"""
        soup = BeautifulSoup(html_content, 'html.parser')
        terms = []
        
        # 尋找表格
        tables = soup.find_all('table', class_='wikitable')
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # 跳過標題行
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:
                    # 正確抓取：中國大陸用語 → 台灣用語
                    cn_cell = cells[2].get_text(strip=True)
                    tw_cell = cells[1].get_text(strip=True)
                    
                    # 先 split 再 clean
                    raw_cn_terms = self.split_terms(cn_cell)
                    raw_tw_terms = self.split_terms(tw_cell)
                    cn_terms = [self.clean_term(t) for t in raw_cn_terms if self.is_chinese_term(t)]
                    tw_terms = [self.clean_term(t) for t in raw_tw_terms if self.is_chinese_term(t)]
                    if not cn_terms or not tw_terms:
                        continue
                    
                    # 按位置對應：中國大陸詞和台灣詞一一對應
                    # 如果數量不符合，則每個中國大陸詞對應所有台灣詞
                    if len(cn_terms) == len(tw_terms):
                        # 一一對應
                        for i, cn in enumerate(cn_terms):
                            tw_str = tw_terms[i]
                            if cn != tw_str:
                                terms.append((cn, tw_str))
                    else:
                        # 數量不符合時，每個中國大陸詞對應所有台灣詞
                        for cn in cn_terms:
                            tw_str = ';'.join(sorted(set(tw_terms)))
                            if cn != tw_str:
                                terms.append((cn, tw_str))
        logger.info(f"從維基教科書解析到 {len(terms)} 個術語對照")
        return terms
        
    def clean_term(self, term):
        """清理術語文字"""
        if not term:
            return ""
            
        # 移除多餘的空白字元
        term = re.sub(r'\s+', ' ', term.strip())
        
        # 移除常見的標記
        term = re.sub(r'\[.*?\]', '', term)  # 移除方括號內容
        term = re.sub(r'\(.*?\)', '', term)  # 移除圓括號內容
        term = re.sub(r'（.*?）', '', term)  # 移除中文圓括號內容
        
        # 移除特殊字元
        term = re.sub(r'[^\w\s\u4e00-\u9fff]', '', term)
        
        return term.strip()
        
    def is_chinese_term(self, term):
        """檢查是否為中文術語（包含中文字元）"""
        if not term:
            return False
        
        # 檢查是否包含中文字元
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', term)
        return len(chinese_chars) > 0
        
    def split_terms(self, term):
        """拆分包含多個詞彙的術語（不做 clean）"""
        if not term:
            return []
        
        # 先按分號拆分，再按其他分隔符號拆分
        # 例如：「存取 (win)；取用 (mac)」應該拆分為「存取 (win)」和「取用 (mac)」
        semicolon_parts = term.split('；')
        result = []
        
        for part in semicolon_parts:
            # 對每個分號分隔的部分，再按其他分隔符號拆分
            separators = r'[\s,，、]'
            sub_parts = re.split(separators, part.strip())
            result.extend([p.strip() for p in sub_parts if p.strip()])
        
        return result
        
    def load_existing_terms(self):
        """載入現有的術語對照表"""
        existing_terms = {}
        if os.path.exists(self.terms_file):
            try:
                with open(self.terms_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        existing_terms[row['cn']] = row['tw']
                logger.info(f"載入現有術語 {len(existing_terms)} 個")
            except Exception as e:
                logger.error(f"載入現有術語失敗: {e}")
        return existing_terms
        
    def save_wiki_snapshot(self, wiki_terms_dict):
        """儲存維基教科書術語快照到 CSV 檔案"""
        try:
            with open(self.wiki_snapshot_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['cn', 'tw'])
                sorted_terms = sorted(wiki_terms_dict.items(), key=lambda x: x[0])
                for cn_term, tw_term in sorted_terms:
                    writer.writerow([cn_term, tw_term])
            logger.info(f"成功儲存維基快照 {len(wiki_terms_dict)} 個術語到 {self.wiki_snapshot_file}")
        except Exception as e:
            logger.error(f"儲存維基快照失敗: {e}")

    def load_wiki_snapshot(self):
        """載入上次維基教科書術語快照"""
        wiki_terms = {}
        if os.path.exists(self.wiki_snapshot_file):
            try:
                with open(self.wiki_snapshot_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        wiki_terms[row['cn']] = row['tw']
                logger.info(f"載入上次維基快照 {len(wiki_terms)} 個術語")
            except Exception as e:
                logger.error(f"載入維基快照失敗: {e}")
        return wiki_terms
        
    def load_deleted_terms(self):
        """載入本地刪除詞彙及其對應內容，回傳 dict: {cn: set(tw1, tw2, ...)}"""
        deleted = {}
        if os.path.exists(self.deleted_terms_file):
            try:
                with open(self.deleted_terms_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line or ',' not in line:
                            continue
                        cn, tws = line.split(',', 1)
                        cn = cn.strip()
                        tw_set = set(t.strip() for t in tws.split(';') if t.strip())
                        if cn in deleted:
                            deleted[cn].update(tw_set)
                        else:
                            deleted[cn] = tw_set
                logger.info(f"載入本地刪除詞彙 {len(deleted)} 筆")
            except Exception as e:
                logger.error(f"載入刪除詞彙失敗: {e}")
        return deleted
        
    def merge_terms(self, wiki_terms, existing_terms):
        """詞彙級合併：僅維基內容有異動的詞才自動合併，且本地刪除內容不會自動加回，只合併新內容"""
        # 將 wiki_terms 按中國大陸詞分組
        cn_to_tw_terms = {}
        for cn_term, tw_term in wiki_terms:
            if cn_term not in cn_to_tw_terms:
                cn_to_tw_terms[cn_term] = set()
            cn_to_tw_terms[cn_term].add(tw_term)
        wiki_terms_dict = {cn: ';'.join(sorted(tws)) for cn, tws in cn_to_tw_terms.items()}

        # 載入上次維基快照
        prev_wiki_terms = self.load_wiki_snapshot()
        # 載入本地刪除詞彙
        deleted_terms = self.load_deleted_terms()

        merged_terms = existing_terms.copy()
        new_terms = 0
        updated_terms = 0
        skipped_terms = 0
        deleted_skipped = 0

        for cn_term, new_tw in wiki_terms_dict.items():
            prev_tw = prev_wiki_terms.get(cn_term)
            # 如果這個詞在維基快照和這次維基內容一樣，保留本地內容
            if prev_tw is not None and prev_tw == new_tw:
                if cn_term in merged_terms:
                    skipped_terms += 1
                    continue  # 保留本地內容
                else:
                    # 本地沒有，新增
                    merged_terms[cn_term] = new_tw
                    new_terms += 1
                    logger.info(f"新增術語: {cn_term} → {new_tw}")
            else:
                # 維基內容有異動，才自動合併/覆蓋
                if cn_term in deleted_terms:
                    # 只合併新內容，不加回刪除內容
                    wiki_tw_set = set(new_tw.split(';'))
                    deleted_tw_set = deleted_terms[cn_term]
                    new_only_set = wiki_tw_set - deleted_tw_set
                    if new_only_set:
                        new_only_str = ';'.join(sorted(new_only_set))
                        merged_terms[cn_term] = new_only_str
                        updated_terms += 1
                        logger.info(f"只合併新內容: {cn_term} → {new_only_str}")
                    else:
                        deleted_skipped += 1
                        logger.info(f"本地刪除過，且無新內容: {cn_term}，不自動加回")
                    continue
                if cn_term not in merged_terms:
                    merged_terms[cn_term] = new_tw
                    new_terms += 1
                    logger.info(f"新增術語: {cn_term} → {new_tw}")
                elif merged_terms[cn_term] != new_tw:
                    old_tw = merged_terms[cn_term]
                    merged_terms[cn_term] = new_tw
                    updated_terms += 1
                    logger.info(f"更新術語: {cn_term} → {old_tw} → {new_tw}")
                else:
                    skipped_terms += 1
        logger.info(f"詞彙級合併：新增 {new_terms}，更新 {updated_terms}，保留本地 {skipped_terms}，本地刪除跳過 {deleted_skipped} 筆")
        # 回傳合併後的內容和這次維基內容（for snapshot）
        return merged_terms, wiki_terms_dict
        
    def save_terms(self, terms_dict):
        """儲存術語對照表到 CSV 檔案"""
        try:
            # 建立備份
            if os.path.exists(self.terms_file):
                backup_file = f"{self.terms_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                os.rename(self.terms_file, backup_file)
                logger.info(f"建立備份: {backup_file}")
            
            # 寫入新的 CSV 檔案
            with open(self.terms_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['cn', 'tw'])
                
                # 按中文術語排序
                sorted_terms = sorted(terms_dict.items(), key=lambda x: x[0])
                for cn_term, tw_term in sorted_terms:
                    writer.writerow([cn_term, tw_term])
                    
            logger.info(f"成功儲存 {len(terms_dict)} 個術語到 {self.terms_file}")
            return True
            
        except Exception as e:
            logger.error(f"儲存術語失敗: {e}")
            return False
            
    def run(self):
        """執行完整的爬取和更新流程（詞彙級合併）"""
        logger.info("開始執行術語對照表更新流程（詞彙級合併）")
        
        # 取得維基教科書頁面
        html_content = self.fetch_wiki_page()
        if not html_content:
            logger.error("無法取得維基教科書頁面，流程終止")
            return False
            
        # 解析術語對照表
        wiki_terms = self.parse_terms_table(html_content)
        if not wiki_terms:
            logger.error("無法解析術語對照表，流程終止")
            return False
            
        # 載入現有術語
        existing_terms = self.load_existing_terms()
        
        # 合併術語
        merged_terms, wiki_terms_dict = self.merge_terms(wiki_terms, existing_terms)
        
        # 儲存術語
        success = self.save_terms(merged_terms)
        
        if success:
            self.save_wiki_snapshot(wiki_terms_dict)
            logger.info("術語對照表更新完成（詞彙級合併）")
        else:
            logger.error("術語對照表更新失敗")
            
        return success

def main():
    """主函式"""
    scraper = WikiTermsScraper()
    success = scraper.run()
    
    if not success:
        exit(1)

if __name__ == "__main__":
    main() 