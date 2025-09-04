from typing import Dict, Any

class Settings:
    app_name: str = "Rewards & Redemption Service"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Cache settings
    cache_ttl: int = 300  # 5 minutes
    
    # External service settings
    mock_external_services: bool = True
    external_service_delay: float = 0.1  # seconds
    
    # Event settings
    event_processing_delay: float = 0.05  # seconds
    
    def __init__(self):
        pass

settings = Settings()