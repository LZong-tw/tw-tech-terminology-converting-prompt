#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taiwan Tech Terminology Converter Examples

使用範例展示如何使用台灣技術術語轉換器
"""

from tech_terminology_converter import TechTerminologyConverter, cn_to_tw, tw_to_cn

def example_basic_usage():
    """基本使用範例"""
    print("=== 基本使用範例 ===")
    
    # 方法1: 使用便利函數
    cn_text = "這個應用程序使用了最新的算法來處理數據"
    tw_text = cn_to_tw(cn_text)
    print(f"簡體: {cn_text}")
    print(f"繁體台灣: {tw_text}")
    
    # 反向轉換
    back_to_cn = tw_to_cn(tw_text)
    print(f"轉回簡體: {back_to_cn}")
    print()

def example_class_usage():
    """類別使用範例"""
    print("=== 類別使用範例 ===")
    
    # 初始化轉換器
    converter = TechTerminologyConverter()
    
    # 測試文本
    test_texts = [
        "開發者可以透過集成開發環境進行調試",
        "這個框架支援多線程程序設計",
        "使用緩存技術可以提升系統性能",
        "資料庫架構設計需要考慮安全性",
    ]
    
    for text in test_texts:
        converted = converter.cn_to_tw_convert(text)
        print(f"原文: {text}")
        print(f"轉換: {converted}")
        print()

def example_search_and_lookup():
    """搜尋和查詢範例"""
    print("=== 搜尋和查詢範例 ===")
    
    converter = TechTerminologyConverter()
    
    # 搜尋包含關鍵字的術語
    print("搜尋包含 '開發' 的術語:")
    results = converter.search_terms("開發", "cn_to_tw")
    for cn, tw in results.items():
        print(f"  {cn} → {tw}")
    print()
    
    # 查詢特定術語
    terms_to_lookup = ["算法", "數據", "程序", "緩存"]
    print("查詢特定術語:")
    for term in terms_to_lookup:
        mapping = converter.get_mapping(term, "cn_to_tw")
        if mapping:
            print(f"  {term} → {mapping}")
        else:
            print(f"  {term} → (未找到對應詞彙)")
    print()

def example_batch_processing():
    """批次處理範例"""
    print("=== 批次處理範例 ===")
    
    converter = TechTerminologyConverter()
    
    # 批次轉換多個句子
    sentences = [
        "這個網站使用了響應式設計",
        "開發團隊選擇了微服務架構", 
        "前端框架採用了組件化開發模式",
        "後端API支援RESTful設計風格",
        "數據庫使用了分布式存儲方案"
    ]
    
    print("批次轉換結果:")
    for sentence in sentences:
        converted = converter.cn_to_tw_convert(sentence)
        print(f"原文: {sentence}")
        print(f"轉換: {converted}")
        print()

def example_file_processing():
    """檔案處理範例"""
    print("=== 檔案處理範例 ===")
    
    # 創建測試檔案
    test_content = """# 技術文檔範例

## 系統架構
這個系統採用了分布式微服務架構，使用Docker容器化部署。

## 開發環境
- 集成開發環境: VS Code
- 版本控制: Git
- 項目管理: GitHub
- 調試工具: Chrome DevTools

## 技術棧
- 前端: React.js框架
- 後端: Node.js + Express
- 數據庫: MongoDB
- 緩存: Redis

## 性能優化
通過實施以下策略來提升系統性能:
1. 緩存機制優化
2. 數據庫查詢優化
3. 前端資源壓縮
4. CDN加速
"""
    
    # 寫入測試檔案
    with open("test_input.txt", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    # 使用轉換器處理檔案
    converter = TechTerminologyConverter()
    
    with open("test_input.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    converted_content = converter.cn_to_tw_convert(content)
    
    # 寫入轉換結果
    with open("test_output.txt", "w", encoding="utf-8") as f:
        f.write(converted_content)
    
    print("檔案處理完成:")
    print("輸入檔案: test_input.txt")
    print("輸出檔案: test_output.txt")
    print()
    
    # 顯示部分轉換結果
    print("轉換結果預覽:")
    lines = converted_content.split('\n')
    for line in lines[:10]:
        if line.strip():
            print(f"  {line}")
    print("...")

def main():
    """執行所有範例"""
    print("台灣技術術語轉換器使用範例\n")
    
    example_basic_usage()
    example_class_usage()
    example_search_and_lookup()
    example_batch_processing()
    example_file_processing()
    
    print("=== 統計信息 ===")
    converter = TechTerminologyConverter()
    stats = converter.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()