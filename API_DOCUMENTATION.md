# API Documentation

This document describes all API endpoints and their payload structures used in the Nifty Indices Web Scraper.

## Base URL
```
https://www.niftyindices.com
```

## API Endpoints

### 1. Historical Data Endpoint

**Endpoint:** `/Backpage.aspx/getHistoricaldatatabletoString`  
**Method:** `POST`  
**Description:** Fetches historical data for a given index within a date range.

**Payload Structure:**
```python
{
    "cinfo": "{'name':'INDEX_NAME','startDate':'DD-MMM-YYYY','endDate':'DD-MMM-YYYY','indexName':'INDEX_NAME'}"
}
```

**Note:** The `cinfo` field is a string representation of a dictionary.

**Python Payload Class:**
```python
from src.api.payloads import HistoricalDataPayload

payload = HistoricalDataPayload(
    name="NIFTY BANK",
    start_date="01-Nov-2025",
    end_date="04-Dec-2025",
    index_name="NIFTY BANK"
)
```

**Response Format:**
```json
{
    "d": [
        {
            "HistoricalDate": "01-Nov-2025",
            "OPEN": "45000.00",
            "HIGH": "45200.00",
            "LOW": "44900.00",
            "CLOSE": "45100.00"
        },
        ...
    ]
}
```

**Usage:**
```python
from src.api.client import NiftyIndicesAPIClient
from src.api.payloads import HistoricalDataPayload

client = NiftyIndicesAPIClient()
payload = HistoricalDataPayload(
    name="NIFTY BANK",
    start_date="01-Nov-2025",
    end_date="04-Dec-2025",
    index_name="NIFTY BANK"
)
data = client.get_historical_data(payload)
```

---

### 2. Sub-Index Types Endpoint

**Endpoint:** `/Backpage.aspx/gethistoricaltypeSubindexdata`  
**Method:** `POST`  
**Description:** Fetches sub-index types for a given index type.

**Payload Structure:**
```python
{
    "cinfo": {
        "indextype": "Equity",
        "indexgroup": "Historical Index Data"
    }
}
```

**Python Payload Class:**
```python
from src.api.payloads import SubIndexTypePayload

payload = SubIndexTypePayload(
    index_type="Equity",
    index_group="Historical Index Data"  # Optional, defaults to "Historical Index Data"
)
```

**Response Format:**
```json
{
    "d": [
        {
            "indextype": "Nifty 50"
        },
        {
            "indextype": "Nifty Next 50"
        },
        ...
    ]
}
```

**Usage:**
```python
from src.api.client import NiftyIndicesAPIClient
from src.api.payloads import SubIndexTypePayload

client = NiftyIndicesAPIClient()
payload = SubIndexTypePayload(index_type="Equity")
sub_index_types = client.get_sub_index_types(payload)
```

---

### 3. Index Data Endpoint

**Endpoint:** `/Backpage.aspx/gethistoricaltypeindexdata`  
**Method:** `POST`  
**Description:** Fetches indices for a given sub-index type.

**Payload Structure:**
```python
{
    "cinfo": {
        "indextype": "SUB_INDEX_TYPE",
        "indexgroup": "Historical Index Data"
    }
}
```

**Python Payload Class:**
```python
from src.api.payloads import IndexDataPayload

payload = IndexDataPayload(
    index_type="Nifty 50",  # This is the sub-index type
    index_group="Historical Index Data"  # Optional, defaults to "Historical Index Data"
)
```

**Response Format:**
```json
{
    "d": [
        {
            "indextype": "NIFTY 50"
        },
        {
            "indextype": "NIFTY BANK"
        },
        ...
    ]
}
```

**Usage:**
```python
from src.api.client import NiftyIndicesAPIClient
from src.api.payloads import IndexDataPayload

client = NiftyIndicesAPIClient()
payload = IndexDataPayload(index_type="Nifty 50")
indices = client.get_indices(payload)
```

---

## Common Headers

All API requests use the following headers:

```python
{
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.niftyindices.com",
    "Referer": "https://www.niftyindices.com/reports/historical-data"
}
```

## Response Parsing

All API responses are automatically parsed by the `NiftyIndicesAPIClient` class. The client handles:

1. ASP.NET response format (data in `d` field)
2. JSON string parsing
3. Direct list/dict responses

## Error Handling

The API client raises exceptions for:
- Request timeouts
- HTTP errors
- JSON parsing errors
- Network errors

Example error handling:
```python
from src.api.client import NiftyIndicesAPIClient
from src.api.payloads import HistoricalDataPayload

try:
    client = NiftyIndicesAPIClient()
    payload = HistoricalDataPayload(...)
    data = client.get_historical_data(payload)
except Exception as e:
    print(f"Error: {e}")
```

## Index Types

Available index types (hardcoded):
- "Equity"
- "Fixed Income"
- "Multi Asset"

These can be retrieved using:
```python
client = NiftyIndicesAPIClient()
index_types = client.get_index_types()
```

