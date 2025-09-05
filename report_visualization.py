# -*- coding: utf-8 -*-
# Pilot evaluation visualization (robust, cross-platform)
# Requirements: pandas, matplotlib

import os, json
from typing import List, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# ====== 0) 경로 설정 ======
# 로컬(윈도우) 예시
DATA_PATH  = r"C:\dev\oclabDev\KCI_data\Evaluation_Report_V01.jsonl"
RESULT_DIR = r"C:\dev\oclabDev\KCI_data\result"

# 콜랩/리눅스에서 돌릴 때는 위 두 줄 대신 아래처럼 바꿔도 됨:
# DATA_PATH  = "/mnt/data/pilot_eval_results (6).jsonl"
# RESULT_DIR = "/mnt/data/kci_results"

os.makedirs(RESULT_DIR, exist_ok=True)

SCORE_COLS = ["accuracy", "explainability", "consistency", "safety"]

# ====== 1) JSONL 로드 ======
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"File not found: {DATA_PATH}")

records: List[Dict[str, Any]] = []
with open(DATA_PATH, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except Exception:
            # 파싱 실패 라인은 스킵
            pass

if not records:
    raise ValueError("No valid JSON objects found.")

# ====== 2) 점수 추출 → DataFrame ======
def extract_scores(obj: Dict[str, Any]) -> Dict[str, Any]:
    ev = obj.get("eval") or {}
    out = {"id": obj.get("id") or obj.get("case_id")}
    for k in SCORE_COLS:
        v = ev.get(k, {})
        out[k] = v.get("score")
    return out

df = pd.DataFrame([extract_scores(o) for o in records])

# 숫자화 & 전부 결측이면 삭제
for col in SCORE_COLS:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=SCORE_COLS, how="all").reset_index(drop=True)
if df.empty:
    raise ValueError("No rows contained evaluation scores after cleaning.")

# ====== 3) 요약 통계 ======
summary = pd.DataFrame({
    "metric": SCORE_COLS,
    "mean": [df[c].mean(skipna=True) for c in SCORE_COLS],
    "std":  [df[c].std(skipna=True)  for c in SCORE_COLS],
    "min":  [df[c].min(skipna=True)  for c in SCORE_COLS],
    "max":  [df[c].max(skipna=True)  for c in SCORE_COLS],
    "count":[df[c].count()           for c in SCORE_COLS],
})

# 저장
tidy_csv      = os.path.join(RESULT_DIR, "pilot_eval_scores.csv")
summary_csv   = os.path.join(RESULT_DIR, "pilot_eval_summary.csv")
df.to_csv(tidy_csv, index=False)
summary.to_csv(summary_csv, index=False)

# ====== 4) 시각화 ======
plt.rcParams.update({"figure.dpi": 140})  # 선명도만 약간

# 4-1) 평균±표준편차 바차트
means = summary.set_index("metric")["mean"].reindex(SCORE_COLS)
stds  = summary.set_index("metric")["std"].reindex(SCORE_COLS).fillna(0.0)

plt.figure()
plt.title("Pilot Evaluation: Mean Scores ± Std")
plt.xlabel("Metric"); plt.ylabel("Score (1–5)")
x = range(len(SCORE_COLS))
plt.bar(list(x), means.values, yerr=stds.values, capsize=5)
plt.xticks(list(x), SCORE_COLS); plt.ylim(0, 5)
mean_fig = os.path.join(RESULT_DIR, "mean_scores_with_std.png")
plt.tight_layout(); plt.savefig(mean_fig, bbox_inches="tight"); plt.show()

# 4-2) 박스플롯(지표별)
for col in SCORE_COLS:
    ser = df[col].dropna()
    if ser.empty:
        continue
    plt.figure()
    plt.title(f"Distribution of {col.capitalize()} Scores")
    plt.ylabel("Score (1–5)")
    plt.boxplot(ser.values, vert=True)
    plt.ylim(0, 5)
    fig_path = os.path.join(RESULT_DIR, f"boxplot_{col}.png")
    plt.tight_layout(); plt.savefig(fig_path, bbox_inches="tight"); plt.show()

# 4-3) 빈도 바차트(1~5)
freq_rows = []
for col in SCORE_COLS:
    ser = df[col].dropna()
    if ser.empty:
        continue
    # (안전) 1~5 범위로 반올림 후 클리핑
    ser = ser.round().clip(1, 5).astype(int)
    counts = Counter(ser.tolist())
    xs = [1, 2, 3, 4, 5]
    ys = [counts.get(i, 0) for i in xs]

    plt.figure()
    plt.title(f"{col.capitalize()} Score Frequencies")
    plt.xlabel("Score"); plt.ylabel("Count")
    plt.bar(xs, ys)
    freq_fig = os.path.join(RESULT_DIR, f"frequencies_{col}.png")
    plt.tight_layout(); plt.savefig(freq_fig, bbox_inches="tight"); plt.show()

    row = {"metric": col, **{f"score_{s}": counts.get(s, 0) for s in xs}}
    freq_rows.append(row)

freq_df = pd.DataFrame(freq_rows)
freq_csv = os.path.join(RESULT_DIR, "pilot_eval_score_frequencies.csv")
freq_df.to_csv(freq_csv, index=False)

print("Saved files:")
print(f"- Tidy CSV: {tidy_csv}")
print(f"- Summary CSV: {summary_csv}")
print(f"- Mean±Std chart: {mean_fig}")
for col in SCORE_COLS:
    print(f"- Boxplot ({col}): {os.path.join(RESULT_DIR, f'boxplot_{col}.png')}")
for col in SCORE_COLS:
    print(f"- Frequencies ({col}): {os.path.join(RESULT_DIR, f'frequencies_{col}.png')}")
