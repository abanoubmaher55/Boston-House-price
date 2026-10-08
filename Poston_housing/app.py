import joblib
import numpy as np
import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="Valuer.ai | Boston Real Estate Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. نظام التنسيق الزجاجي الشامل (Glassmorphism CSS Isolation)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* توحيد الخط والخلفية العميقة لجميع الأوضاع */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: #070b14 !important;
        color: #f8fafc !important;
    }
    
    [data-testid="stHeader"] {
        background: rgba(7, 11, 20, 0.8) !important;
        backdrop-filter: blur(12px);
    }

    /* إصلاح ألوان النصوص والعناوين تماماً لجميع الأوضاع */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #f8fafc !important;
    }

    .stCaption, [data-testid="stCaptionContainer"] p {
        color: #94a3b8 !important;
    }

    /* خلفية هيدر الصفحة بتأثير التدرج الجذاب */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #38bdf8 50%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8 !important;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* تصميم بطاقات الإدخال الزجاجية */
    .input-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px;
        backdrop-filter: blur(16px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }

    /* إعادة تنسيق حقول الإدخال */
    .stNumberInput div[data-baseweb="input"] {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        transition: all 0.3s ease;
    }
    
    .stNumberInput div[data-baseweb="input"]:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.25) !important;
    }

    /* تصميم زر الحساب النيون */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 16px 24px !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.35) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.5px;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(56, 189, 248, 0.5) !important;
        background: linear-gradient(135deg, #0369a1 0%, #4338ca 100%) !important;
    }

    /* تصميم بطاقة النتيجة البارزة (Hero Output Glass Card) */
    .result-card {
        background: linear-gradient(165deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 24px;
        padding: 36px;
        text-align: center;
        backdrop-filter: blur(20px);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
        position: relative;
        overflow: hidden;
    }

    .result-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.08) 0%, transparent 60%);
        pointer-events: none;
    }

    .badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        background: rgba(56, 189, 248, 0.1);
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.25);
        margin-bottom: 16px;
    }

    .price-display {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 12px 0;
        letter-spacing: -1.5px;
    }

    .feature-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.05);
        padding: 8px 14px;
        border-radius: 10px;
        font-size: 0.85rem;
        color: #cbd5e1 !important;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin: 4px;
    }

        /* إخفاء الهيدر والقائمة العلوية بالكامل لمنع التغيير للوضع النهاري */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    #MainMenu {
        visibility: hidden !important;
    }

    footer {
        visibility: hidden !important;
    }

    
        /* إجبار حقول الإدخال على المظهر المظلم دائماً مهما كان وضع المتصفح */
    div[data-baseweb="input"] {
        background-color: #0f172a !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="input"] input {
        background-color: transparent !important;
        color: #ffffff !important;
    }

    /* تعديل خلفية أزرار الزيادة والنقصان (+ و -) داخل الحقول */
    div[data-baseweb="input"] button {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: none !important;
    }

    div[data-baseweb="input"] button:hover {
        background-color: #38bdf8 !important;
        color: #070b14 !important;
    }


    </style>
""",
    unsafe_allow_html=True,
)


# 3. تحميل النموذج
@st.cache_resource
def load_model():
  return joblib.load("boston_housing_model.pkl")


model = load_model()

# 4. رأس الصفحة (Hero Header)
st.markdown(
    '<div class="hero-title">A smarter way to see home value.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-subtitle">Enter property characteristics to generate an'
    " AI-driven valuation powered by Decision Tree Regression.</div>",
    unsafe_allow_html=True,
)

# 5. التنسيق في عمودين متوازيين
col_input, col_output = st.columns([1.1, 0.9], gap="large")

with col_input:
  st.markdown(
      '<div class="badge">Property Specs</div>', unsafe_allow_html=True
  )

  # حقل عدد الغرف
  rm = st.number_input(
      "01 Average Rooms (RM)",
      min_value=1.0,
      max_value=50.0,
      value=6.0,
      step=0.1,
      help="Average number of rooms per dwelling",
  )

  # حقل نسبة الفقر
  lstat = st.number_input(
      "02 Neighborhood Lower-Status % (LSTAT)",
      min_value=0.0,
      max_value=100.0,
      value=12.5,
      step=0.1,
      help="Percentage of homeowners considered lower status",
  )

  # حقل نسبة الطلاب للمعلمين
  ptratio = st.number_input(
      "03 Pupil-Teacher Ratio (PTRATIO)",
      min_value=1.0,
      max_value=100.0,
      value=18.0,
      step=0.5,
      help="Pupil-teacher ratio by town schools",
  )

  st.write("")
  predict_btn = st.button("Calculate Estimated Value ✨")

with col_output:
  st.markdown('<div class="badge">Valuation Output</div>', unsafe_allow_html=True)

  # 1. تنفيذ التنبؤ فقط عند الضغط على الزر
  if predict_btn:
    # استخدام DataFrame لتفادي تحذيرات التيرمينال
    features = pd.DataFrame(
        [[rm, lstat, ptratio]], columns=['RM', 'LSTAT', 'PTRATIO']
    )
    predicted_price = model.predict(features)[0]

    # تحديد التصنيف بناءً على السعر المحسوب
    if predicted_price >= 500000:
      segment = 'Luxury Segment 🌟'
    elif predicted_price >= 300000:
      segment = 'Mid-Tier Suburban 🏡'
    else:
      segment = 'Affordable Entry 🏢'

    # عرض كارت النتيجة النهائي
    st.markdown(
        f"""
        <div class="result-card">
            <div style="font-size: 0.85rem; color: #94a3b8; font-weight: 600; letter-spacing: 1px;">ESTIMATED MARKET VALUE</div>
            <div class="price-display">${predicted_price:,.2f}</div>
            <div style="margin-bottom: 20px;">
                <span class="feature-chip">🛏️ {rm:.1f} Rooms</span>
                <span class="feature-chip">📊 {lstat:.1f}% LSTAT</span>
                <span class="feature-chip">🎓 {ptratio:.1f} PTRATIO</span>
            </div>
            <div style="font-size: 0.9rem; color: #38bdf8; font-weight: 600; background: rgba(56, 189, 248, 0.1); padding: 10px; border-radius: 12px; border: 1px solid rgba(56, 189, 248, 0.2);">
                Category: {segment}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    # 2. الكارت الافتراضي قبل الضغط على الزر
    st.markdown(
        """
        <div class="result-card">
            <div style="font-size: 0.85rem; color: #94a3b8; font-weight: 600; letter-spacing: 1px;">ESTIMATED MARKET VALUE</div>
            <div class="price-display" style="opacity: 0.3;">$ --,---.--</div>
            <div style="margin-bottom: 20px;">
                <span class="feature-chip">🛏️ Waiting for input</span>
            </div>
            <div style="font-size: 0.85rem; color: #94a3b8; font-weight: 400; background: rgba(255, 255, 255, 0.03); padding: 12px; border-radius: 12px; border: 1px dashed rgba(255, 255, 255, 0.1);">
                Adjust the property specs on the left and click <b>Calculate Estimated Value</b> to run the prediction model.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )