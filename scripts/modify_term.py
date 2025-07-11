#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動從 terms.csv 修改或刪除指定詞彙的對應內容，刪除時才記錄到 deleted_terms.txt，確保冪等性。
"""

import csv
import sys
import os
import argparse

TERMS_FILE = 'terms.csv'
DELETED_TERMS_FILE = 'deleted_terms.txt'

def modify_term(cn_term, new_tw=None, delete_mode=False):
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
                    if delete_mode:
                        continue  # 不寫入 terms.csv
                    else:
                        # 修改模式下，整組刪除等同於刪除
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

    if not delete_mode:
        print(f"已修改 {cn_term} 對應內容，未記錄到 deleted_terms.txt（冪等）")
        return

    # 記錄到 deleted_terms.txt（避免重複，僅刪除模式）
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
    parser = argparse.ArgumentParser(description='修改或刪除 terms.csv 的對應內容。')
    parser.add_argument('cn_term', help='中國大陸詞')
    parser.add_argument('new_tw', nargs='?', default=None, help='新的台灣詞（多個用分號分隔）')
    parser.add_argument('--delete', '-d', action='store_true', help='刪除模式，會記錄到 deleted_terms.txt')
    args = parser.parse_args()
    modify_term(args.cn_term, args.new_tw, args.delete) 