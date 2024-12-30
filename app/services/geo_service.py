import requests
import time
from typing import Dict, Optional
import streamlit as st
from app.config.settings import settings  

class Geoservice:
    def __init__(self,api_key: str):
        self.api_key = api_key
    
    def fetch_geo_data(self, ip: str) -> Optional[Dict]:
        """Fetch geolocation data for an IP address."""
        try:
            url = f"{settings.IPSTACK_API_URL}/{ip}?access_key={self.api_key}"
            response = requests.get(url, timeout=settings.REQUEST_TIMEOUT)
            
            if response.status_code == 429:  # Too Many Requests
                time.sleep(settings.RETRY_DELAY)
                return self.fetch_geo_data(ip)
            
            if response.status_code == 200:
                return response.json()
            
            st.error(f"Error fetching data for IP {ip}: {response.status_code}")
            return None
            
        except requests.exceptions.RequestException as e:
            st.error(f"Network error for IP {ip}: {str(e)}")
            return None
    
