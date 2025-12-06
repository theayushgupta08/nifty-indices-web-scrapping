"""
Nifty Indices Scraper Service
Handles data scraping and processing logic
"""

import pandas as pd
from typing import Optional
from ..api.client import NiftyIndicesAPIClient
from ..api.payloads import HistoricalDataPayload


class NiftyIndicesScraper:
    """
    Service class for scraping Nifty Indices historical data
    """
    
    def __init__(self, timeout: int = 30):
        """
        Initialize scraper with API client
        
        Args:
            timeout: Request timeout in seconds (default: 30)
        """
        self.api_client = NiftyIndicesAPIClient(timeout=timeout)
    
    def scrape_historical_data(
        self,
        name: str,
        start_date: str,
        end_date: str,
        index_name: str
    ) -> Optional[pd.DataFrame]:
        """
        Scrape historical data for an index
        
        Args:
            name: Name of the index to scrape
            start_date: Start date in DD-MMM-YYYY format (e.g., "01-Nov-2025")
            end_date: End date in DD-MMM-YYYY format (e.g., "04-Dec-2025")
            index_name: Name of the index
            
        Returns:
            pandas DataFrame with columns: Date, Open, High, Low, Close
            Returns None if scraping fails
        """
        print(f"Scraping data for: {index_name}")
        print(f"Date range: {start_date} to {end_date}")
        
        # Create payload
        payload = HistoricalDataPayload(
            name=name,
            start_date=start_date,
            end_date=end_date,
            index_name=index_name
        )
        
        try:
            print("Sending API request...")
            json_list = self.api_client.get_historical_data(payload)
            
            if json_list is None:
                print("Error: No data received from API")
                return None
            
            print(f"API request successful. Found {len(json_list)} records")
            print(f"Sample record keys: {json_list[0].keys() if json_list else 'No records'}")
            
            # Extract data from JSON list
            extracted_data = []
            for record in json_list:
                row_data = {
                    'Date': record.get('HistoricalDate', ''),
                    'Open': record.get('OPEN', ''),
                    'High': record.get('HIGH', ''),
                    'Low': record.get('LOW', ''),
                    'Close': record.get('CLOSE', '')
                }
                extracted_data.append(row_data)
            
            # Create DataFrame from extracted data
            df = pd.DataFrame(extracted_data)
            
            print(f"Created DataFrame with {len(df)} rows")
            print(f"DataFrame columns: {df.columns.tolist()}")
            
            # Clean data - remove commas and convert to numeric where applicable
            for col in ['Open', 'High', 'Low', 'Close']:
                if col in df.columns:
                    # Convert to string first, then remove commas
                    df[col] = df[col].astype(str).str.replace(',', '', regex=False)
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Ensure Date column is first and clean it
            if 'Date' in df.columns:
                # Clean Date column - remove extra spaces
                df['Date'] = df['Date'].astype(str).str.strip()
                # Reorder columns: Date first, then Open, High, Low, Close
                cols = ['Date', 'Open', 'High', 'Low', 'Close']
                df = df[cols]
            
            print(f"\nSuccessfully processed {len(df)} rows of data")
            print(f"Final columns: {df.columns.tolist()}")
            print(f"Sample data:\n{df.head()}")
            return df
            
        except Exception as e:
            print(f"An error occurred during scraping: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_index_types(self) -> list:
        """Get available index types"""
        return self.api_client.get_index_types()
    
    def get_sub_index_types(self, index_type: str) -> list:
        """
        Get sub-index types for a given index type
        
        Args:
            index_type: The index type (e.g., "Equity", "Fixed Income", "Multi Asset")
            
        Returns:
            List of sub-index type names
        """
        from ..api.payloads import SubIndexTypePayload
        
        payload = SubIndexTypePayload(index_type=index_type)
        return self.api_client.get_sub_index_types(payload)
    
    def get_indices(self, sub_index_type: str) -> list:
        """
        Get indices for a given sub-index type
        
        Args:
            sub_index_type: The sub-index type
            
        Returns:
            List of index names
        """
        from ..api.payloads import IndexDataPayload
        
        payload = IndexDataPayload(index_type=sub_index_type)
        return self.api_client.get_indices(payload)

