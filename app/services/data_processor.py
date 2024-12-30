import pandas as pd
import streamlit as st
from typing import List, Dict
from app.utils.validators import is_valid_ip
from app.services.geo_service import Geoservice

class DataProcessor:
    def __init__(self,geo_service:Geoservice):
        self.geo_service=geo_service
    
    def process_ips(self,df:pd.DataFrame) -> pd.DataFrame:
        """Process IP addresses and enrich with geolocation data."""
        ip_data = []
        progress_bar = st.progress(0)
        status_text=st.empty()

        unique_ips=df['ip'].unique()
        valid_ips=[ip for ip in unique_ips if is_valid_ip(ip)]

        for idx,ip in enumerate(valid_ips):
            status_text.text(f"Processing IP {idx + 1}/{len(valid_ips)}: {ip}")
            data=self.geo_service.fetch_geo_data(ip)

            if data:
                self._process_ip_data(data,ip,df,ip_data)
            progress= float((idx+1)/len(valid_ips))
            progress_bar.progress(progress)
        
        progress_bar.empty()
        status_text.empty()
        return pd.DataFrame(ip_data)
    
    def _process_ip_data(self,data:Dict,ip:str,df:pd.DataFrame,ip_data:List):
        """ Helper Method to process individual IP data."""
        pages_for_ip = df[df['ip'] == ip]["page_visited"].tolist()

        for page in pages_for_ip:
            ip_info = {
                "ip": ip,
                "page_visited": page,
                "country_name": data.get("country_name"),
                "city": data.get("city"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "connection_type": data.get("connection_type"),
                "is_eu": data.get("location", {}).get("is_eu")
            }
            ip_data.append(ip_info)


    
