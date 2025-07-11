## 功能

- ✅ **自動爬取**：從維基教科書自動取得最新的術語對照表
- ✅ **智慧合併**：與現有術語表智慧合併，避免重複
- ✅ **自動更新**：每週自動執行更新流程
- ✅ **備份機制**：更新前自動建立備份檔案
- ✅ **Log 記錄**：詳細記錄更新過程和變更內容

## 檔案結構

```
tw-cn-terminologies/
├── .github/workflows/update-terms.yml  # GitHub Actions 工作流程
├── scripts/
│   ├── scrape_wiki_terms.py           # 爬蟲主程式
│   └── test_scraper.py                # 測試腳本
├── terms.csv                          # 術語對照表
├── update_terms.py                    # README 更新腳本
├── requirements.txt                   # Python 依賴
└── README.md                          # 專案說明
```

## 使用方法

### 1. 本地測試

```bash
# 安裝依賴
pip install -r requirements.txt

# 測試爬蟲功能
python scripts/test_scraper.py

# 手動執行更新
python scripts/scrape_wiki_terms.py
python update_terms.py
```

### 2. 自動化更新

GitHub Actions 會自動執行以下流程：

1. **定時觸發**：每週一凌晨 2 點自動執行
2. **手動觸發**：可在 GitHub Actions 頁面手動觸發
3. **爬取資料**：從維基教科書取得最新術語對照表
4. **智慧合併**：與現有資料合併，新增和更新術語
5. **更新文件**：自動更新 README 中的術語清單
6. **繳交變更**：自動繳交並推送變更

### 3. 監控更新

- 查看 GitHub Actions 頁面的執行記錄
- 檢查 `terms.csv` 檔案的變更歷史
- 查看備份檔案了解更新前的狀態

## 設定選項

### 修改更新頻率

編輯 `.github/workflows/update-terms.yml` 中的 cron 表達式：

```yaml
schedule:
  - cron: '0 2 * * 1'  # 每週一凌晨 2 點
```

### 修改資料源

編輯 `scripts/scrape_wiki_terms.py` 中的 URL：

```python
self.url = "https://zh.wikibooks.org/w/index.php?title=%E5%A4%A7%E9%99%86%E5%8F%B0%E6%B9%BE%E8%AE%A1%E7%AE%97%E6%9C%BA%E6%9C%AF%E8%AF%AD%E5%AF%B9%E7%85%A7%E8%A1%A8&variant=zh"
```

## 故障排除

### 常見問題

1. **爬蟲失敗**
   - 檢查網路連線
   - 確認維基教科書頁面可存取
   - 查看記錄中的錯誤訊息

2. **解析失敗**
   - 檢查維基教科書頁面結構是否變化
   - 更新解析邏輯

3. **GitHub Actions 失敗**
   - 檢查工作流程設定
   - 確認權限設定正確

### 記錄分析

爬蟲會輸出詳細的記錄訊息：

```
2025-07-11 12:47:16,268 - INFO - 新增 452 個術語，更新 12 個術語
2025-07-11 12:47:16,268 - INFO - 建立備份: terms.csv.backup.20250711_124716
2025-07-11 12:47:16,288 - INFO - 成功儲存 977 個術語到 terms.csv
```

## 技術細節

### 相依函式庫

- `requests`: HTTP 請求
- `beautifulsoup4`: HTML 解析
- `pandas`: 資料處理
- `lxml`: XML/HTML 解析器

### 資料格式

CSV 檔案格式：
```csv
cn,tw
摘要,摘要
抽象的,抽象的
抽象,抽象
...
```

### 備份機制

每次更新前會建立備份檔案：
```
terms.csv.backup.YYYYMMDD_HHMMSS
```

## 刪除/修改詞彙與保護本地內容

請使用 `scripts/modify_term.py` 來刪除或修改詞彙，會自動記錄到 `deleted_terms.txt`，未來自動合併時不會自動加回你刪掉的內容。

### modify_term.py 用法
- 修改對應內容：「python scripts/modify_term.py 配置 組態;設定」
- 刪除整組：「python scripts/modify_term.py 文本」
- 刪除部分對應：「python scripts/modify_term.py 配置 組態」

### deleted_terms.txt 格式
- 每行：「中國大陸詞,台灣詞1;台灣詞2...」
- 只刪除部分對應時，可多行記錄同一個中國大陸詞。

#### 範例：
```
配置,配置
文本,文字
```

### 合併邏輯
- 合併時只會加回 deleted_terms.txt 以外的新內容。
- 若要以本地內容為合併基準，請將 `terms.csv` 複製為 `wiki_terms_snapshot.csv`。