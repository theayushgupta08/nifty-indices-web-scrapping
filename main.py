"""
Main Entry Point
Nifty Indices Historical Data Scraper

Usage:
    python main.py              # Run GUI
    python main.py --cli        # Run CLI version
"""

import sys
from src.gui.main_window import create_gui
from src.services.scraper import NiftyIndicesScraper
from src.utils.export import export_to_csv
from src.config.settings import Settings


def main_cli():
    """Main function to run the scraper in CLI mode"""
    print("=" * 60)
    print("Nifty Indices Historical Data Scraper")
    print("=" * 60)
    
    # Configuration - You can modify these parameters
    NAME = "NIFTY BANK"  # Options: "NIFTY 50", "NIFTY NEXT 50", "NIFTY BANK", etc.
    START_DATE = "04-Dec-2020"  # Format: DD-MMM-YYYY (e.g., "01-Nov-2025")
    END_DATE = "04-Dec-2025"  # Format: DD-MMM-YYYY (e.g., "04-Dec-2025")
    INDEX_NAME = "NIFTY BANK"  # Options: "NIFTY 50", "NIFTY NEXT 50", "NIFTY BANK", etc.
    OUTPUT_FILE = "nifty_bank_historical_data.csv"
    
    print("\nConfiguration:")
    print(f"  Index: {INDEX_NAME}")
    print(f"  Start Date: {START_DATE}")
    print(f"  End Date: {END_DATE}")
    print(f"  Output File: {OUTPUT_FILE}")
    
    # Initialize scraper
    scraper = NiftyIndicesScraper(timeout=Settings.API_TIMEOUT)
    
    # Scrape data using API
    df = scraper.scrape_historical_data(
        name=NAME,
        start_date=START_DATE,
        end_date=END_DATE,
        index_name=INDEX_NAME
    )
    
    # Export to CSV
    if df is not None:
        export_to_csv(df, OUTPUT_FILE)
    else:
        print("\nFailed to scrape data. Please check:")
        print("1. Internet connection")
        print("2. The website is accessible")
        print("3. The index name and date range are valid")
        print("4. The API endpoint is working")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        main_cli()
    else:
        # Run GUI by default
        create_gui()

