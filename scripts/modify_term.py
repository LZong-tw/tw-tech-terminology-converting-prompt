#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動從 terms.csv 修改或刪除指定詞彙的對應內容，並記錄移除的對應到 deleted_terms.txt
"""

import csv
import sys
import os

TERMS_FILE = 'terms.csv'
DELETED_TERMS_FILE = 'deleted_terms.txt'

def update_term(cn_term, new_tw=None):
    # 讀取現有 terms
    terms = []
    old_tw_set = set()
    found = False
    with open(TERMS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['cn'] == cn_term:
                found = True
                old_tw_set = set(t.strip() for t in row['tw'].split(';') if t.strip())
                if new_tw is None or not new_tw.strip():
                    # 整組刪除
                    continue
                else:
                    new_tw_set = set(t.strip() for t in new_tw.split(';') if t.strip())
                    # 只保留新內容
                    if new_tw_set:
                        row['tw'] = ';'.join(sorted(new_tw_set))
                        terms.append(row)
            else:
                terms.append(row)
    if not found:
        print(f'未找到詞彙：{cn_term}')
        return

    # 寫回 terms.csv
    with open(TERMS_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['cn', 'tw'])
        writer.writeheader()
        for row in terms:
            writer.writerow(row)

    # 記錄到 deleted_terms.txt（避免重複）
    already = set()
    if os.path.exists(DELETED_TERMS_FILE):
        with open(DELETED_TERMS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    already.add(line)

    # 記錄被移除的對應
    if new_tw is None or not new_tw.strip():
        # 整組刪除
        for tw in sorted(old_tw_set):
            record = f"{cn_term},{tw}"
            if record not in already:
                with open(DELETED_TERMS_FILE, 'a', encoding='utf-8') as f:
                    f.write(record + '\n')
                print(f"已刪除並記錄：{record}")
            else:
                print(f"已刪除，記錄已存在：{record}")
    else:
        new_tw_set = set(t.strip() for t in new_tw.split(';') if t.strip())
        removed = old_tw_set - new_tw_set
        for tw in sorted(removed):
            record = f"{cn_term},{tw}"
            if record not in already:
                with open(DELETED_TERMS_FILE, 'a', encoding='utf-8') as f:
                    f.write(record + '\n')
                print(f"已移除並記錄：{record}")
            else:
                print(f"已移除，記錄已存在：{record}")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        update_term(sys.argv[1])
    elif len(sys.argv) == 3:
        update_term(sys.argv[1], sys.argv[2])
    else:
        print("用法: python scripts/update_term.py <中國大陸詞> [新台灣詞(多個用分號分隔)]")
        sys.exit(1) 