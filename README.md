# HTTP Data Serve API

A FastAPI-based service that provides JSON data with various data types, pagination support, and a beautiful web UI for exploration.

## Features

- 🚀 **RESTful API** with automatic OpenAPI documentation
- 📊 **Multiple Data Types**: Supports all common JSON data types (string, integer, float, boolean, array, object, null)
- 📄 **Pagination**: Configurable page size and navigation
- 🎨 **Modern Web UI**: Beautiful, responsive interface for API exploration
- 🔍 **Schema Endpoint**: Get JSON schema for data validation
- ⚡ **Fast Performance**: Built with FastAPI for high performance
- 🎛️ **User-Configurable Records**: Specify total number of records (1-10,000)
- 🗓️ **Multiple Date Formats**: Dedicated API with various date format options
- 🔄 **API Selection**: Choose between standard or date-formats API from the UI

## Data Structure

Each JSON object in the response contains the following fields with specific data types:

- `id` (integer): Unique identifier
- `uuid` (string): UUID format string
- `name` (string): User name
- `email` (string): Email address
- `age` (integer): Age in years
- `height` (float): Height in centimeters
- `weight` (float): Weight in kilograms
- `is_active` (boolean): Active status
- `balance` (float): Account balance
- `birth_date` (string): Birth date in ISO format
- `created_at` (string): Creation timestamp in ISO format
- `tags` (array): Array of string tags
- `metadata` (object): Nested object with additional properties
- `score` (float, nullable): Optional score value
- `description` (string, nullable): Optional description

## Quick Start

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. Open your browser and navigate to:
   - **Web UI**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Alternative Docs**: http://localhost:8000/redoc

## API Endpoints

### GET /api/data

Returns paginated JSON data with various data types.

**Parameters:**
- `page` (integer, optional): Page number (default: 1, minimum: 1)
- `page_size` (integer, optional): Items per page (default: 10, range: 1-100)
- `total_records` (integer, optional): Total number of records to generate (default: 1000, range: 1-10000)

**Example Request:**
```bash
curl "http://localhost:8000/api/data?page=1&page_size=5&total_records=500"
```

### GET /api/data-with-date-formats

Returns paginated JSON data with multiple date format variations.

**Parameters:**
- `page` (integer, optional): Page number (default: 1, minimum: 1)
- `page_size` (integer, optional): Items per page (default: 10, range: 1-100)
- `total_records` (integer, optional): Total number of records to generate (default: 1000, range: 1-10000)

**Date Format Fields:**
- `birth_date_iso`: ISO format (2023-12-25)
- `birth_date_us`: US format (12/25/2023)
- `birth_date_eu`: EU format (25/12/2023)
- `birth_date_long`: Long format (December 25, 2023)
- `created_at_iso`: ISO datetime (2023-12-25T10:30:00)
- `created_at_timestamp`: Unix timestamp (1703505000)
- `created_at_readable`: Readable format (Mon, Dec 25 2023 10:30 AM)

**Example Request:**
```bash
curl "http://localhost:8000/api/data-with-date-formats?page=1&page_size=3&total_records=100"
```

**Example Response:**
```json
{
  "data": [
    {
      "id": 1,
      "uuid": "123e4567-e89b-12d3-a456-426614174000",
      "name": "User ABC123",
      "email": "user123@example.com",
      "age": 28,
      "height": 175.5,
      "weight": 70.2,
      "is_active": true,
      "balance": 1250.75,
      "birth_date": "1995-03-15",
      "created_at": "2024-01-15T10:30:00",
      "tags": ["python", "api", "web"],
      "metadata": {
        "department": "Engineering",
        "location": "San Francisco",
        "experience_years": 5,
        "skills": ["Python", "React", "SQL"],
        "certification": true,
        "last_login": "2024-01-15T10:30:00"
      },
      "score": 85.5,
      "description": "This is a sample description for user 1"
    }
  ],
  "total": 1000,
  "page": 1,
  "page_size": 5,
  "total_pages": 200,
  "has_next": true,
  "has_previous": false
}
```

### GET /api/schema

Returns the JSON schema for the data objects.

**Example Request:**
```bash
curl "http://localhost:8000/api/schema"
```

## Web UI Features

The built-in web interface provides:

- **API Selection**: Choose between Standard API and Date Formats API
- **Record Count Control**: Specify total number of records (1-10,000)
- **Interactive Controls**: Adjust page size and navigate through pages
- **Real-time Statistics**: View total items, current page, and pagination info
- **JSON Response Viewer**: Formatted JSON display with syntax highlighting
- **Copy Functionality**: One-click copy of JSON responses
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations
- **Dynamic Descriptions**: Context-aware API descriptions based on selection

## Customization

### Modifying Data Generation

To customize the data structure or generation logic, edit the following functions in `main.py`:

- `generate_data_object()`: Main data generation function
- `DataObject` model: Pydantic model defining the structure
- Helper functions: `generate_random_*()` functions for specific data types

### Changing Total Items

Modify the `total_items` variable in the `/api/data` endpoint to change the simulated dataset size.

### UI Customization

The HTML template is embedded in the `root()` function. You can modify the CSS and JavaScript to customize the appearance and behavior.

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

This project is open source and available under the MIT License.
# http-dataserve
