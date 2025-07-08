#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taiwan Tech Terminology Converter

A Python library for converting technical terminology between 
Simplified Chinese (China Mainland) and Traditional Chinese (Taiwan).
"""

import json
import re
from typing import Dict, Optional, Union
from pathlib import Path

class TechTerminologyConverter:
    """台灣技術術語轉換器
    
    用於在簡體中文（中國大陸）和繁體中文（台灣）技術術語之間進行轉換
    """
    
    def __init__(self, vocabulary_path: Optional[str] = None):
        """初始化轉換器
        
        Args:
            vocabulary_path: JSON詞彙檔案路徑，如果未提供則使用預設的terminology.json
        """
        if vocabulary_path is None:
            vocabulary_path = Path(__file__).parent / "terminology.json"
        
        self.vocabulary_path = vocabulary_path
        self._load_vocabulary()
    
    def _load_vocabulary(self):
        """載入詞彙檔案"""
        try:
            with open(self.vocabulary_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.cn_to_tw = data.get('cn_to_tw', {})
            self.tw_to_cn = data.get('tw_to_cn', {})
            self.metadata = data.get('metadata', {})
            
            print(f"已載入 {len(self.cn_to_tw)} 條簡轉繁術語映射")
            print(f"已載入 {len(self.tw_to_cn)} 條繁轉簡術語映射")
            
        except FileNotFoundError:
            raise FileNotFoundError(f"找不到詞彙檔案: {self.vocabulary_path}")
        except json.JSONDecodeError:
            raise ValueError(f"詞彙檔案格式錯誤: {self.vocabulary_path}")
    
    def cn_to_tw_convert(self, text: str, preserve_case: bool = True) -> str:
        """將簡體中文（大陸）技術術語轉換為繁體中文（台灣）
        
        Args:
            text: 要轉換的文本
            preserve_case: 是否保持大小寫（對英文單詞）
            
        Returns:
            轉換後的文本
        """
        result = text
        
        # 按術語長度降序排列，優先匹配長術語避免部分匹配問題
        sorted_terms = sorted(self.cn_to_tw.keys(), key=len, reverse=True)
        
        # 使用一個標記系統來避免重複替換
        # 我們用一個特殊的標記來標記已經轉換的部分
        marker_counter = 0
        markers = {}
        
        for cn_term in sorted_terms:
            tw_term = self.cn_to_tw[cn_term]
            
            # 如果這個術語存在於當前結果中
            if cn_term in result:
                # 創建一個唯一的標記
                marker = f"__MARKER_{marker_counter}__"
                markers[marker] = tw_term
                marker_counter += 1
                
                # 用標記替換術語
                result = result.replace(cn_term, marker)
        
        # 最後將所有標記替換為對應的台灣術語
        for marker, tw_term in markers.items():
            result = result.replace(marker, tw_term)
        
        return result
    
    def tw_to_cn_convert(self, text: str, preserve_case: bool = True) -> str:
        """將繁體中文（台灣）技術術語轉換為簡體中文（大陸）
        
        Args:
            text: 要轉換的文本
            preserve_case: 是否保持大小寫（對英文單詞）
            
        Returns:
            轉換後的文本
        """
        result = text
        
        # 按術語長度降序排列，優先匹配長術語避免部分匹配問題
        sorted_terms = sorted(self.tw_to_cn.keys(), key=len, reverse=True)
        
        # 使用一個標記系統來避免重複替換
        marker_counter = 0
        markers = {}
        
        for tw_term in sorted_terms:
            cn_term = self.tw_to_cn[tw_term]
            
            # 如果這個術語存在於當前結果中
            if tw_term in result:
                # 創建一個唯一的標記
                marker = f"__MARKER_{marker_counter}__"
                markers[marker] = cn_term
                marker_counter += 1
                
                # 用標記替換術語
                result = result.replace(tw_term, marker)
        
        # 最後將所有標記替換為對應的大陸術語
        for marker, cn_term in markers.items():
            result = result.replace(marker, cn_term)
        
        return result
    
    def convert(self, text: str, direction: str = "cn_to_tw") -> str:
        """通用轉換方法
        
        Args:
            text: 要轉換的文本
            direction: 轉換方向，"cn_to_tw" 或 "tw_to_cn"
            
        Returns:
            轉換後的文本
        """
        if direction == "cn_to_tw":
            return self.cn_to_tw_convert(text)
        elif direction == "tw_to_cn":
            return self.tw_to_cn_convert(text)
        else:
            raise ValueError("direction 必須是 'cn_to_tw' 或 'tw_to_cn'")
    
    def get_mapping(self, term: str, direction: str = "cn_to_tw") -> Optional[str]:
        """獲取特定術語的對應詞彙
        
        Args:
            term: 要查詢的術語
            direction: 查詢方向，"cn_to_tw" 或 "tw_to_cn"
            
        Returns:
            對應的術語，如果找不到則返回None
        """
        if direction == "cn_to_tw":
            return self.cn_to_tw.get(term)
        elif direction == "tw_to_cn":
            return self.tw_to_cn.get(term)
        else:
            raise ValueError("direction 必須是 'cn_to_tw' 或 'tw_to_cn'")
    
    def search_terms(self, keyword: str, direction: str = "cn_to_tw") -> Dict[str, str]:
        """搜尋包含關鍵字的術語
        
        Args:
            keyword: 搜尋關鍵字
            direction: 搜尋方向，"cn_to_tw" 或 "tw_to_cn"
            
        Returns:
            包含關鍵字的術語映射字典
        """
        if direction == "cn_to_tw":
            source_dict = self.cn_to_tw
        elif direction == "tw_to_cn":
            source_dict = self.tw_to_cn
        else:
            raise ValueError("direction 必須是 'cn_to_tw' 或 'tw_to_cn'")
        
        results = {}
        for term, translation in source_dict.items():
            if keyword in term or keyword in translation:
                results[term] = translation
        
        return results
    
    def get_statistics(self) -> Dict[str, Union[int, str]]:
        """獲取詞彙庫統計信息
        
        Returns:
            統計信息字典
        """
        return {
            "cn_to_tw_mappings": len(self.cn_to_tw),
            "tw_to_cn_mappings": len(self.tw_to_cn),
            "vocabulary_file": str(self.vocabulary_path),
            "version": self.metadata.get("version", "unknown"),
            "description": self.metadata.get("description", "")
        }

# 便利函數
def cn_to_tw(text: str) -> str:
    """快速將簡體中文（大陸）技術術語轉換為繁體中文（台灣）"""
    converter = TechTerminologyConverter()
    return converter.cn_to_tw_convert(text)

def tw_to_cn(text: str) -> str:
    """快速將繁體中文（台灣）技術術語轉換為簡體中文（大陸）"""
    converter = TechTerminologyConverter()
    return converter.tw_to_cn_convert(text)

if __name__ == "__main__":
    # 簡單測試
    converter = TechTerminologyConverter()
    
    # 測試範例
    test_text_cn = "這個應用程序使用了最新的算法來處理數據，並透過雲計算提供服務。開發者可以透過集成開發環境進行調試。"
    print("原文（簡體）:", test_text_cn)
    
    converted = converter.cn_to_tw_convert(test_text_cn)
    print("轉換後（繁體台灣）:", converted)
    
    # 顯示統計信息
    stats = converter.get_statistics()
    print(f"\n詞彙庫統計: {stats}")