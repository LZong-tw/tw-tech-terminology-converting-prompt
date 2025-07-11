import csv
import re
from hanziconv import HanziConv

# 讀取 CSV
terms = []
with open('terms.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        terms.append(f"- {HanziConv.toTraditional(row['cn'])} → {row['tw']}")

# 讀取 README
with open('README.md', encoding='utf-8') as f:
    readme = f.read()

# 定位區塊
pattern = re.compile(
    r'(請將以下文本中的技術術語進行轉換。轉換規則如下：)([\s\S]*?)(\[在此處插入需要轉換的文本\])',
    re.MULTILINE
)

# 生成新區塊，補上所有標題和說明
terms_block = (
    '\n### 中國大陸簡體 → 台灣繁體術語對照表：\n'
    + '\n'.join(terms) + '\n\n'
    + '### 轉換指示：\n'
    + '1. 請將文本中出現的中國大陸術語轉換為對應的台灣術語\n'
    + '2. 保持其他內容不變\n'
    + '3. 注意上下文，選擇最合適的轉換詞彙\n'
    + '4. 如果同一個中國大陸術語有多個台灣對應詞彙，請根據上下文選擇最合適的\n\n'
    + '### 要轉換的文本：\n'
)

# 替換
new_readme, count = pattern.subn(r'\1' + terms_block + r'\3', readme)
if count == 0:
    raise RuntimeError('未找到術語表區塊，請確認 README 格式')

# 寫回 README
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_readme)