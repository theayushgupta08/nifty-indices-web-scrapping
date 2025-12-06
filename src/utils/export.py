"""
Data Export Utilities
Handles exporting data to CSV and Excel formats
"""

import pandas as pd
from typing import Optional


def export_to_csv(df: pd.DataFrame, filename: str = 'nifty_historical_data.csv') -> bool:
    """
    Export DataFrame to CSV file
    
    Args:
        df: pandas DataFrame to export
        filename: Output filename (default: 'nifty_historical_data.csv')
        
    Returns:
        True if export successful, False otherwise
    """
    if df is not None and not df.empty:
        try:
            df.to_csv(filename, index=False)
            print(f"\nData successfully exported to {filename}")
            print(f"Total rows: {len(df)}")
            print(f"Columns: {', '.join(df.columns.tolist())}")
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    else:
        print("No data to export.")
        return False


def export_to_excel(df: pd.DataFrame, filename: str = 'nifty_historical_data.xlsx') -> bool:
    """
    Export DataFrame to Excel file
    
    Args:
        df: pandas DataFrame to export
        filename: Output filename (default: 'nifty_historical_data.xlsx')
        
    Returns:
        True if export successful, False otherwise
    """
    if df is not None and not df.empty:
        try:
            df.to_excel(filename, index=False, engine='openpyxl')
            print(f"\nData successfully exported to {filename}")
            print(f"Total rows: {len(df)}")
            print(f"Columns: {', '.join(df.columns.tolist())}")
            return True
        except ImportError:
            print("Error: openpyxl is required for Excel export. Install it using: pip install openpyxl")
            return False
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return False
    else:
        print("No data to export.")
        return False

