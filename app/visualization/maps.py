import folium
from folium.plugins import MarkerCluster, HeatMap
import streamlit as st
from typing import Optional
from app.config.settings import settings
import pandas as pd


class MapVisualizer:
    @staticmethod
    def create_map(df, map_type: str = "markers") -> Optional[folium.Map]:
        """Create a Folium map with either markers or heatmap."""
        try:
            df_clean = df.copy()
            df_clean = df_clean[
            df_clean['latitude'].astype(str).str.match(r'-?\d+\.?\d*') &
            df_clean['longitude'].astype(str).str.match(r'-?\d+\.?\d*')
        ]
            df_clean['latitude'] = pd.to_numeric(df_clean['latitude'], errors='coerce')
            df_clean['longitude'] = pd.to_numeric(df_clean['longitude'], errors='coerce')
            df_clean = df_clean.dropna(subset=['latitude', 'longitude'])
           
            
            if len(df_clean) == 0:
                st.warning("Not vdalid coordinates found in the data")
                return None
                
            center_lat = float(df_clean['latitude'].mean())
            center_lon = float(df_clean['longitude'].mean())
            
            m = folium.Map(
                location=[center_lat, center_lon], 
                zoom_start=settings.MAP_DEFAULT_ZOOM
            )
            
            if map_type == "markers":
                MapVisualizer._add_markers(m, df_clean)
            else:
                MapVisualizer._add_heatmap(m, df_clean)
            
            return m
            
        except Exception as e:
            st.error(f"Error creating map: {str(e)}")
            return None
    @staticmethod
    def _add_markers(m: folium.Map, df_clean: pd.DataFrame):
        """Add marker cluster to the map."""
        mc = MarkerCluster(name="cluster")
        mc.add_to(m)
        
        for _, row in df_clean.iterrows():
            popup_html = f"""
                <b>IP:</b> {str(row['ip'])}<br>
                <b>Page:</b> {str(row['page_visited'])}<br>
                <b>Location:</b> {str(row['city'])}, {str(row['country_name'])}<br>
                <b>Connection:</b> {str(row['connection_type'])}
            """
            
            folium.Marker(
                location=[float(row['latitude']), float(row['longitude'])],
                popup=folium.Popup(popup_html, max_width=500)
            ).add_to(mc)

    @staticmethod
    def _add_heatmap(m: folium.Map, df_clean: pd.DataFrame):
        """Add heatmap layer to the map."""
        heat_data = [[float(row['latitude']), float(row['longitude'])] 
                    for _, row in df_clean.iterrows()]
        HeatMap(heat_data).add_to(m)
