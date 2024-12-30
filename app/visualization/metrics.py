import streamlit as st
import pandas as pd
import plotly.express as px

class MetricsVisualizer:
    @staticmethod
    def display_key_metrics(df: pd.DataFrame):
        """Display key metrics in columns."""
        cols = st.columns(5)
        
        metrics = {
            "Total Visits": len(df),
            "Unique Pages": len(df["page_visited"].unique()),
            "Countries": len(df["country_name"].unique()),
            "EU Traffic": f"{(len(df[df.get('is_eu', False)])/len(df))*100:.1f}%",
            "Connection Types": len(df["connection_type"].unique())
        }
        
        for col, (label, value) in zip(cols, metrics.items()):
            with col:
                st.metric(label, value)

    @staticmethod
    def display_business_metrics(df: pd.DataFrame):
        """Display business intelligence metrics in a clean, organized layout."""
        st.subheader("📊 Business Intelligence Metrics")
        
        # Create three columns for metrics
        metric_cols = st.columns(3)
        
        # 1. Page Visits Analysis
        with metric_cols[0]:
            page_counts = df["page_visited"].value_counts()
            st.metric(
                label="Most Popular Page",
                value=str(page_counts.index[0]),
                delta=f"{int(page_counts.iloc[0])} visits"
            )
        
        # 2. Country Analysis
        with metric_cols[1]:
            country_counts = df["country_name"].value_counts()
            st.metric(
                label="Top Traffic Country",
                value=str(country_counts.index[0]),
                delta=f"{int(country_counts.iloc[0])} visits"
            )
        
        # 3. Connection Type Analysis
        with metric_cols[2]:
            conn_counts = df["connection_type"].value_counts()
            st.metric(
                label="Primary Connection Type",
                value=str(conn_counts.index[0]),
                delta=f"{int(conn_counts.iloc[0])} connections"
            )
        
        # Create three columns for charts
        chart_cols = st.columns(3)
        
        # 1. Page Visits Chart
        with chart_cols[0]:
            fig_page = px.pie(
                values=page_counts.values[:5],
                names=page_counts.index[:5],
                title="Most Popular Pages",
                hole=0.3
            )
            fig_page.update_layout(
                height=400,
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_page, use_container_width=True)
        
        # 2. Country Traffic Chart
        with chart_cols[1]:
            fig_country = px.bar(
                x=country_counts.values[:5],
                y=country_counts.index[:5],
                title="Country Traffic Distribution",
                orientation="h",
                labels={"x": "Visits", "y": "Country"}
            )
            fig_country.update_layout(
                showlegend=False,
                height=400,
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_country, use_container_width=True)
        
        # 3. Connection Type Chart
        with chart_cols[2]:
            fig_conn = px.bar(
                 x=conn_counts.values,
                 y=conn_counts.index,
                 title="Connection Type Distribution",
                 orientation="h",
                 labels={"x": "Number of Connections", "y": "Connection Type"}
        )
            fig_conn.update_layout(
                showlegend=False,
                height=400,
                margin=dict(l=10, r=10, t=30, b=10),
                xaxis_title="Number of Connections",
                bargap=0.2
            )
            st.plotly_chart(fig_conn, use_container_width=True)
        
    @staticmethod
    def display_raw_data(df):
        """Display raw dataframe with pagination."""
        st.subheader("📋 Raw Data")

    

        page_size = st.number_input("Rows per page", min_value=5, max_value=50, value=10)
        total_pages = len(df) // page_size + (1 if len(df) % page_size > 0 else 0)
        
        if total_pages > 0:
            page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
            start_idx = (page - 1) * page_size
            end_idx = min(start_idx + page_size, len(df))
            st.dataframe(df.iloc[start_idx:end_idx])
            st.caption(f"Showing {start_idx + 1}-{end_idx} of {len(df)} rows")
        else:
            st.info("No data to display")