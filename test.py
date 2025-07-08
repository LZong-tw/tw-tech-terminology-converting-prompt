#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡單的測試檔案，驗證台灣技術術語轉換器功能
"""

import sys
from tech_terminology_converter import TechTerminologyConverter, cn_to_tw, tw_to_cn

def test_basic_conversion():
    """測試基本轉換功能"""
    print("測試基本轉換功能...")
    
    # 測試案例
    test_cases = [
        ("應用程序", "應用程式"),
        ("算法", "演算法"),
        ("數據", "資料"),
        ("調試", "除錯"),
        ("集成開發環境", "整合式開發環境"),
        ("雲計算", "雲端運算"),
    ]
    
    converter = TechTerminologyConverter()
    
    passed = 0
    failed = 0
    
    for cn_input, expected_tw in test_cases:
        result = converter.cn_to_tw_convert(cn_input)
        if result == expected_tw:
            print(f"✓ {cn_input} → {result}")
            passed += 1
        else:
            print(f"✗ {cn_input} → {result} (期望: {expected_tw})")
            failed += 1
    
    print(f"\n簡→繁轉換測試結果: {passed} 通過, {failed} 失敗")
    return failed == 0

def test_reverse_conversion():
    """測試反向轉換功能"""
    print("\n測試反向轉換功能...")
    
    test_cases = [
        ("應用程式", "應用程序"),
        ("演算法", "算法"),
        ("資料", "數據"),
        ("除錯", "調試"),
        ("整合式開發環境", "集成開發環境"),
        ("雲端運算", "雲計算"),
    ]
    
    converter = TechTerminologyConverter()
    
    passed = 0
    failed = 0
    
    for tw_input, expected_cn in test_cases:
        result = converter.tw_to_cn_convert(tw_input)
        if result == expected_cn:
            print(f"✓ {tw_input} → {result}")
            passed += 1
        else:
            print(f"✗ {tw_input} → {result} (期望: {expected_cn})")
            failed += 1
    
    print(f"\n繁→簡轉換測試結果: {passed} 通過, {failed} 失敗")
    return failed == 0

def test_full_sentence():
    """測試完整句子轉換"""
    print("\n測試完整句子轉換...")
    
    # README 中的範例
    cn_sentence = "這個應用程序使用了最新的算法來處理數據，並透過雲計算提供服務。開發者可以透過集成開發環境進行調試。"
    expected_tw = "這個應用程式使用了最新的演算法來處理資料，並透過雲端運算提供服務。開發者可以透過整合式開發環境進行除錯。"
    
    converter = TechTerminologyConverter()
    result = converter.cn_to_tw_convert(cn_sentence)
    
    if result == expected_tw:
        print("✓ 完整句子轉換測試通過")
        print(f"原文: {cn_sentence}")
        print(f"轉換: {result}")
        return True
    else:
        print("✗ 完整句子轉換測試失敗")
        print(f"原文: {cn_sentence}")
        print(f"實際: {result}")
        print(f"期望: {expected_tw}")
        return False

def test_convenience_functions():
    """測試便利函數"""
    print("\n測試便利函數...")
    
    cn_text = "這個程序使用算法處理數據"
    tw_text = "這個常式使用演算法處理資料"
    
    # 測試 cn_to_tw 函數
    result1 = cn_to_tw(cn_text)
    if tw_text in result1:  # 部分匹配因為可能有其他轉換
        print(f"✓ cn_to_tw: {cn_text} → {result1}")
        success1 = True
    else:
        print(f"✗ cn_to_tw: {cn_text} → {result1}")
        success1 = False
    
    # 測試 tw_to_cn 函數
    result2 = tw_to_cn(tw_text)
    if cn_text in result2:  # 部分匹配
        print(f"✓ tw_to_cn: {tw_text} → {result2}")
        success2 = True
    else:
        print(f"✗ tw_to_cn: {tw_text} → {result2}")
        success2 = False
    
    return success1 and success2

def test_search_and_lookup():
    """測試搜尋和查詢功能"""
    print("\n測試搜尋和查詢功能...")
    
    converter = TechTerminologyConverter()
    
    # 測試查詢功能
    mapping = converter.get_mapping("算法", "cn_to_tw")
    if mapping == "演算法":
        print("✓ 單詞查詢功能正常")
        lookup_success = True
    else:
        print(f"✗ 單詞查詢失敗: 算法 → {mapping}")
        lookup_success = False
    
    # 測試搜尋功能
    results = converter.search_terms("程序", "cn_to_tw")
    if len(results) > 0 and "應用程序" in results:
        print(f"✓ 搜尋功能正常，找到 {len(results)} 個相關術語")
        search_success = True
    else:
        print("✗ 搜尋功能失敗")
        search_success = False
    
    return lookup_success and search_success

def main():
    """執行所有測試"""
    print("台灣技術術語轉換器測試\n")
    
    tests = [
        test_basic_conversion,
        test_reverse_conversion,
        test_full_sentence,
        test_convenience_functions,
        test_search_and_lookup,
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"✗ 測試 {test_func.__name__} 發生錯誤: {e}")
    
    print(f"\n=== 測試總結 ===")
    print(f"總測試數: {total_tests}")
    print(f"通過測試: {passed_tests}")
    print(f"失敗測試: {total_tests - passed_tests}")
    
    if passed_tests == total_tests:
        print("🎉 所有測試通過！")
        return 0
    else:
        print("❌ 部分測試失敗")
        return 1

if __name__ == "__main__":
    sys.exit(main())