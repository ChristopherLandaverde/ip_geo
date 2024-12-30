import plotly.express as px
import streamlit as st

class ChartVisualizer:
    @staticmethod
    def create_page_visits_chart(df):
        """Create page visits distribution chart."""
        page_visits = df['page_visited'].value_counts()
        fig = px.bar(
            x=page_visits.index, 
            y=page_visits.values,
            title='Page Visits Distribution',
            labels={'x': 'Page', 'y': 'Number of Visits'}
        )
        return fig

    @staticmethod
    def create_geographic_distribution_chart(df):
        """Create geographic distribution chart."""
        geo_dist = df.groupby('country_name').size().reset_index(name='visits')
        fig = px.choropleth(
            geo_dist,
            locations='country_name',
            locationmode='country names',
            color='visits',
            title='Geographic Distribution of Visits',
            color_continuous_scale='Viridis'
        )
        return fig

    @staticmethod
    def create_connection_type_chart(df):
        """Create connection type distribution chart."""
        if 'connection_type' in df.columns:
            conn_dist = df['connection_type'].value_counts()
            fig = px.pie(
                values=conn_dist.values,
                names=conn_dist.index,
                title='Connection Type Distribution'
            )
            return fig
        return None
