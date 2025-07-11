import csv
import re

# 讀取 CSV
terms = []
with open('terms.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        terms.append(f"- {row['cn']} → {row['tw']}")

# 讀取 README
with open('README.md', encoding='utf-8') as f:
    readme = f.read()

# 定位區塊
pattern = re.compile(
    r'(請將以下文本中的技術術語進行轉換。轉換規則如下：)([\s\S]*?)(\[在此處插入需要轉換的文本\])',
    re.MULTILINE
)

# 生成新區塊
terms_block = '\n' + '\n'.join(terms) + '\n'

# 替換
new_readme, count = pattern.subn(r'\1' + terms_block + r'\3', readme)
if count == 0:
    raise RuntimeError('未找到術語表區塊，請確認 README 格式')

# 寫回 README
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_readme) 