from dataclasses import  dataclass,field
from typing import List

@dataclass
class Settings:
    PAGE_TITLE: str = "IP Geolocation & Page Analytics"
    IPSTACK_API_URL: str = "http://api.ipstack.com/"
    REQUIRED_COLUMNS: List[str] = field(default_factory=lambda:["ip","page_visited"])
    REQUEST_TIMEOUT: int = 10
    MAP_DEFAULT_ZOOM: int = 2
    RETRY_DELAY: int=1

settings = Settings()
