#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動從 terms.csv 刪除指定詞彙的部分或全部對應，並記錄到 deleted_terms.txt
"""

import csv
import sys
import os

TERMS_FILE = 'terms.csv'
DELETED_TERMS_FILE = 'deleted_terms.txt'

def delete_term(cn_term, tw_term=None):
    # 讀取現有 terms
    terms = []
    deleted_tw = None
    found = False
    with open(TERMS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['cn'] == cn_term:
                tws = [t.strip() for t in row['tw'].split(';') if t.strip()]
                if tw_term is None:
                    # 整組刪除
                    deleted_tw = row['tw']
                    continue
                else:
                    # 部分刪除
                    if tw_term in tws:
                        tws.remove(tw_term)
                        deleted_tw = tw_term
                        found = True
                        if tws:
                            row['tw'] = ';'.join(tws)
                            terms.append(row)
                        # else: 全部刪除，不加回
                    else:
                        terms.append(row)
            else:
                terms.append(row)
    if deleted_tw is None and not found:
        print(f'未找到詞彙或對應內容：{cn_term} {tw_term if tw_term else ""}')
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
    if tw_term is None:
        record = f"{cn_term},{deleted_tw}"
    else:
        record = f"{cn_term},{tw_term}"
    if record not in already:
        with open(DELETED_TERMS_FILE, 'a', encoding='utf-8') as f:
            f.write(record + '\n')
        print(f"已刪除並記錄：{record}")
    else:
        print(f"已刪除，記錄已存在：{record}")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        delete_term(sys.argv[1])
    elif len(sys.argv) == 3:
        delete_term(sys.argv[1], sys.argv[2])
    else:
        print(\"用法: python scripts/delete_term.py <中國大陸詞> [台灣詞]\")
        sys.exit(1)