import streamlit as st
from scorer import RubricScorer

# Page Config
st.set_page_config(
    page_title="Nirmaan AI Communication Coach", 
    page_icon="🎙️",
    layout="wide"
)

# --- SIDEBAR (Developer Info) ---
with st.sidebar:
    st.header("About")
    st.markdown("This AI tool analyzes spoken communication skills using NLP and semantic search.")
    st.divider()
    st.markdown("**Created by:**")
    st.markdown("### P. Venkata Srinag") # <--- YOUR NAME HERE
    st.caption("Nirmaan AI Intern Case Study")

# --- MAIN HEADER ---
st.title("🎙️ Nirmaan AI Communication Coach")
st.markdown("Analyze your spoken communication skills based on the official rubric.")
st.markdown("---")

# Initialize Scorer (Cached to prevent reloading models on every click)
@st.cache_resource
def load_scorer():
    return RubricScorer()

scorer = load_scorer()

# --- INPUT SECTION ---
col1, col2 = st.columns([2, 1])

with col1:
    transcript = st.text_area(
        "Paste Transcript Here:", 
        height=300, 
        placeholder="Hello everyone, myself Muskan..."
    )

with col2:
    duration = st.number_input(
        "Audio Duration (seconds):", 
        min_value=10, 
        value=52, 
        help="Required to calculate Words Per Minute (WPM)"
    )
    
    analyze_btn = st.button("Analyze Score 🚀", type="primary", use_container_width=True)
    
    if analyze_btn:
        if not transcript:
            st.error("Please enter a transcript.")
        else:
            with st.spinner("Analyzing semantic meaning, grammar, and sentiment..."):
                # --- CALL THE BACKEND ---
                results = scorer.analyze_transcript(transcript, duration)
                
                # --- DISPLAY RESULTS ---
                st.balloons() # precise visual reward
                st.success("Analysis Complete!")
                
                # Overall Score
                st.markdown(f"""
                <div style="text-align: center; border: 2px solid #4CAF50; padding: 10px; border-radius: 10px; margin-bottom: 20px;">
                    <h2 style="margin:0; color: #4CAF50;">Overall Score</h2>
                    <h1 style="margin:0; font-size: 3rem;">{results['overall_score']} / 100</h1>
                </div>
                """, unsafe_allow_html=True)
                
                # Detailed Breakdown
                st.subheader("Detailed Criterion Scores")
                
                # Create 5 columns for the metrics
                cols = st.columns(5)
                metrics = results["details"]
                
                keys = list(metrics.keys())
                for i, col in enumerate(cols):
                    criterion = keys[i]
                    data = metrics[criterion]
                    
                    # Color coding logic for visual feedback
                    color = "normal"
                    if data["score"] < 5: color = "off"
                    
                    col.metric(label=criterion, value=data["score"], delta_color=color)
                    col.caption(f"📝 {data['feedback']}")

                # Raw JSON
                with st.expander("View Raw Scoring Data (Debug)"):
                    st.json(results)

# Footer
st.markdown("---")
st.caption("Developed by **P. Venkata Srinag** for Nirmaan AI Intern Case Study")