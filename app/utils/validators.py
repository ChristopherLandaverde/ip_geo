import ipaddress
from typing import List

def is_valid_ip(ip:str) -> bool:
    """Validate an IP address"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
def validate_dataframe_columns(columns:List[str], required_columns:List[str]) -> bool:
    """Validate that a dataframe has the required columns"""
    return all(column in columns for column in required_columns)