"""
API Payload Structures
Defines all payload structures used in API requests
"""

from typing import Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class HistoricalDataPayload:
    """
    Payload structure for historical data API endpoint
    
    API Endpoint: /Backpage.aspx/getHistoricaldatatabletoString
    Method: POST
    
    Payload Structure:
    {
        "cinfo": "{'name':'INDEX_NAME','startDate':'DD-MMM-YYYY','endDate':'DD-MMM-YYYY','indexName':'INDEX_NAME'}"
    }
    
    Note: The cinfo field is a string representation of a dictionary
    """
    name: str
    start_date: str  # Format: DD-MMM-YYYY
    end_date: str    # Format: DD-MMM-YYYY
    index_name: str
    
    def to_api_payload(self) -> Dict[str, Any]:
        """
        Convert to API payload format
        The API expects cinfo as a string representation of dictionary
        """
        cinfo_string = (
            f"{{'name':'{self.name}',"
            f"'startDate':'{self.start_date}',"
            f"'endDate':'{self.end_date}',"
            f"'indexName':'{self.index_name}'}}"
        )
        return {"cinfo": cinfo_string}


@dataclass
class SubIndexTypePayload:
    """
    Payload structure for sub-index type API endpoint
    
    API Endpoint: /Backpage.aspx/gethistoricaltypeSubindexdata
    Method: POST
    
    Payload Structure:
    {
        "cinfo": {
            "indextype": "INDEX_TYPE",
            "indexgroup": "Historical Index Data"
        }
    }
    """
    index_type: str
    index_group: str = "Historical Index Data"
    
    def to_api_payload(self) -> Dict[str, Any]:
        """Convert to API payload format"""
        return {
            "cinfo": {
                "indextype": self.index_type,
                "indexgroup": self.index_group
            }
        }


@dataclass
class IndexDataPayload:
    """
    Payload structure for index data API endpoint
    
    API Endpoint: /Backpage.aspx/gethistoricaltypeindexdata
    Method: POST
    
    Payload Structure:
    {
        "cinfo": {
            "indextype": "SUB_INDEX_TYPE",
            "indexgroup": "Historical Index Data"
        }
    }
    """
    index_type: str  # This is the sub-index type
    index_group: str = "Historical Index Data"
    
    def to_api_payload(self) -> Dict[str, Any]:
        """Convert to API payload format"""
        return {
            "cinfo": {
                "indextype": self.index_type,
                "indexgroup": self.index_group
            }
        }

