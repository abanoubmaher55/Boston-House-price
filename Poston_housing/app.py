import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Valuer.ai | Boston Real Estate Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: #070b14 !important;
        color: #f8fafc !important;
    }

    
    header[data-testid="stHeader"], #MainMenu, footer {
        display: none !important;
        visibility: hidden !important;
    }

    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #f8fafc !important;
    }

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
        font-size: 1.05rem;
        color: #94a3b8 !important;
        margin-bottom: 1.8rem;
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

    div[data-baseweb="input"], [data-testid="stNumberInput"] div[data-baseweb="input"] {
        background-color: #0f172a !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        border-radius: 12px !important;
    }
    div[data-baseweb="input"] input {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    div[data-baseweb="input"] button {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: none !important;
    }
    

    div[data-testid="stColumn"] button {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #cbd5e1 !important;
        font-size: 0.8rem !important;
        padding: 8px !important;
        border-radius: 10px !important;
    }
    div[data-testid="stColumn"] button:hover {
        border-color: #38bdf8 !important;
        color: #ffffff !important;
        background: rgba(56, 189, 248, 0.15) !important;
    }

    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 14px 20px !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.35) !important;
        transition: all 0.3s ease !important;
    }

    
    .result-card {
        background: linear-gradient(165deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 24px;
        padding: 28px;
        text-align: center;
        backdrop-filter: blur(20px);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
    }
    .price-display {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
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
    </style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model():
  return joblib.load("boston_housing_model.pkl")


model = load_model()


if "rm" not in st.session_state:
  st.session_state.rm = 6.0
if "lstat" not in st.session_state:
  st.session_state.lstat = 12.5
if "ptratio" not in st.session_state:
  st.session_state.ptratio = 18.0


def apply_preset(rm_val, lstat_val, ptratio_val):
  st.session_state.rm = rm_val
  st.session_state.lstat = lstat_val
  st.session_state.ptratio = ptratio_val


st.markdown(
    '<div class="hero-title">A smarter way to see home value.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-subtitle">Enter property characteristics to generate an'
    " AI-driven valuation powered by Decision Tree Regression.</div>",
    unsafe_allow_html=True,
)


col_input, col_output = st.columns([1.1, 0.9], gap="large")


with col_input:
  st.markdown(
      '<div class="badge">Property Specs</div>', unsafe_allow_html=True
  )

  
  st.caption("⚡ QUICK DEMO SCENARIOS")
  p_col1, p_col2, p_col3 = st.columns(3)
  with p_col1:
    st.button(
        "🏢 Client 1 (Standard)",
        on_click=apply_preset,
        args=(5.0, 17.0, 15.0),
        use_container_width=True,
    )
  with p_col2:
    st.button(
        "🏚️ Client 2 (Budget)",
        on_click=apply_preset,
        args=(4.0, 55.0, 22.0),
        use_container_width=True,
    )
  with p_col3:
    st.button(
        "🏰 Client 3 (Luxury)",
        on_click=apply_preset,
        args=(8.0, 7.0, 12.0),
        use_container_width=True,
    )

  st.write("")

  
  rm = st.number_input(
      "01 Average Rooms (RM)",
      min_value=1.0,
      max_value=50.0,
      key="rm",
      step=0.1,
      help="Average number of rooms per dwelling",
  )

  lstat = st.number_input(
      "02 Neighborhood Lower-Status % (LSTAT)",
      min_value=0.0,
      max_value=100.0,
      key="lstat",
      step=0.1,
      help="Percentage of lower-status population",
  )

  ptratio = st.number_input(
      "03 Pupil-Teacher Ratio (PTRATIO)",
      min_value=1.0,
      max_value=100.0,
      key="ptratio",
      step=0.5,
      help="Pupil-teacher ratio in town schools",
  )

  st.write("")
  predict_btn = st.button("Calculate Estimated Value ✨")


with col_output:
  st.markdown(
      '<div class="badge">Valuation Output & Analytics</div>',
      unsafe_allow_html=True,
  )

  if predict_btn:
    features = pd.DataFrame(
        [[rm, lstat, ptratio]], columns=["RM", "LSTAT", "PTRATIO"]
    )
    predicted_price = model.predict(features)[0]

    if predicted_price >= 600000:
      segment = "Luxury Segment 🌟"
    elif predicted_price >= 350000:
      segment = "Mid-Tier Suburban 🏡"
    else:
      segment = "Affordable Entry 🏢"

    
    st.markdown(
        f"""
        <div class="result-card">
            <div style="font-size: 0.85rem; color: #94a3b8; font-weight: 600; letter-spacing: 1px;">ESTIMATED MARKET VALUE</div>
            <div class="price-display">${predicted_price:,.2f}</div>
            <div style="margin-bottom: 15px;">
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

    
    st.markdown(
        """
        <div style="text-align: center; color: #94a3b8; font-size: 0.8rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 20px; margin-bottom: 8px;">
            MARKET RANGE POSITION
        </div>
        """,
        unsafe_allow_html=True,
    )

   
    gauge_max = max(1000000, float(predicted_price) * 1.1)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=predicted_price,
            number={
                "prefix": "$",
                "valueformat": ",.0f",
                "font": {"color": "#ffffff", "size": 24},
            },
            gauge={
                "axis": {
                    "range": [100000, gauge_max],
                    "tickwidth": 1,
                    "tickcolor": "#94a3b8",
                },
                "bar": {"color": "#38bdf8"},
                "bgcolor": "rgba(15, 23, 42, 0.8)",
                "borderwidth": 1,
                "bordercolor": "rgba(255, 255, 255, 0.1)",
                "steps": [
                    {
                        "range": [100000, 350000],
                        "color": "rgba(239, 68, 68, 0.15)",
                    },
                    {
                        "range": [350000, 600000],
                        "color": "rgba(234, 179, 8, 0.15)",
                    },
                    {
                        "range": [600000, 1000000],
                        "color": "rgba(34, 197, 94, 0.15)",
                    },
                ],
            },
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#f8fafc", "family": "Plus Jakarta Sans"},
        height=220,  
        margin=dict(
            l=30, r=30, t=35, b=10
        ),  
    )

    st.plotly_chart(
        fig, use_container_width=True, config={"displayModeBar": False}
    )

  else:
    st.markdown(
        """
        <div class="result-card">
            <div style="font-size: 0.85rem; color: #94a3b8; font-weight: 600; letter-spacing: 1px;">ESTIMATED MARKET VALUE</div>
            <div class="price-display" style="opacity: 0.3;">$ --,---.--</div>
            <div style="margin-bottom: 20px;">
                <span class="feature-chip">🛏️ Waiting for input</span>
            </div>
            <div style="font-size: 0.85rem; color: #94a3b8; font-weight: 400; background: rgba(255, 255, 255, 0.03); padding: 16px; border-radius: 12px; border: 1px dashed rgba(255, 255, 255, 0.1);">
                Adjust the property specs on the left or click a <b>Preset</b> button, then click <b>Calculate Estimated Value</b> to run the AI model.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )