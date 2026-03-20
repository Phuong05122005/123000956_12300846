# app.py
import streamlit as st
from underthesea import word_tokenize, pos_tag
import pandas as pd

st.set_page_config(page_title="Demo POS Tagging Tiếng Việt", layout="wide")

st.title("Demo POS Tagging Tiếng Việt")
st.write("Nhập câu tiếng Việt, ứng dụng sẽ tách từ và gán nhãn từ loại.")

# Input
text = st.text_area(
    "Nhập câu tiếng Việt ở đây:",
    "Hệ thống phân loại bình luận tiếng Việt rất chính xác.",
    height=100
)

analyze_clicked = st.button("🔍 Phân tích", type="primary", use_container_width=True)

col1, col2 = st.columns(2)

# =========================
# 🎨 MÀU PASTEL DỊU MẮT
# =========================
POS_COLORS = {
    "N": "#F8BBD0",
    "Np": "#F48FB1",
    "Nc": "#FADADD",
    "Nu": "#E8F5E9",
    "V": "#B2DFDB",
    "A": "#FFF9C4",
    "P": "#D1C4E9",
    "R": "#C8E6C9",
    "L": "#E1BEE7",
    "M": "#BBDEFB",
    "E": "#FFE0B2",
    "C": "#B2EBF2",
    "I": "#FFF3E0",
    "T": "#E6EE9C",
    "B": "#FFCCBC",
    "Y": "#CFD8DC",
    "S": "#F3E5F5",
    "X": "#ECEFF1",
    "CH": "#E0E0E0",
}

POS_TAGS_EXPLANATION = {
    "N": "Danh từ",
    "Np": "Danh từ riêng",
    "Nc": "Danh từ chỉ loại",
    "Nu": "Danh từ đơn vị",
    "V": "Động từ",
    "A": "Tính từ",
    "P": "Đại từ",
    "R": "Phó từ",
    "L": "Định từ",
    "M": "Số từ",
    "E": "Giới từ",
    "C": "Liên từ",
    "I": "Thán từ",
    "T": "Trợ từ",
    "B": "Hán-Việt",
    "Y": "Viết tắt",
    "S": "Ngoại lai",
    "X": "Không rõ",
    "CH": "Dấu câu",
}

# =========================
# 📥 EXPORT CSV
# =========================
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# =========================
# 🚀 MAIN
# =========================
if analyze_clicked:

    # ❌ Validate input
    if not text.strip():
        st.error("⚠️ Vui lòng nhập nội dung!")
    else:
        tokens = word_tokenize(text)
        pos_result = pos_tag(text)

        df = pd.DataFrame(pos_result, columns=["Word", "POS"])

        # =========================
        # 🧩 TOKENIZE + HIGHLIGHT POS
        # =========================
        with col1:
            st.subheader("🧩 Tokenize + POS Highlight")

            token_html = ""
            for word, pos in pos_result:
                color = POS_COLORS.get(pos, "#FFFFFF")

                token_html += f"""
                <span style="
                    display:inline-block;
                    padding:8px 12px;
                    margin:4px;
                    background:{color};
                    color:#2d3436;
                    border-radius:10px;
                    font-weight:500;
                    border:1px solid #dfe6e9;
                ">
                    {word} ({pos})
                </span>
                """

            st.markdown(token_html, unsafe_allow_html=True)

        # =========================
        # 🏷️ POS TABLE
        # =========================
        with col2:
            st.subheader("🏷️ POS Tagging Table")

            def highlight_pos(val):
                color = POS_COLORS.get(val, "#FFFFFF")
                return f"background-color: {color}; color:#2d3436; font-weight:500"

            st.dataframe(
                df.style.applymap(highlight_pos, subset=["POS"]),
                use_container_width=True
            )

        # =========================
        # 📥 EXPORT CSV
        # =========================
        csv = convert_df(df)

        st.download_button(
            label="📥 Tải CSV",
            data=csv,
            file_name="pos_tagging.csv",
            mime="text/csv",
        )

# =========================
# 📘 POS EXPLANATION
# =========================
st.markdown("---")
st.subheader("📘 Bảng giải thích POS")

pos_df = pd.DataFrame(
    [(k, v) for k, v in POS_TAGS_EXPLANATION.items()],
    columns=["Tag", "Ý nghĩa"]
)

def highlight_tag(row):
    color = POS_COLORS.get(row["Tag"], "#FFFFFF")
    return [
        f"background-color: {color}; color:#2d3436; font-weight:600",
        f"background-color: {color}; color:#2d3436"
    ]

st.dataframe(
    pos_df.style.apply(highlight_tag, axis=1),
    use_container_width=True
)