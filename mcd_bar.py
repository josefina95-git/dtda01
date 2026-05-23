# ============================================================
# 修改後 ── 日別發票數量分布（長條圖 + 月/日標籤）
# ============================================================
import pathlib
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="日別分布", layout="wide")
st.title("日別發票數量分布（長條圖）")
st.caption("資料來源：mcd_night.csv") # 或是你原本的 orders.csv 都可以

# 假設資料夾結構與你之前練習相同，這裡讀取你之前產出的 mcd_night.csv
# 💡 注意：加上 parse_dates 讓 pandas 自動把該欄位識別為時間
# ──── 改成這樣 ────
df = pd.read_csv("./mcd_night.csv", parse_dates=["inv_date"])

# ── 步驟 1 & 2：將日期轉換為 "MM/DD" 的格式（例如：10/15） ─────────────────────
# 💡 .dt.strftime() 是一個非常強大的讀取時間函式，%m 代表月份，%d 代表日期
df["日期"] = df["inv_date"].dt.strftime('%m/%d')

# ── 步驟 3：按「日期」分組統計，並計算發票數量 ──────────────────────────────
# 💡 使用 .nunique() 可以精準計算出當天有幾個「不重複」的發票號碼
daily_df = df.groupby("日期")["inv_num"].nunique().reset_index(name="發票數量")

# 如果你想確保日期是依照時間先後順序排列，可以補上這行排序：
daily_df = daily_df.sort_values("日期")

st.dataframe(daily_df, use_container_width=True)
st.markdown("---")

# ── 步驟 4：畫長條圖 ──────────────────────────────────────────────────
fig = px.bar(
    daily_df,
    x="日期",       # X軸：10/15, 10/16...
    y="發票數量",    # Y軸：當日發票數量
    title="每日發票數量趨勢分布",
    color="發票數量",
    color_continuous_scale="RdYlGn",   # 紅（低）→ 黃 → 綠（高）
)

fig.update_layout(
    coloraxis_showscale=False,
    xaxis_title="日期",
    yaxis_title="發票數量 (筆)",
    # 💡 技巧：當日期很多天時，強制 X 軸每個標籤都要秀出來，不會被 plotly 自動省略
    xaxis={'type': 'category'} 
)

st.plotly_chart(fig, use_container_width=True)
