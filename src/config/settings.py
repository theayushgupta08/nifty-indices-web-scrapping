"""
Application Settings
Configuration constants and settings
"""


class Settings:
    """Application configuration settings"""
    
    # API Settings
    API_BASE_URL = "https://www.niftyindices.com"
    API_TIMEOUT = 30
    
    # Default Values
    DEFAULT_INDEX_TYPES = ["Equity", "Fixed Income", "Multi Asset"]
    DEFAULT_INDEX_GROUP = "Historical Index Data"
    
    # Date Format
    DATE_FORMAT = "%d-%b-%Y"  # DD-MMM-YYYY
    DATE_FORMAT_FULL = "%d-%B-%Y"  # DD-MMMM-YYYY
    
    # GUI Settings
    GUI_TITLE = "Nifty Indices Historical Data Scraper"
    GUI_WIDTH = 420
    GUI_HEIGHT = 440
    GUI_RESIZABLE = False
    
    # Default Date Values (for GUI)
    DEFAULT_START_DATE = "02-Dec-2025"
    DEFAULT_END_DATE = "06-Dec-2025"
    
    # Output Settings
    DEFAULT_CSV_FILENAME = "nifty_historical_data.csv"
    DEFAULT_EXCEL_FILENAME = "nifty_historical_data.xlsx"

