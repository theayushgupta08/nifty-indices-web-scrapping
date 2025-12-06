# Nifty Indices Web Scraper

A production-grade web scraper for fetching historical data from Nifty Indices. This application provides both GUI and CLI interfaces to retrieve historical index data (Open, High, Low, Close prices) for various Nifty indices within specified date ranges. The data can be exported to CSV or Excel formats for further analysis.

## Project Description

This project scrapes historical financial data from the Nifty Indices website (https://www.niftyindices.com) by interacting with their ASP.NET backend APIs. Instead of traditional web scraping, the application uses direct API calls to fetch structured JSON data, making it more reliable and efficient. The application supports multiple index types (Equity, Fixed Income, Multi Asset) with cascading dropdown menus to help users select the desired index. Users can specify custom date ranges and export the retrieved data in their preferred format.

## Project Structure

```
nifty-indices-web-scrapping/
├── src/
│   ├── __init__.py
│   ├── api/                    # API client and payload structures
│   │   ├── __init__.py
│   │   ├── client.py           # NiftyIndicesAPIClient - handles all API calls
│   │   └── payloads.py         # Payload data classes for all API endpoints
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   └── scraper.py          # NiftyIndicesScraper - main scraping service
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── date_parser.py      # Date parsing utilities
│   │   └── export.py           # CSV/Excel export functions
│   ├── gui/                     # GUI components
│   │   ├── __init__.py
│   │   └── main_window.py       # Tkinter GUI implementation
│   └── config/                  # Configuration
│       ├── __init__.py
│       └── settings.py          # Application settings
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Features

- **Production-Grade Architecture**: Organized into modular components (API, Services, GUI, Utils, Config)
- **Centralized API Management**: All API endpoints and payload structures in one place
- **GUI Interface**: User-friendly Tkinter-based interface
- **CLI Support**: Command-line interface for automation
- **Multiple Export Formats**: Support for CSV and Excel exports
- **Error Handling**: Comprehensive error handling and validation

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd nifty-indices-web-scrapping
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Mode (Default)
```bash
python main.py
```

### CLI Mode
```bash
python main.py --cli
```

## API Endpoints

All API endpoints are centralized in `src/api/client.py`:

1. **Historical Data**
   - Endpoint: `/Backpage.aspx/getHistoricaldatatabletoString`
   - Payload: `HistoricalDataPayload` (see `src/api/payloads.py`)

2. **Sub-Index Types**
   - Endpoint: `/Backpage.aspx/gethistoricaltypeSubindexdata`
   - Payload: `SubIndexTypePayload` (see `src/api/payloads.py`)

3. **Index Data**
   - Endpoint: `/Backpage.aspx/gethistoricaltypeindexdata`
   - Payload: `IndexDataPayload` (see `src/api/payloads.py`)

## Payload Structures

All payload structures are defined in `src/api/payloads.py`:

- `HistoricalDataPayload`: For fetching historical data
- `SubIndexTypePayload`: For fetching sub-index types
- `IndexDataPayload`: For fetching indices

## Configuration

Application settings can be modified in `src/config/settings.py`:

- API base URL and timeout
- Default date formats
- GUI dimensions and settings
- Default output filenames

## Dependencies

- `requests`: HTTP library for API calls
- `pandas`: Data manipulation and export
- `openpyxl`: Excel file support
- `tkinter`: GUI framework (usually included with Python)

## Key Learnings

This project demonstrates several important software engineering concepts and best practices:

### 1. **API-First Approach vs Web Scraping**
   - **Learning**: Instead of parsing HTML with BeautifulSoup, the application directly calls the underlying ASP.NET APIs
   - **Benefit**: More reliable, faster, and less prone to breaking when the website's HTML structure changes
   - **Implementation**: All API endpoints are centralized in `src/api/client.py` with proper error handling

### 2. **Production-Grade Code Organization**
   - **Learning**: Separating concerns into distinct layers (API, Services, GUI, Utils, Config)
   - **Benefit**: Makes the codebase maintainable, testable, and scalable
   - **Structure**: 
     - API layer handles HTTP communication
     - Service layer contains business logic
     - GUI layer manages user interface
     - Utils provide reusable functions
     - Config centralizes settings

### 3. **Centralized API Management**
   - **Learning**: All API endpoints and payload structures are defined in one place
   - **Benefit**: Easy to maintain, update, and document API interactions
   - **Implementation**: 
     - `src/api/client.py` contains all API methods
     - `src/api/payloads.py` defines all payload data classes with clear documentation

### 4. **Data Class Patterns**
   - **Learning**: Using Python dataclasses for payload structures provides type safety and clear documentation
   - **Benefit**: Self-documenting code, easier to understand API requirements
   - **Example**: `HistoricalDataPayload`, `SubIndexTypePayload`, `IndexDataPayload`

### 5. **ASP.NET Response Handling**
   - **Learning**: ASP.NET APIs often wrap responses in a `d` field, and sometimes return JSON strings that need parsing
   - **Benefit**: Robust response parsing handles various response formats gracefully
   - **Implementation**: `_parse_response()` method in `NiftyIndicesAPIClient`

### 6. **GUI Threading**
   - **Learning**: Long-running operations (API calls) should run in separate threads to prevent UI freezing
   - **Benefit**: Responsive user interface even during network operations
   - **Implementation**: Threading in `src/gui/main_window.py` for async API calls

### 7. **Error Handling and User Feedback**
   - **Learning**: Comprehensive error handling with user-friendly messages
   - **Benefit**: Better user experience and easier debugging
   - **Implementation**: Try-except blocks with specific error messages and status updates

### 8. **Configuration Management**
   - **Learning**: Centralizing configuration in a settings class makes it easy to modify behavior
   - **Benefit**: No need to hunt through code to change defaults or settings
   - **Implementation**: `src/config/settings.py` contains all configurable values

### 9. **Modular Design Principles**
   - **Learning**: Each module has a single responsibility and clear interfaces
   - **Benefit**: Code is easier to test, maintain, and extend
   - **Example**: Date parsing, export functions, and API calls are all separate modules

### 10. **Documentation Best Practices**
   - **Learning**: Comprehensive documentation (docstrings, API docs, README) is crucial for maintainability
   - **Benefit**: New developers can understand and contribute to the project quickly
   - **Implementation**: 
     - Docstrings in all classes and methods
     - `API_DOCUMENTATION.md` for API reference
     - Clear README with usage examples

## License

See LICENSE file for details.
