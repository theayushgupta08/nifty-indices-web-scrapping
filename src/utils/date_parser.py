"""
Date Parsing Utilities
Handles date string parsing and validation
"""

from datetime import datetime
from typing import Optional


def parse_date(date_str: str) -> Optional[datetime]:
    """
    Parse date string in DD-MMM-YYYY format to datetime object
    
    Supports both abbreviated (Dec) and full month names (December)
    
    Args:
        date_str: Date string in DD-MMM-YYYY or DD-MMMM-YYYY format
        
    Returns:
        datetime object if parsing successful, None otherwise
        
    Examples:
        >>> parse_date("02-Dec-2025")
        datetime.datetime(2025, 12, 2, 0, 0)
        >>> parse_date("02-December-2025")
        datetime.datetime(2025, 12, 2, 0, 0)
    """
    try:
        return datetime.strptime(date_str, "%d-%b-%Y")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%d-%B-%Y")
        except ValueError:
            return None

