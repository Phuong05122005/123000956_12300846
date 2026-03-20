# app.py
import streamlit as st
from underthesea import word_tokenize, pos_tag
import pandas as pd

st.set_page_config(page_title="Demo POS Tagging Tiếng Việt", layout="wide")

st.title("Demo POS Tagging Tiếng Việt với Streamlit")
st.write("Nhập một câu tiếng Việt, ứng dụng sẽ tách từ và gán nhãn từ loại.")

# Input
text = st.text_area(
    "Nhập câu tiếng Việt ở đây:",
    "Hệ thống phân loại bình luận tiếng Việt rất chính xác.",
    height=100
)

analyze_clicked = st.button("🔍 Phân tích", type="primary", width="stretch")

col1, col2 = st.columns(2)

# Bảng giải thích nhãn từ loại
POS_TAGS_EXPLANATION = {
    "N": "Danh từ", "Np": "Danh từ riêng", "Nc": "Danh từ chỉ loại",
    "Nu": "Danh từ đơn vị", "V": "Động từ", "A": "Tính từ",
    "P": "Đại từ", "R": "Phó từ", "L": "Định từ", "M": "Số từ",
    "E": "Giới từ", "C": "Liên từ", "I": "Thán từ",
    "T": "Trợ từ, tiểu từ", "B": "Từ gốc Hán-Việt",
    "Y": "Từ viết tắt", "S": "Từ ngoại lai",
    "X": "Từ không phân loại", "CH": "Dấu câu",
}

# Màu cho từng loại từ loại
POS_COLORS = {
    "N": "#FF6B6B", "Np": "#FF4444", "Nc": "#FF8888", "Nu": "#FFAAAA",
    "V": "#4ECDC4", "A": "#FFE66D", "P": "#A8E6CF", "R": "#95E1D3",
    "L": "#DDA0DD", "M": "#87CEEB", "E": "#FFA07A", "C": "#98D8C8",
    "I": "#F7DC6F", "T": "#BB8FCE", "B": "#F0B27A", "Y": "#AED6F1",
    "S": "#F5B7B1", "X": "#D5DBDB", "CH": "#BDC3C7",
}

# Lưu kết quả vào session_state
if analyze_clicked:
    if not text.strip():
        st.error("⚠️ Vui lòng nhập nội dung!")
        st.session_state.pop("pos_result", None)
        st.session_state.pop("pos_tokens", None)
        st.session_state.pop("pos_text", None)
    else:
        st.session_state["pos_text"] = text
        st.session_state["pos_tokens"] = word_tokenize(text)
        st.session_state["pos_result"] = pos_tag(text)

if "pos_result" in st.session_state:
    pos_result = st.session_state["pos_result"]
    tokens = st.session_state["pos_tokens"]

    # ==================== CỘT 1: TOKENIZE ====================
    with col1:
        st.subheader("🔤 Kết quả Tokenization")
        token_df = pd.DataFrame({"Token": tokens})
        st.dataframe(token_df, use_container_width=True)

    # ==================== CỘT 2: POS TAGGING ====================
    with col2:
        st.subheader("🏷️ Kết quả POS Tagging")
        pos_df = pd.DataFrame(pos_result, columns=["Từ", "Nhãn"])
        st.dataframe(pos_df, use_container_width=True)

    # ==================== HIGHLIGHT MÀU ====================
    st.subheader("🌈 Câu gốc với highlight màu theo từ loại")
    colored_html = " ".join([
        f'<span style="background-color: {POS_COLORS.get(tag, "#D5DBDB")}; '
        f'color: #000000; padding: 4px 8px; border-radius: 6px; margin: 2px; '
        f'display: inline-block;">{word} <small style="opacity:0.7;">({tag})</small></span>'
        for word, tag in pos_result
    ])
    st.markdown(colored_html, unsafe_allow_html=True)

    # ==================== EXPORT CSV ====================
    st.subheader("📥 Xuất kết quả")
    export_df = pd.DataFrame(pos_result, columns=["Từ", "Nhãn"])
    csv_data = export_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📄 Tải file CSV",
        data=csv_data,
        file_name="pos_tagging_result.csv",
        mime="text/csv",
        use_container_width=True
    )

# ==================== BẢNG GIẢI THÍCH (luôn hiển thị + CÓ MÀU) ====================
st.subheader("📋 Bảng giải thích các nhãn từ loại (POS Tags)")

exp_df = pd.DataFrame(
    list(POS_TAGS_EXPLANATION.items()),
    columns=["Nhãn", "Giải thích"]
)

# Hàm style màu cho từng dòng theo POS_COLORS
def highlight_row(row):
    color = POS_COLORS.get(row["Nhãn"], "#D5DBDB")
    return [f'background-color: {color}; color: #000000; font-weight: bold;' for _ in row]

# Áp dụng style
styled_exp = exp_df.style.apply(highlight_row, axis=1)

st.dataframe(
    styled_exp,
    use_container_width=True,
    hide_index=True
)

st.caption("🚀 Demo được xây dựng bằng underthesea + Streamlit. Chúc bạn học NLP vui vẻ!")