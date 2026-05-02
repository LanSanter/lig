# One-shot Sample 使用方式

1. 範例資料存放於 `backend/data/oneshot_samples.json`。
2. 由 `backend/services/sample_loader.py` 的 `load_oneshot_samples()` 載入（含 LRU cache）。
3. `scenario_expander.py` 會使用 one-shot 樣本生成候選情境語氣與 trigger。
4. `draft_generator.py` 會根據輸入關鍵詞匹配對應 trigger，若無命中則退回通用策略。
