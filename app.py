import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="HBS Risk Calculator | Hungry Bone Syndrome Predictor",
    page_icon="🦴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    .gradient-text {
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: bold;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .risk-intermediate {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .footer {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 3rem;
        color: white;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.markdown("## 📊 Navigation")
page = st.sidebar.selectbox(
    "Choose a section:",
    ["🏠 Calculator", "📈 About the Model", "📚 Clinical Guidelines", "🔬 Research Background"],
    index=0
)

# Sidebar info
st.sidebar.markdown("## ℹ️ Quick Info")
st.sidebar.markdown("**Model Performance:**")
st.sidebar.markdown("• AUC: 0.742")
st.sidebar.markdown("• Excellent Calibration")
st.sidebar.markdown("• Validated on 227 patients")
st.sidebar.markdown("• 49.8% HBS incidence")

st.sidebar.markdown("## 🎯 Risk Categories")
st.sidebar.markdown("• **Low Risk (<30%)**: Standard monitoring")
st.sidebar.markdown("• **Intermediate (30-70%)**: Enhanced monitoring")
st.sidebar.markdown("• **High Risk (>70%)**: Intensive care")

# Main content based on navigation
if page == "🏠 Calculator":
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🦴 HBS Risk Calculator</h1>
        <p>Hungry Bone Syndrome Prediction Tool for Post-Parathyroidectomy Patients</p>
        <p><em>Evidence-Based Risk Assessment • Validated Clinical Model • Personalized Care</em></p>
    </div>
    """, unsafe_allow_html=True)

    # Input section
    st.markdown("## 📝 Patient Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👤 Demographics")
        age = st.slider(
            "Age (years)",
            min_value=18,
            max_value=85,
            value=55,
            help="Patient age in years"
        )
        
        st.markdown("### 🧪 Laboratory Values")
        phosphate = st.slider(
            "Phosphate at 1 month (mmol/L)",
            min_value=0.50,
            max_value=4.00,
            value=2.00,
            step=0.01,
            help="Serum phosphate level at 1 month post-surgery"
        )
    
    with col2:
        st.markdown("### 🔬 Biochemical Markers")
        alp = st.slider(
            "Alkaline Phosphatase at 1 month (U/L)",
            min_value=50,
            max_value=1500,
            value=300,
            help="Serum alkaline phosphatase at 1 month post-surgery"
        )
        
        pth = st.slider(
            "PTH at 3 months (pmol/L)",
            min_value=15,
            max_value=600,
            value=150,
            help="Parathyroid hormone level at 3 months post-surgery"
        )

    # Calculate button
    if st.button("🔮 Calculate HBS Risk", key="calculate"):
        # HBS prediction model
        # logit(p) = -2.7425363 + (-0.01346972)*Age + 1.4125066*Phos_1 + 0.00250891*ALP_1 + 0.00236971*PTH_3
        
        logit_p = (-2.7425363 + 
                   (-0.01346972) * age + 
                   1.4125066 * phosphate + 
                   0.00250891 * alp + 
                   0.00236971 * pth)
        
        probability = 1 / (1 + np.exp(-logit_p))
        probability_percent = probability * 100
        
        # Risk categorization
        if probability_percent < 30:
            risk_category = "Low Risk"
            risk_color = "risk-low"
            risk_emoji = "🟢"
            recommendations = [
                "⚠️ Standard postoperative monitoring",
                "⚠️ Regular calcium and vitamin D supplementation", 
                "⚠️ Outpatient follow-up at 1-2 weeks",
                "⚠️ Early discharge planning appropriate",
                "⚠️ Patient education on hypocalcemia symptoms"
            ]
        elif probability_percent < 70:
            risk_category = "Intermediate Risk"
            risk_color = "risk-intermediate"
            risk_emoji = "🟡"
            recommendations = [
                "⚠️ Enhanced postoperative monitoring",
                "⚠️ Proactive calcium supplementation",
                "⚠️ Consider prolonged observation (24-48 hours)",
                "⚠️ Frequent biochemical monitoring",
                "⚠️ Close outpatient follow-up"
            ]
        else:
            risk_category = "High Risk"
            risk_color = "risk-high"
            risk_emoji = "🔴"
            recommendations = [
                "🚨 Intensive postoperative monitoring",
                "🚨 Prophylactic high-dose calcium/calcitriol",
                "🚨 Consider ICU-level monitoring",
                "🚨 Extended hospitalization",
                "🚨 Immediate intervention protocols ready"
            ]

        # Results section
        st.markdown("## 🎯 Risk Assessment Results")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Main probability display
            st.markdown(f"""
            <div class="metric-card">
                <h2>HBS Probability</h2>
                <h1 style="font-size: 4rem; margin: 1rem 0;">{probability_percent:.1f}%</h1>
                <p>Risk of developing Hungry Bone Syndrome</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Risk category
            st.markdown(f"""
            <div class="{risk_color}">
                <h3>{risk_emoji} {risk_category}</h3>
                <p><strong>Probability: {probability_percent:.1f}%</strong></p>
            </div>
            """, unsafe_allow_html=True)

        # Clinical recommendations
        st.markdown("## 📋 Clinical Recommendations")
        for rec in recommendations:
            st.markdown(f"• {rec}")

        # Risk visualization
        st.markdown("## 📊 Risk Visualization")
        
        # Gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=probability_percent,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "HBS Risk Probability (%)"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Risk comparison chart
        st.markdown("## 📈 Risk Comparison")
        
        # Sample data for comparison (based on study population)
        risk_data = {
            'Risk Category': ['Low Risk (<30%)', 'Intermediate Risk (30-70%)', 'High Risk (>70%)'],
            'Observed HBS Rate (%)': [23.8, 50.0, 93.3],
            'Your Risk': [probability_percent if probability_percent < 30 else 0,
                         probability_percent if 30 <= probability_percent < 70 else 0,
                         probability_percent if probability_percent >= 70 else 0]
        }
        
        fig_comparison = px.bar(
            x=risk_data['Risk Category'],
            y=risk_data['Observed HBS Rate (%)'],
            title="Risk Category Comparison",
            labels={'x': 'Risk Categories', 'y': 'HBS Probability (%)'},
            color=risk_data['Risk Category'],
            color_discrete_map={
                'Low Risk (<30%)': 'lightgreen',
                'Intermediate Risk (30-70%)': 'orange', 
                'High Risk (>70%)': 'red'
            }
        )
        
        # Add patient's risk as scatter points
        for i, risk in enumerate(risk_data['Your Risk']):
            if risk > 0:
                fig_comparison.add_scatter(
                    x=[risk_data['Risk Category'][i]],
                    y=[risk],
                    mode='markers',
                    marker=dict(size=15, color='blue', symbol='diamond'),
                    name='Your Risk'
                )
        
        fig_comparison.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig_comparison, use_container_width=True)

elif page == "📈 About the Model":
    st.markdown("# 📈 Model Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## 🎯 Model Performance")
        st.markdown("• **Discrimination (AUC)**: 0.742 (optimism-corrected)")
        st.markdown("• **Calibration**: Excellent")
        st.markdown("• **Clinical Utility**: Demonstrated across threshold probabilities 0.1-0.8")
        st.markdown("• **Validation**: 500 bootstrap iterations")
        
        st.markdown("## 📊 Model Formula")
        st.code("""
logit(p) = -2.7425363 + 
           (-0.01346972) × Age + 
           1.4125066 × Phosphate_1month + 
           0.00250891 × ALP_1month + 
           0.00236971 × PTH_3months

Probability = 1 / (1 + exp(-logit(p)))
        """)
    
    with col2:
        st.markdown("## 🔬 Predictor Variables and Their Effects")
        
        # Create a simple bar chart showing predictor effects
        predictors = ['Age', 'Phosphate', 'ALP', 'PTH at 3 months']
        coefficients = [-0.01346972, 1.4125066, 0.00250891, 0.00236971]
        colors = ['blue' if c < 0 else 'red' if c > 1 else 'orange' for c in coefficients]
        
        fig_predictors = px.bar(
            x=predictors,
            y=coefficients,
            title="Predictor Variables and Their Effects",
            labels={'x': 'Variable', 'y': 'Coefficient'},
            color=colors
        )
        fig_predictors.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_predictors, use_container_width=True)

elif page == "📚 Clinical Guidelines":
    st.markdown("# 📚 Clinical Management Guidelines")
    
    st.markdown("## 🟢 Low Risk (<30% probability)")
    st.markdown("""
    **Clinical Recommendations:**
    - ✅ Standard postoperative monitoring
    - ✅ Regular calcium and vitamin D supplementation
    - ✅ Outpatient follow-up at 1-2 weeks
    - ✅ Early discharge planning appropriate
    - ✅ Patient education on hypocalcemia symptoms
    
    **Monitoring Protocol:**
    - Serum calcium q8h for first 24 hours
    - Daily calcium levels until stable
    - Standard supplementation: Calcium carbonate 1-2g TID, Calcitriol 0.25-0.5 mcg BID
    """)
    
    st.markdown("## 🟡 Intermediate Risk (30-70% probability)")
    st.markdown("""
    **Clinical Recommendations:**
    - ⚠️ Enhanced postoperative monitoring
    - ⚠️ Proactive calcium supplementation
    - ⚠️ Consider prolonged observation (24-48 hours)
    - ⚠️ Frequent biochemical monitoring
    - ⚠️ Close outpatient follow-up
    
    **Monitoring Protocol:**
    - Serum calcium q6h for first 48 hours
    - Consider ionized calcium monitoring
    - Enhanced supplementation: Calcium carbonate 2-3g TID, Calcitriol 0.5-1.0 mcg BID
    """)
    
    st.markdown("## 🔴 High Risk (>70% probability)")
    st.markdown("""
    **Clinical Recommendations:**
    - 🚨 Intensive postoperative monitoring
    - 🚨 Prophylactic high-dose calcium/calcitriol
    - 🚨 Consider ICU-level monitoring
    - 🚨 Extended hospitalization
    - 🚨 Immediate intervention protocols ready
    
    **Monitoring Protocol:**
    - Continuous cardiac monitoring
    - Serum calcium q4-6h
    - Prophylactic treatment: High-dose calcium carbonate 3-4g TID, Calcitriol 1.0-2.0 mcg BID
    """)

elif page == "🔬 Research Background":
    st.markdown("# 🔬 Research Background")
    
    st.markdown("## 🦴 What is Hungry Bone Syndrome?")
    st.markdown("""
    Hungry Bone Syndrome (HBS) is a serious complication following parathyroidectomy, characterized by:
    - Severe, prolonged hypocalcemia
    - Hypophosphatemia
    - Hypomagnesemia
    - Increased bone mineral uptake
    - Potential for life-threatening complications
    """)
    
    st.markdown("## 📊 Study Population")
    st.markdown("""
    - **Total Patients**: 227 (from 251 screened)
    - **HBS Cases**: 113 (49.8% incidence)
    - **Mean Age**: 52.7 ± 14.2 years
    - **Gender**: 56.4% male
    - **Comorbidities**: 42.7% diabetes, 81.1% hypertension
    """)
    
    st.markdown("## 🔬 Model Development")
    st.markdown("""
    - **Variable Selection**: LASSO regularization
    - **Internal Validation**: 500 bootstrap iterations
    - **Performance Assessment**: Discrimination, calibration, clinical utility
    - **Risk Stratification**: Three clinically meaningful categories
    """)

# Footer
st.markdown("""
<div class="footer">
    <h3>🏥 HBS Risk Calculator</h3>
    <p>Developed for clinical research and educational purposes</p>
    <p><em>Always consult with healthcare professionals for clinical decisions</em></p>
    <p>© 2024 | Evidence-Based Medicine | Validated Clinical Tool</p>
</div>
""", unsafe_allow_html=True)
