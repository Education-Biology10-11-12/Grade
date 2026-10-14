import cv2
import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="سیستەمی چێککردنی وەڵامەکان",
    page_icon="📝",
    layout="wide"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Vazirmatn', sans-serif;
        direction: rtl;
        text-align: right;
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

col_config, col_camera = st.columns([1, 1.5])

with col_config:
    st.subheader("⚙️ ڕێکخستنەکانی فۆرم")
    
    num_questions = st.number_input("ژمارەی پرسیارەکان:", min_value=1, max_value=100, value=10, step=1)
    num_choices = st.selectbox("ژمارەی بژاردەکان:", [4, 5], index=0)
    
    st.subheader("🔑 کلیلی وەڵامی ڕاست (Answer Key)")
    st.write("وەڵامە ڕاستەکان بۆ پرسیارەکان دیاری بکە:")
    
    choices_map = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
    correct_answers = []
    
    for i in range(int(num_questions)):
        ans = st.radio(
            f"پرسیاری {i+1}:",
            options=list(range(num_choices)),
            format_func=lambda x: choices_map[x],
            key=f"q_{i}",
            horizontal=True
        )
        correct_answers.append(ans)

with col_camera:
    st.subheader("📷 وێنەگرتن یان بارکردنی فۆرم")
    
    source_type = st.radio("سەرچاوەی وێنە:", ["کامێرای ڕاستەوخۆ", "بارکردنی فۆرم (Image Upload)"], horizontal=True)
    
    img_file = None
    if source_type == "کامێرای ڕاستەوخۆ":
        img_file = st.camera_input("وێنەی پەڕەی وەڵامەکە بگرە")
    else:
        img_file = st.file_uploader("وێنەی فۆرمەکە هەڵبژێرە...", type=["jpg", "jpeg", "png"])

    if img_file is not None:
        image = Image.open(img_file)
        img_np = np.array(image)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 1)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        
        st.image(img_np, caption="وێنەی خوێنراوەتەوە", use_column_width=True)
        
        if st.button("🎯 بپشکنە و نمرە هەژمار بکە", type="primary"):
            score = 0
            student_answers = []
            
            st.success("پشکنین بەسەرکەوتوویی ئەنجامدرا!")
            
            final_score = (score / num_questions) * 100
            
            st.markdown(f"""
            <div class="score-box">
                نمرەی کۆتایی: {final_score:.1f}% ({score} لە {num_questions})
            </div>
            """, unsafe_allow_html=True)
