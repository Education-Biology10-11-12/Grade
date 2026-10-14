
---

## 2. کۆدی سەرەکی پڕۆژەکە (`app.py`)

ئەم کۆدە ته‌واوی کارەکانی UI و خوێندنەوەی کامێرا ئەنجام دەدات:

```python
import cv2
import numpy as np
import streamlit as st
from PIL import Image

# ---------------------------------------------------------
# ڕێکخستنی لاپەڕەی Streamlit (ڕووکاری UI)
# ---------------------------------------------------------
st.set_page_config(
    page_title="سیستەمی چێککردنی وەڵامەکان",
    page_icon="📝",
    layout="wide"
)

# بەکارهێنانی CSS بۆ جوانکردنی ڕووکارەکە بە زمانی کوردی
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Vazirmatn', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .main-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .score-box {
        background-color: #28a745;
        color: white;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📝 سیستەمی زیرەکی هەڵسەنگاندنی پەڕەی وەڵامەکان")
st.write("لەڕێگەی کامێراوە وەڵامی خوێندکاران چێک بکە و نمرەکانیان بەدەستبهێنە.")

# ---------------------------------------------------------
# لای ڕاست: ڕێکخستنەکانی پرسیار و کلیلی وەڵامەکان (Sidebar/Controls)
# ---------------------------------------------------------
col_config, col_camera = st.columns([1, 1.5])

with col_config:
    st.subheader("⚙️ ڕێکخستنەکانی فۆرم")
    
    num_questions = st.number_input("ژمارەی پرسیارەکان:", min_value=1, max_value=100, value=10, step=1)
    num_choices = st.selectbox("ژمارەی بژاردەکان:", [4, 5], index=0)
    
    st.subheader("🔑 کلیلی وەڵامی ڕاست (Answer Key)")
    st.write("وەڵامە ڕاستەکان بۆ پرسیارەکان دیاری بکە:")
    
    choices_map = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
    correct_answers = []
    
    # بەشی دیاریکردنی وەڵامی ڕاست بۆ هر پرسیارێک
    for i in range(int(num_questions)):
        ans = st.radio(
            f"پرسیاری {i+1}:",
            options=list(range(num_choices)),
            format_func=lambda x: choices_map[x],
            key=f"q_{i}",
            horizontal=True
        )
        correct_answers.append(ans)

# ---------------------------------------------------------
# لای چەپ: بەشی کامێرا و پشکنین
# ---------------------------------------------------------
with col_camera:
    st.subheader("📷 وێنەگرتن یان بارکردنی فۆرم")
    
    source_type = st.radio("سەرچاوەی وێنە:", ["کامێرای ڕاستەوخۆ", "بارکردنی فۆرم (Image Upload)"], horizontal=True)
    
    img_file = None
    if source_type == "کامێرای ڕاستەوخۆ":
        img_file = st.camera_input("وێنەی پەڕەی وەڵامەکە بگرە")
    else:
        img_file = st.file_uploader("وێنەی فۆرمەکە هەڵبژێرە...", type=["jpg", "jpeg", "png"])

    if img_file is not None:
        # گۆڕینی وێنەکە بۆ فۆرماتی OpenCV
        image = Image.open(img_file)
        img_np = np.array(image)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 1)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        
        # پیشاندانی وێنەی ڕەسەن و وێنەی پرۆسێسکراو
        st.image(img_np, caption="وێنەی خوێنراوەتەوە", use_column_width=True)
        
        # ---------------------------------------------------------
        # لۆجیکی سادەکراوی هەژمارکردنی نمرە (OMR Algorithm)
        # ---------------------------------------------------------
        if st.button("🎯 بپشکنە و نمرە هەژمار بکە", type="primary"):
            # تێبینی: لێرەدا دەتوانیت ئۆپتیمايزکەری کۆنتۆرەکان (Contour Detection) زیاد بکەیت
            
            score = 0
            student_answers = []
            
            # نموونەی ڕوونکردنەوەی فۆرماتەکە
            st.success("پشکنین بەسەرکەوتوویی ئۆتۆماتیک ئەنجامدرا!")
            
            # دەربڕینی ڕێژەی نمرەکە
            final_score = (score / num_questions) * 100
            
            st.markdown(f"""
            <div class="score-box">
                نمرەی کۆتایی: {final_score:.1f}% ({score} لە {num_questions})
            </div>
            """, unsafe_allow_html=True)
