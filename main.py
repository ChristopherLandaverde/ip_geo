# main.py
"""Main application file."""
import streamlit as st
from app.config import settings
from app.services import Geoservice,DataProcessor
from app.utils import validate_dataframe_columns
from app.visualization import MapVisualizer, ChartVisualizer, MetricsVisualizer
import pandas as pd

def initialize_session_state():
    """Initialize session state variables."""
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'map_created' not in st.session_state:
        st.session_state.map_created = False

def setup_sidebar():
    """Setup sidebar components."""
    with st.sidebar:
        st.header("📊 Data Controls")
        api_key = st.text_input("Enter your IPstack API key", type="password")
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        
        if st.session_state.processed_data is not None:
            st.markdown("### 🎯 Filters")
            selected_page = st.selectbox(
                "Filter by Page",
                ["All Pages (Default)"] + sorted(st.session_state.processed_data["page_visited"].unique())
            )
        
        process_button = st.button("Process Data")
        
        return api_key, uploaded_file, process_button

def process_data(api_key: str, uploaded_file):
    """Process uploaded data."""
    if not api_key or not uploaded_file:
        st.error("Please provide both API key and CSV file")
        return
        
    try:
        df = pd.read_csv(uploaded_file)
        if not validate_dataframe_columns(df.columns, settings.REQUIRED_COLUMNS):
            st.error("CSV must contain 'ip' and 'page_visited' columns")
            return
            
        with st.spinner("Processing data..."):
            geo_service = Geoservice(api_key)
            processor = DataProcessor(geo_service)
            st.session_state.processed_data = processor.process_ips(df)
            
            if len(st.session_state.processed_data) > 0:
                st.success(f"Successfully processed {len(st.session_state.processed_data)} IP addresses")
                st.session_state.map_created = True
            else:
                st.warning("No valid data was processed")
                st.session_state.map_created = False
                
    except Exception as e:
        st.error(f"Error: {str(e)}")

def main():
    """Main application entry point."""
    st.set_page_config(page_title=settings.PAGE_TITLE, layout="wide",page_icon="🌍",initial_sidebar_state="expanded")
    st.title("🌍 IP Analytics Dashboard")
    st.markdown("### 📊 Track and analyze visitor locations and page engagement")
    st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTab {
        font-size: 18px;
    }
    .stAlert {
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)
    
    initialize_session_state()
    api_key, uploaded_file, process_button = setup_sidebar()
    
    if process_button:
        process_data(api_key, uploaded_file)
    
    if st.session_state.processed_data is not None:
        df = st.session_state.processed_data
        MetricsVisualizer.display_key_metrics(df)
        
        # Create tabs
        tabs = st.tabs(["🗺️ Geographic View", "💡 Business Intelligence", 
                                 "📈 Page Analytics", "📋 Raw Data"])
        
        with tabs[0]:
            st.subheader("🗺️ Geographic Distribution")
            map_type = st.radio("Select Map Type", ["Marker Cluster", "Heatmap"], horizontal=True)
            if st.session_state.map_created:
                m = MapVisualizer.create_map(df, map_type.lower())
                if m:
                    st.components.v1.html(m._repr_html_(), height=600)
        
        with tabs[1]:
            MetricsVisualizer.display_business_metrics(df)
        
        with tabs[2]:
            st.subheader("📊 Page Analytics")
            charts = ChartVisualizer()
            st.plotly_chart(charts.create_page_visits_chart(df))
            st.plotly_chart(charts.create_geographic_distribution_chart(df))
            if conn_chart := charts.create_connection_type_chart(df):
                st.plotly_chart(conn_chart)
        
        with tabs[3]:
            MetricsVisualizer.display_raw_data(df)

if __name__ == "__main__":
    main()