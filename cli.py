#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taiwan Tech Terminology Converter CLI

Command-line interface for converting technical terminology between 
Simplified Chinese (China Mainland) and Traditional Chinese (Taiwan).
"""

import argparse
import sys
from pathlib import Path
from tech_terminology_converter import TechTerminologyConverter

def main():
    parser = argparse.ArgumentParser(
        description="台灣技術術語轉換器 - 簡體中文（大陸）與繁體中文（台灣）技術術語互轉工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  %(prog)s -d cn_to_tw "這個應用程序使用了最新的算法"
  %(prog)s -d tw_to_cn "這個應用程式使用了最新的演算法"
  %(prog)s -f input.txt -o output.txt -d cn_to_tw
  %(prog)s --search "程序" -d cn_to_tw
  %(prog)s --stats
        """)
    
    parser.add_argument(
        'text', 
        nargs='?', 
        help='要轉換的文本（如果未指定 -f 參數）'
    )
    
    parser.add_argument(
        '-d', '--direction',
        choices=['cn_to_tw', 'tw_to_cn'],
        default='cn_to_tw',
        help='轉換方向：cn_to_tw (簡體→繁體台灣) 或 tw_to_cn (繁體台灣→簡體) [預設: cn_to_tw]'
    )
    
    parser.add_argument(
        '-f', '--file',
        type=str,
        help='輸入檔案路徑'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='輸出檔案路徑（未指定則輸出到終端）'
    )
    
    parser.add_argument(
        '-v', '--vocabulary',
        type=str,
        help='自訂詞彙檔案路徑 (JSON格式)'
    )
    
    parser.add_argument(
        '--search',
        type=str,
        help='搜尋包含指定關鍵字的術語映射'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='顯示詞彙庫統計信息'
    )
    
    parser.add_argument(
        '--lookup',
        type=str,
        help='查詢特定術語的對應詞彙'
    )
    
    args = parser.parse_args()
    
    try:
        # 初始化轉換器
        converter = TechTerminologyConverter(args.vocabulary)
        
        # 顯示統計信息
        if args.stats:
            stats = converter.get_statistics()
            print("=== 詞彙庫統計信息 ===")
            print(f"簡→繁映射數量: {stats['cn_to_tw_mappings']}")
            print(f"繁→簡映射數量: {stats['tw_to_cn_mappings']}")
            print(f"詞彙檔案: {stats['vocabulary_file']}")
            print(f"版本: {stats['version']}")
            print(f"描述: {stats['description']}")
            return
        
        # 搜尋術語
        if args.search:
            results = converter.search_terms(args.search, args.direction)
            if results:
                direction_desc = "簡體→繁體(台灣)" if args.direction == "cn_to_tw" else "繁體(台灣)→簡體"
                print(f"=== 搜尋結果 ({direction_desc}) ===")
                for source, target in results.items():
                    print(f"{source} → {target}")
            else:
                print(f"未找到包含 '{args.search}' 的術語")
            return
        
        # 查詢特定術語
        if args.lookup:
            result = converter.get_mapping(args.lookup, args.direction)
            if result:
                direction_desc = "簡體→繁體(台灣)" if args.direction == "cn_to_tw" else "繁體(台灣)→簡體"
                print(f"{args.lookup} → {result} ({direction_desc})")
            else:
                print(f"未找到術語 '{args.lookup}' 的對應詞彙")
            return
        
        # 處理文本轉換
        if args.file:
            # 從檔案讀取
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    input_text = f.read()
            except FileNotFoundError:
                print(f"錯誤: 找不到檔案 '{args.file}'", file=sys.stderr)
                sys.exit(1)
            except UnicodeDecodeError:
                print(f"錯誤: 無法讀取檔案 '{args.file}'，請確認檔案編碼為 UTF-8", file=sys.stderr)
                sys.exit(1)
        elif args.text:
            # 從命令列參數讀取
            input_text = args.text
        else:
            # 從標準輸入讀取
            input_text = sys.stdin.read()
        
        if not input_text.strip():
            print("錯誤: 沒有輸入文本", file=sys.stderr)
            sys.exit(1)
        
        # 進行轉換
        converted_text = converter.convert(input_text, args.direction)
        
        # 輸出結果
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(converted_text)
                print(f"轉換完成，結果已儲存到 '{args.output}'")
            except Exception as e:
                print(f"錯誤: 無法寫入檔案 '{args.output}': {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print(converted_text)
    
    except FileNotFoundError as e:
        print(f"錯誤: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"錯誤: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未預期的錯誤: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()