"""
Nifty Indices API Client
Handles all API communication with Nifty Indices endpoints
"""

import requests
import json
from typing import List, Optional, Dict, Any
from .payloads import (
    HistoricalDataPayload,
    SubIndexTypePayload,
    IndexDataPayload
)


class NiftyIndicesAPIClient:
    """
    API Client for Nifty Indices endpoints
    
    Base URL: https://www.niftyindices.com
    """
    
    BASE_URL = "https://www.niftyindices.com"
    TIMEOUT = 30
    
    # API Endpoints
    ENDPOINT_HISTORICAL_DATA = "/Backpage.aspx/getHistoricaldatatabletoString"
    ENDPOINT_SUB_INDEX_TYPES = "/Backpage.aspx/gethistoricaltypeSubindexdata"
    ENDPOINT_INDEX_DATA = "/Backpage.aspx/gethistoricaltypeindexdata"
    
    def __init__(self, timeout: int = 30):
        """
        Initialize API client
        
        Args:
            timeout: Request timeout in seconds (default: 30)
        """
        self.timeout = timeout
        self.session = requests.Session()
        self._setup_headers()
    
    def _setup_headers(self):
        """Setup default headers for API requests"""
        self.default_headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": self.BASE_URL,
            "Referer": f"{self.BASE_URL}/reports/historical-data"
        }
    
    def _parse_response(self, response_data: Any) -> Any:
        """
        Parse API response handling ASP.NET format
        
        Args:
            response_data: Raw response data from API
            
        Returns:
            Parsed data (usually a list or dict)
        """
        if isinstance(response_data, dict):
            # Check if data is in 'd' field (common in ASP.NET responses)
            if 'd' in response_data:
                data_content = response_data['d']
                # If 'd' is a string, parse it as JSON
                if isinstance(data_content, str):
                    try:
                        return json.loads(data_content)
                    except json.JSONDecodeError:
                        return data_content
                else:
                    return data_content
            else:
                return response_data
        elif isinstance(response_data, list):
            return response_data
        elif isinstance(response_data, str):
            try:
                return json.loads(response_data)
            except json.JSONDecodeError:
                return response_data
        else:
            return response_data
    
    def get_historical_data(
        self,
        payload: HistoricalDataPayload
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get historical data for an index
        
        API Endpoint: /Backpage.aspx/getHistoricaldatatabletoString
        Method: POST
        
        Args:
            payload: HistoricalDataPayload object
            
        Returns:
            List of historical data records or None if error
        """
        url = f"{self.BASE_URL}{self.ENDPOINT_HISTORICAL_DATA}"
        api_payload = payload.to_api_payload()
        
        try:
            response = self.session.post(
                url,
                json=api_payload,
                headers=self.default_headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            response_data = response.json()
            json_list = self._parse_response(response_data)
            
            if not isinstance(json_list, list):
                return None
            
            if not json_list:
                return None
            
            return json_list
            
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. The API might be slow or unavailable.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error making API request: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
    
    def get_index_types(self) -> List[str]:
        """
        Get available index types
        
        Returns:
            List of index types (hardcoded as per requirements)
        """
        # Index types are hardcoded as per user requirement
        return ["Equity", "Fixed Income", "Multi Asset"]
    
    def get_sub_index_types(
        self,
        payload: SubIndexTypePayload
    ) -> List[str]:
        """
        Get sub-index types based on index type
        
        API Endpoint: /Backpage.aspx/gethistoricaltypeSubindexdata
        Method: POST
        
        Args:
            payload: SubIndexTypePayload object
            
        Returns:
            List of sub-index type names
        """
        url = f"{self.BASE_URL}{self.ENDPOINT_SUB_INDEX_TYPES}"
        api_payload = payload.to_api_payload()
        
        try:
            response = self.session.post(
                url,
                json=api_payload,
                headers=self.default_headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            data = self._parse_response(data)
            
            # Extract indexType values
            sub_index_types = []
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        if "indextype" in item and item["indextype"]:
                            sub_index_types.append(str(item["indextype"]))
            elif isinstance(data, dict):
                if "indextype" in data and data["indextype"]:
                    sub_index_types.append(str(data["indextype"]))
            
            # Remove duplicates and empty values, then sort
            sub_index_types = sorted(list(set([s for s in sub_index_types if s])))
            return sub_index_types
            
        except Exception as e:
            raise Exception(f"Error fetching sub-index types: {e}")
    
    def get_indices(
        self,
        payload: IndexDataPayload
    ) -> List[str]:
        """
        Get indices based on sub-index type
        
        API Endpoint: /Backpage.aspx/gethistoricaltypeindexdata
        Method: POST
        
        Args:
            payload: IndexDataPayload object
            
        Returns:
            List of index names
        """
        url = f"{self.BASE_URL}{self.ENDPOINT_INDEX_DATA}"
        api_payload = payload.to_api_payload()
        
        try:
            response = self.session.post(
                url,
                json=api_payload,
                headers=self.default_headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            data = self._parse_response(data)
            
            # Extract indexType values
            indices = []
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        if 'indextype' in item and item['indextype']:
                            indices.append(str(item['indextype']))
            elif isinstance(data, dict):
                if 'indextype' in data and data['indextype']:
                    indices.append(str(data['indextype']))
            
            # Remove duplicates and empty values, then sort
            indices = sorted(list(set([s for s in indices if s])))
            return indices
            
        except Exception as e:
            raise Exception(f"Error fetching indices: {e}")

