from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
import random
import string
from datetime import datetime, date
from decimal import Decimal
import uuid
import json
import time

app = FastAPI(
    title="HTTP Data Serve API",
    description="API that serves JSON objects with various data types and pagination support",
    version="1.0.0"
)

# Data model for our JSON objects
class DataObject(BaseModel):
    id: int
    uuid: str
    name: str
    email: str
    age: int
    height: float
    weight: float
    is_active: bool
    balance: float
    birth_date: str
    created_at: str
    tags: List[str]
    metadata: Dict[str, Any]
    score: Optional[float]
    description: Optional[str]

# Data model for objects with different date formats
class DataObjectWithDifferentDates(BaseModel):
    id: int
    uuid: str
    name: str
    email: str
    age: int
    height: float
    weight: float
    is_active: bool
    balance: float
    birth_date_iso: str          # ISO format: 2023-12-25
    birth_date_us: str           # US format: 12/25/2023
    birth_date_eu: str           # EU format: 25/12/2023
    birth_date_long: str         # Long format: December 25, 2023
    created_at_iso: str          # ISO datetime: 2023-12-25T10:30:00
    created_at_timestamp: int    # Unix timestamp: 1703505000
    created_at_readable: str     # Readable: Mon, Dec 25 2023 10:30 AM
    tags: List[str]
    metadata: Dict[str, Any]
    score: Optional[float]
    description: Optional[str]

class PaginatedResponse(BaseModel):
    data: List[DataObject]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

class PaginatedResponseWithDifferentDates(BaseModel):
    data: List[DataObjectWithDifferentDates]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

def generate_random_string(length: int = 10) -> str:
    """Generate a random string of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_email() -> str:
    """Generate a random email address."""
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "example.com", "test.org"]
    username = generate_random_string(8).lower()
    domain = random.choice(domains)
    return f"{username}@{domain}"

def generate_random_tags() -> List[str]:
    """Generate random tags."""
    all_tags = ["python", "javascript", "api", "web", "mobile", "data", "ai", "ml", 
                "backend", "frontend", "database", "cloud", "devops", "security"]
    num_tags = random.randint(1, 5)
    return random.sample(all_tags, num_tags)

def generate_random_metadata() -> Dict[str, Any]:
    """Generate random metadata object."""
    return {
        "department": random.choice(["Engineering", "Marketing", "Sales", "HR", "Finance"]),
        "location": random.choice(["New York", "San Francisco", "London", "Tokyo", "Berlin"]),
        "experience_years": random.randint(1, 20),
        "skills": random.sample(["Python", "Java", "React", "Node.js", "SQL", "Docker"], 
                               random.randint(2, 4)),
        "certification": random.choice([True, False]),
        "last_login": datetime.now().isoformat()
    }

def generate_data_object(id: int) -> DataObject:
    """Generate a single data object with all data types."""
    return DataObject(
        id=id,
        uuid=str(uuid.uuid4()),
        name=f"User {generate_random_string(6)}",
        email=generate_random_email(),
        age=random.randint(18, 80),
        height=round(random.uniform(150.0, 200.0), 2),
        weight=round(random.uniform(45.0, 120.0), 2),
        is_active=random.choice([True, False]),
        balance=round(random.uniform(0.0, 100000.0), 2),
        birth_date=date(
            random.randint(1940, 2005),
            random.randint(1, 12),
            random.randint(1, 28)
        ).isoformat(),
        created_at=datetime.now().isoformat(),
        tags=generate_random_tags(),
        metadata=generate_random_metadata(),
        score=round(random.uniform(0.0, 100.0), 2) if random.choice([True, False]) else None,
        description=f"This is a sample description for user {id}" if random.choice([True, False]) else None
    )

def generate_data_object_with_different_dates(id: int) -> DataObjectWithDifferentDates:
    """Generate a single data object with different date formats."""
    # Generate random birth date
    birth_date_obj = date(
        random.randint(1940, 2005),
        random.randint(1, 12),
        random.randint(1, 28)
    )
    
    # Generate random created datetime
    created_datetime = datetime.now().replace(
        year=random.randint(2020, 2024),
        month=random.randint(1, 12),
        day=random.randint(1, 28),
        hour=random.randint(0, 23),
        minute=random.randint(0, 59)
    )
    
    return DataObjectWithDifferentDates(
        id=id,
        uuid=str(uuid.uuid4()),
        name=f"User {generate_random_string(6)}",
        email=generate_random_email(),
        age=random.randint(18, 80),
        height=round(random.uniform(150.0, 200.0), 2),
        weight=round(random.uniform(45.0, 120.0), 2),
        is_active=random.choice([True, False]),
        balance=round(random.uniform(0.0, 100000.0), 2),
        # Different birth date formats
        birth_date_iso=birth_date_obj.isoformat(),  # 2023-12-25
        birth_date_us=birth_date_obj.strftime("%m/%d/%Y"),  # 12/25/2023
        birth_date_eu=birth_date_obj.strftime("%d/%m/%Y"),  # 25/12/2023
        birth_date_long=birth_date_obj.strftime("%B %d, %Y"),  # December 25, 2023
        # Different created_at formats
        created_at_iso=created_datetime.isoformat(),  # 2023-12-25T10:30:00
        created_at_timestamp=int(created_datetime.timestamp()),  # Unix timestamp
        created_at_readable=created_datetime.strftime("%a, %b %d %Y %I:%M %p"),  # Mon, Dec 25 2023 10:30 AM
        tags=generate_random_tags(),
        metadata=generate_random_metadata(),
        score=round(random.uniform(0.0, 100.0), 2) if random.choice([True, False]) else None,
        description=f"This is a sample description for user {id}" if random.choice([True, False]) else None
    )

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main UI page."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HTTP Data Serve API Explorer</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            .header p {
                font-size: 1.2em;
                opacity: 0.9;
            }
            
            .content {
                padding: 30px;
            }
            
            .controls {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
                padding: 25px;
                background: #f8f9fa;
                border-radius: 10px;
                border: 2px solid #e9ecef;
            }
            
            .control-group {
                display: flex;
                flex-direction: column;
            }
            
            .control-group label {
                font-weight: 600;
                color: #495057;
                margin-bottom: 8px;
                font-size: 0.9em;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .control-group input, .control-group select, .control-group button {
                padding: 12px 15px;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                font-size: 1em;
                transition: all 0.3s ease;
                background: white;
            }
            
            .control-group input:focus, .control-group select:focus {
                outline: none;
                border-color: #4facfe;
                box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
            }
            
            .api-description {
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 25px;
                border: 2px solid #90caf9;
            }
            
            .api-description h3 {
                margin: 0 0 10px 0;
                color: #1565c0;
                font-size: 1.2em;
            }
            
            .api-description p {
                margin: 0;
                color: #1976d2;
                line-height: 1.5;
            }
            
            .api-details {
                background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 25px;
                border: 2px solid #ce93d8;
            }
            
            .api-details h4 {
                margin: 0 0 15px 0;
                color: #7b1fa2;
                font-size: 1.1em;
            }
            
            .parameters-section {
                margin-bottom: 20px;
            }
            
            .parameters-section ul {
                margin: 0;
                padding-left: 20px;
                color: #8e24aa;
            }
            
            .parameters-section li {
                margin-bottom: 8px;
                line-height: 1.4;
            }
            
            .example-section code {
                display: block;
                background: #4a148c;
                color: #e1bee7;
                padding: 10px 15px;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
                word-wrap: break-word;
                margin: 0;
            }
            
            .api-list-section {
                margin-bottom: 30px;
            }
            
            .api-list-section h3 {
                text-align: center;
                color: #495057;
                margin-bottom: 25px;
                font-size: 1.5em;
            }
            
            .api-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }
            
            .api-card {
                background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
                border: 2px solid #ffcc02;
                border-radius: 12px;
                padding: 20px;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                position: relative;
                overflow: hidden;
            }
            
            .api-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(255, 204, 2, 0.3);
                border-color: #ff9800;
            }
            
            .api-card.selected {
                border-color: #ff5722;
                background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
                box-shadow: 0 8px 25px rgba(255, 87, 34, 0.3);
            }
            
            .api-card-header {
                display: flex;
                align-items: center;
                margin-bottom: 12px;
            }
            
            .api-card-icon {
                font-size: 2em;
                margin-right: 12px;
            }
            
            .api-card-title {
                font-size: 1.2em;
                font-weight: 600;
                color: #e65100;
                margin: 0;
            }
            
            .api-card-path {
                font-family: 'Courier New', monospace;
                background: rgba(0,0,0,0.1);
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.8em;
                color: #bf360c;
                margin-bottom: 10px;
            }
            
            .api-card-description {
                color: #f57c00;
                font-size: 0.9em;
                line-height: 1.4;
                margin-bottom: 15px;
            }
            
            .api-card-actions {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }
            
            .api-action-btn {
                background: #ff5722;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 0.8em;
                cursor: pointer;
                transition: background 0.3s ease;
                font-weight: 500;
            }
            
            .api-action-btn:hover {
                background: #d84315;
            }
            
            .api-action-btn.secondary {
                background: #757575;
            }
            
            .api-action-btn.secondary:hover {
                background: #424242;
            }
            
            .fetch-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                cursor: pointer;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .fetch-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            .fetch-btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            
            .info-section {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                margin-bottom: 25px;
            }
            
            .info-card {
                background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .info-card h3 {
                font-size: 2em;
                color: #8b4513;
                margin-bottom: 5px;
            }
            
            .info-card p {
                color: #a0522d;
                font-weight: 500;
                text-transform: uppercase;
                font-size: 0.8em;
                letter-spacing: 1px;
            }
            
            .pagination {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 10px;
                margin: 25px 0;
                flex-wrap: wrap;
            }
            
            .pagination button {
                padding: 10px 15px;
                border: 2px solid #dee2e6;
                background: white;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 500;
                transition: all 0.3s ease;
            }
            
            .pagination button:hover:not(:disabled) {
                background: #4facfe;
                color: white;
                border-color: #4facfe;
            }
            
            .pagination button:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            .pagination .current-page {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-color: #667eea;
            }
            
            .response-container {
                background: #f8f9fa;
                border-radius: 10px;
                overflow: hidden;
                border: 2px solid #e9ecef;
            }
            
            .response-header {
                background: #343a40;
                color: white;
                padding: 15px 20px;
                font-weight: 600;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .copy-btn {
                background: #28a745;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 0.8em;
                transition: background 0.3s ease;
            }
            
            .copy-btn:hover {
                background: #218838;
            }
            
            .json-response {
                padding: 20px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
                line-height: 1.6;
                max-height: 600px;
                overflow-y: auto;
                white-space: pre-wrap;
                word-wrap: break-word;
                background: #ffffff;
            }
            
            .loading {
                text-align: center;
                padding: 40px;
                color: #6c757d;
                font-style: italic;
            }
            
            .error {
                background: #f8d7da;
                color: #721c24;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                border: 1px solid #f5c6cb;
            }
            
            @media (max-width: 768px) {
                .controls {
                    grid-template-columns: 1fr;
                }
                
                .info-section {
                    grid-template-columns: repeat(2, 1fr);
                }
                
                .pagination {
                    justify-content: center;
                }
                
                .header h1 {
                    font-size: 2em;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 HTTP Data Serve API</h1>
                <p>Explore JSON data with various data types and pagination</p>
            </div>
            
            <div class="content">
                <div class="controls">
                    <div class="control-group">
                        <label for="apiType">Select API Endpoint</label>
                        <select id="apiType" onchange="updateApiDescription()">
                            <option value="">Loading APIs...</option>
                        </select>
                    </div>
                    <div class="control-group" id="totalRecordsGroup">
                        <label for="totalRecords">Total Records</label>
                        <input type="number" id="totalRecords" min="1" max="10000" value="1000">
                    </div>
                    <div class="control-group" id="pageSizeGroup">
                        <label for="pageSize">Page Size</label>
                        <input type="number" id="pageSize" min="1" max="100" value="10">
                    </div>
                    <div class="control-group" id="currentPageGroup">
                        <label for="currentPage">Current Page</label>
                        <input type="number" id="currentPage" min="1" value="1">
                    </div>
                    <div class="control-group">
                        <label>&nbsp;</label>
                        <button class="fetch-btn" onclick="fetchData()" id="fetchBtn" disabled>Fetch Data</button>
                    </div>
                </div>
                
                <div class="api-list-section" id="apiListSection">
                    <h3>🔄 Loading Available APIs...</h3>
                    <div class="api-grid" id="apiGrid">
                        <!-- APIs will be loaded here -->
                    </div>
                </div>
                
                <div class="api-description" id="apiDescription" style="display: none;">
                    <h3>📊 Selected API</h3>
                    <p>Select an API from the list above to see details and make requests.</p>
                </div>
                
                <div class="api-details" id="apiDetails" style="display: none;">
                    <div class="parameters-section">
                        <h4>📋 Parameters</h4>
                        <ul id="parametersList"></ul>
                    </div>
                    <div class="example-section">
                        <h4>💡 Example URL</h4>
                        <code id="exampleUrl"></code>
                    </div>
                </div>
                
                <div class="info-section" id="infoSection" style="display: none;">
                    <div class="info-card">
                        <h3 id="totalItems">-</h3>
                        <p>Total Items</p>
                    </div>
                    <div class="info-card">
                        <h3 id="currentPageInfo">-</h3>
                        <p>Current Page</p>
                    </div>
                    <div class="info-card">
                        <h3 id="totalPages">-</h3>
                        <p>Total Pages</p>
                    </div>
                    <div class="info-card">
                        <h3 id="itemsShown">-</h3>
                        <p>Items Shown</p>
                    </div>
                </div>
                
                <div class="pagination" id="pagination" style="display: none;"></div>
                
                <div class="response-container">
                    <div class="response-header">
                        <span>API Response</span>
                        <button class="copy-btn" onclick="copyResponse()">Copy JSON</button>
                    </div>
                    <div class="json-response" id="jsonResponse">
                        <div class="loading">👋 Welcome! Click "Fetch Data" to explore the API response</div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let currentResponse = null;
            let availableEndpoints = [];

            async function loadAvailableEndpoints() {
                try {
                    const response = await fetch('/api/endpoints');
                    const data = await response.json();
                    availableEndpoints = data.endpoints;
                    
                    // Create API grid
                    createApiGrid();
                    
                    // Populate the dropdown (keep for compatibility)
                    const select = document.getElementById('apiType');
                    select.innerHTML = '';
                    
                    availableEndpoints.forEach((endpoint, index) => {
                        const option = document.createElement('option');
                        option.value = endpoint.path;
                        option.textContent = endpoint.name;
                        select.appendChild(option);
                    });
                    
                    // Select the first endpoint by default
                    if (availableEndpoints.length > 0) {
                        select.value = availableEndpoints[0].path;
                        document.getElementById('fetchBtn').disabled = false;
                    }
                    
                } catch (error) {
                    console.error('Failed to load endpoints:', error);
                    document.getElementById('apiListSection').innerHTML = `
                        <div class="error">❌ Failed to load API endpoints: ${error.message}</div>
                    `;
                }
            }

            function createApiGrid() {
                const gridContainer = document.getElementById('apiGrid');
                const sectionTitle = document.querySelector('#apiListSection h3');
                
                sectionTitle.textContent = '🚀 Available API Endpoints';
                gridContainer.innerHTML = '';
                
                availableEndpoints.forEach((endpoint, index) => {
                    const card = document.createElement('div');
                    card.className = 'api-card';
                    card.setAttribute('data-endpoint', endpoint.path);
                    
                    // Determine icon
                    let icon = '📊';
                    if (endpoint.path.includes('date-formats')) icon = '🗓️';
                    else if (endpoint.path.includes('schema')) icon = '🔍';
                    else if (endpoint.path.includes('endpoints')) icon = '📋';
                    
                    // Create action buttons
                    let actionButtons = '';
                    if (endpoint.parameters && endpoint.parameters.length > 0) {
                        actionButtons = `
                            <button class="api-action-btn" onclick="quickFetch('${endpoint.path}', 'default')">
                                🚀 Quick Fetch
                            </button>
                            <button class="api-action-btn secondary" onclick="selectApiForCustomization('${endpoint.path}')">
                                ⚙️ Customize
                            </button>
                        `;
                    } else {
                        actionButtons = `
                            <button class="api-action-btn" onclick="quickFetch('${endpoint.path}', 'simple')">
                                🚀 Fetch Data
                            </button>
                        `;
                    }
                    
                    // Special fields info
                    let specialFieldsInfo = '';
                    if (endpoint.special_fields) {
                        const fieldsPreview = endpoint.special_fields.slice(0, 3).join(', ');
                        specialFieldsInfo = `
                            <div style="margin-top: 10px; padding: 8px; background: rgba(0,0,0,0.05); border-radius: 6px; font-size: 0.8em;">
                                <strong>Special Fields:</strong> ${fieldsPreview}${endpoint.special_fields.length > 3 ? '...' : ''}
                            </div>
                        `;
                    }
                    
                    card.innerHTML = `
                        <div class="api-card-header">
                            <span class="api-card-icon">${icon}</span>
                            <h4 class="api-card-title">${endpoint.name}</h4>
                        </div>
                        <div class="api-card-path">${endpoint.path}</div>
                        <div class="api-card-description">${endpoint.description}</div>
                        ${specialFieldsInfo}
                        <div class="api-card-actions">
                            ${actionButtons}
                        </div>
                    `;
                    
                    gridContainer.appendChild(card);
                });
            }

            function updateApiDescription() {
                const selectedPath = document.getElementById('apiType').value;
                const endpoint = availableEndpoints.find(ep => ep.path === selectedPath);
                
                if (!endpoint) return;
                
                const descriptionDiv = document.getElementById('apiDescription');
                const detailsDiv = document.getElementById('apiDetails');
                
                // Update description
                let icon = '📊';
                if (endpoint.path.includes('date-formats')) icon = '🗓️';
                else if (endpoint.path.includes('schema')) icon = '🔍';
                
                descriptionDiv.innerHTML = `
                    <h3>${icon} ${endpoint.name}</h3>
                    <p>${endpoint.description}</p>
                `;
                
                // Update details
                if (endpoint.parameters && endpoint.parameters.length > 0) {
                    const parametersList = document.getElementById('parametersList');
                    parametersList.innerHTML = '';
                    
                    endpoint.parameters.forEach(param => {
                        const li = document.createElement('li');
                        li.innerHTML = `<strong>${param.name}</strong> (${param.type}): ${param.description} <em>Default: ${param.default}</em>`;
                        parametersList.appendChild(li);
                    });
                    
                    document.getElementById('exampleUrl').textContent = endpoint.example;
                    detailsDiv.style.display = 'block';
                    
                    // Show/hide parameter controls based on endpoint
                    const hasDataParams = endpoint.parameters.some(p => ['page', 'page_size', 'total_records'].includes(p.name));
                    document.getElementById('totalRecordsGroup').style.display = hasDataParams ? 'flex' : 'none';
                    document.getElementById('pageSizeGroup').style.display = hasDataParams ? 'flex' : 'none';
                    document.getElementById('currentPageGroup').style.display = hasDataParams ? 'flex' : 'none';
                } else {
                    detailsDiv.style.display = 'none';
                    // Hide pagination controls for schema endpoint
                    document.getElementById('totalRecordsGroup').style.display = 'none';
                    document.getElementById('pageSizeGroup').style.display = 'none';
                    document.getElementById('currentPageGroup').style.display = 'none';
                }
                
                // Show special fields for date formats API
                if (endpoint.special_fields) {
                    const specialFieldsHtml = endpoint.special_fields.map(field => `<li>${field}</li>`).join('');
                    descriptionDiv.innerHTML += `
                        <div style="margin-top: 15px;">
                            <h4 style="color: #1565c0; margin-bottom: 10px;">🗓️ Special Date Fields:</h4>
                            <ul style="color: #1976d2; padding-left: 20px; margin: 0;">
                                ${specialFieldsHtml}
                            </ul>
                        </div>
                    `;
                }
            }

            async function quickFetch(apiPath, type = 'default') {
                const responseDiv = document.getElementById('jsonResponse');
                responseDiv.innerHTML = '<div class="loading">🔄 Loading data...</div>';
                
                // Clear previous selections
                document.querySelectorAll('.api-card').forEach(card => {
                    card.classList.remove('selected');
                });
                
                // Highlight selected card
                const selectedCard = document.querySelector(`[data-endpoint="${apiPath}"]`);
                if (selectedCard) {
                    selectedCard.classList.add('selected');
                }
                
                try {
                    let url = apiPath;
                    
                    // Add default parameters for data endpoints
                    if (type === 'default' && (apiPath.includes('/api/data'))) {
                        const totalRecords = document.getElementById('totalRecords').value || 1000;
                        const pageSize = document.getElementById('pageSize').value || 10;
                        const page = document.getElementById('currentPage').value || 1;
                        url += `?page=${page}&page_size=${pageSize}&total_records=${totalRecords}`;
                    }
                    
                    const response = await fetch(url);
                    const data = await response.json();
                    
                    if (!response.ok) {
                        throw new Error(data.detail || 'Failed to fetch data');
                    }
                    
                    currentResponse = data;
                    displayResponse(data);
                    
                    // Update info and pagination for data endpoints
                    if (data.total !== undefined) {
                        updateInfo(data);
                        updatePagination(data);
                        document.getElementById('infoSection').style.display = 'grid';
                        document.getElementById('pagination').style.display = 'flex';
                    } else {
                        document.getElementById('infoSection').style.display = 'none';
                        document.getElementById('pagination').style.display = 'none';
                    }
                    
                    // Show endpoint details
                    const endpoint = availableEndpoints.find(ep => ep.path === apiPath);
                    if (endpoint) {
                        showApiDetails(endpoint);
                    }
                    
                } catch (error) {
                    responseDiv.innerHTML = `<div class="error">❌ Error: ${error.message}</div>`;
                }
            }

            function selectApiForCustomization(apiPath) {
                // Clear previous selections
                document.querySelectorAll('.api-card').forEach(card => {
                    card.classList.remove('selected');
                });
                
                // Highlight selected card
                const selectedCard = document.querySelector(`[data-endpoint="${apiPath}"]`);
                if (selectedCard) {
                    selectedCard.classList.add('selected');
                }
                
                // Update dropdown to match selection
                document.getElementById('apiType').value = apiPath;
                
                // Show endpoint details
                const endpoint = availableEndpoints.find(ep => ep.path === apiPath);
                if (endpoint) {
                    showApiDetails(endpoint);
                }
                
                // Show/hide controls based on endpoint type
                const hasDataParams = endpoint.parameters && endpoint.parameters.some(p => ['page', 'page_size', 'total_records'].includes(p.name));
                document.getElementById('totalRecordsGroup').style.display = hasDataParams ? 'flex' : 'none';
                document.getElementById('pageSizeGroup').style.display = hasDataParams ? 'flex' : 'none';
                document.getElementById('currentPageGroup').style.display = hasDataParams ? 'flex' : 'none';
                
                // Scroll to controls
                document.querySelector('.controls').scrollIntoView({ behavior: 'smooth' });
            }

            function showApiDetails(endpoint) {
                const descriptionDiv = document.getElementById('apiDescription');
                const detailsDiv = document.getElementById('apiDetails');
                
                // Update description
                let icon = '📊';
                if (endpoint.path.includes('date-formats')) icon = '🗓️';
                else if (endpoint.path.includes('schema')) icon = '🔍';
                
                descriptionDiv.innerHTML = `
                    <h3>${icon} ${endpoint.name}</h3>
                    <p>${endpoint.description}</p>
                `;
                
                // Update details
                if (endpoint.parameters && endpoint.parameters.length > 0) {
                    const parametersList = document.getElementById('parametersList');
                    parametersList.innerHTML = '';
                    
                    endpoint.parameters.forEach(param => {
                        const li = document.createElement('li');
                        li.innerHTML = `<strong>${param.name}</strong> (${param.type}): ${param.description} <em>Default: ${param.default}</em>`;
                        parametersList.appendChild(li);
                    });
                    
                    document.getElementById('exampleUrl').textContent = endpoint.example;
                    detailsDiv.style.display = 'block';
                } else {
                    detailsDiv.style.display = 'none';
                }
                
                // Show special fields for date formats API
                if (endpoint.special_fields) {
                    const specialFieldsHtml = endpoint.special_fields.map(field => `<li>${field}</li>`).join('');
                    descriptionDiv.innerHTML += `
                        <div style="margin-top: 15px;">
                            <h4 style="color: #1565c0; margin-bottom: 10px;">🗓️ Special Date Fields:</h4>
                            <ul style="color: #1976d2; padding-left: 20px; margin: 0;">
                                ${specialFieldsHtml}
                            </ul>
                        </div>
                    `;
                }
                
                descriptionDiv.style.display = 'block';
            }

            async function fetchData() {
                const selectedPath = document.getElementById('apiType').value;
                const endpoint = availableEndpoints.find(ep => ep.path === selectedPath);
                const responseDiv = document.getElementById('jsonResponse');
                
                if (!endpoint) {
                    responseDiv.innerHTML = '<div class="error">❌ No endpoint selected</div>';
                    return;
                }
                
                // Show loading
                responseDiv.innerHTML = '<div class="loading">🔄 Loading data...</div>';
                
                try {
                    let url = endpoint.path;
                    
                    // Add parameters if the endpoint supports them
                    const hasDataParams = endpoint.parameters && endpoint.parameters.some(p => ['page', 'page_size', 'total_records'].includes(p.name));
                    
                    if (hasDataParams) {
                        const pageSize = document.getElementById('pageSize').value;
                        const page = document.getElementById('currentPage').value;
                        const totalRecords = document.getElementById('totalRecords').value;
                        url += `?page=${page}&page_size=${pageSize}&total_records=${totalRecords}`;
                    }
                    
                    const response = await fetch(url);
                    const data = await response.json();
                    
                    if (!response.ok) {
                        throw new Error(data.detail || 'Failed to fetch data');
                    }
                    
                    currentResponse = data;
                    displayResponse(data);
                    
                    // Only update pagination info for data endpoints
                    if (hasDataParams && data.total !== undefined) {
                        updateInfo(data);
                        updatePagination(data);
                    } else {
                        // Hide pagination for non-data endpoints
                        document.getElementById('infoSection').style.display = 'none';
                        document.getElementById('pagination').style.display = 'none';
                    }
                    
                } catch (error) {
                    responseDiv.innerHTML = `<div class="error">❌ Error: ${error.message}</div>`;
                }
            }

            function displayResponse(data) {
                const responseDiv = document.getElementById('jsonResponse');
                responseDiv.textContent = JSON.stringify(data, null, 2);
            }

            function updateInfo(data) {
                document.getElementById('totalItems').textContent = data.total;
                document.getElementById('currentPageInfo').textContent = data.page;
                document.getElementById('totalPages').textContent = data.total_pages;
                document.getElementById('itemsShown').textContent = data.data.length;
                document.getElementById('infoSection').style.display = 'grid';
            }

            function updatePagination(data) {
                const paginationDiv = document.getElementById('pagination');
                paginationDiv.innerHTML = '';
                
                // Previous button
                const prevBtn = document.createElement('button');
                prevBtn.textContent = '← Previous';
                prevBtn.disabled = !data.has_previous;
                prevBtn.onclick = () => goToPage(data.page - 1);
                paginationDiv.appendChild(prevBtn);
                
                // Page numbers
                const startPage = Math.max(1, data.page - 2);
                const endPage = Math.min(data.total_pages, data.page + 2);
                
                for (let i = startPage; i <= endPage; i++) {
                    const pageBtn = document.createElement('button');
                    pageBtn.textContent = i;
                    pageBtn.onclick = () => goToPage(i);
                    if (i === data.page) {
                        pageBtn.className = 'current-page';
                    }
                    paginationDiv.appendChild(pageBtn);
                }
                
                // Next button
                const nextBtn = document.createElement('button');
                nextBtn.textContent = 'Next →';
                nextBtn.disabled = !data.has_next;
                nextBtn.onclick = () => goToPage(data.page + 1);
                paginationDiv.appendChild(nextBtn);
                
                paginationDiv.style.display = 'flex';
            }

            function goToPage(page) {
                document.getElementById('currentPage').value = page;
                fetchData();
            }

            function copyResponse() {
                if (currentResponse) {
                    navigator.clipboard.writeText(JSON.stringify(currentResponse, null, 2))
                        .then(() => {
                            const btn = document.querySelector('.copy-btn');
                            const originalText = btn.textContent;
                            btn.textContent = '✅ Copied!';
                            setTimeout(() => {
                                btn.textContent = originalText;
                            }, 2000);
                        })
                        .catch(err => {
                            console.error('Failed to copy: ', err);
                        });
                }
            }

            // Load available endpoints and initial data
            window.onload = async () => {
                await loadAvailableEndpoints();
                // Don't auto-fetch data anymore, let user choose
            };
        </script>
    </body>
    </html>
    """

@app.get("/api/data", response_model=PaginatedResponse)
async def get_data(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    total_records: int = Query(1000, ge=1, le=10000, description="Total number of records to generate (1-10000)")
):
    """
    Get paginated data with various data types.
    
    - **page**: Page number (starts from 1)
    - **page_size**: Number of items per page (1-100)
    - **total_records**: Total number of records to generate (1-10000)
    
    Returns an array of JSON objects with the following data types:
    - **id**: integer
    - **uuid**: string (UUID format)
    - **name**: string
    - **email**: string (email format)
    - **age**: integer
    - **height**: float (in cm)
    - **weight**: float (in kg)
    - **is_active**: boolean
    - **balance**: float (monetary value)
    - **birth_date**: string (ISO date format)
    - **created_at**: string (ISO datetime format)
    - **tags**: array of strings
    - **metadata**: object with nested properties
    - **score**: float (nullable)
    - **description**: string (nullable)
    """
    
    # Use user-specified total records
    total_items = total_records
    
    # Calculate pagination
    total_pages = (total_items + page_size - 1) // page_size
    start_index = (page - 1) * page_size
    end_index = min(start_index + page_size, total_items)
    
    # Generate data for current page
    data = []
    for i in range(start_index, end_index):
        data.append(generate_data_object(i + 1))
    
    return PaginatedResponse(
        data=data,
        total=total_items,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1
    )

@app.get("/api/data-with-date-formats", response_model=PaginatedResponseWithDifferentDates)
async def get_data_with_date_formats(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    total_records: int = Query(1000, ge=1, le=10000, description="Total number of records to generate (1-10000)")
):
    """
    Get paginated data with various date formats.
    
    - **page**: Page number (starts from 1)
    - **page_size**: Number of items per page (1-100)
    - **total_records**: Total number of records to generate (1-10000)
    
    Returns an array of JSON objects with multiple date format variations:
    - **birth_date_iso**: string (ISO format: 2023-12-25)
    - **birth_date_us**: string (US format: 12/25/2023)
    - **birth_date_eu**: string (EU format: 25/12/2023)
    - **birth_date_long**: string (Long format: December 25, 2023)
    - **created_at_iso**: string (ISO datetime: 2023-12-25T10:30:00)
    - **created_at_timestamp**: integer (Unix timestamp: 1703505000)
    - **created_at_readable**: string (Readable: Mon, Dec 25 2023 10:30 AM)
    
    Plus all other data types from the standard API.
    """
    
    # Use user-specified total records
    total_items = total_records
    
    # Calculate pagination
    total_pages = (total_items + page_size - 1) // page_size
    start_index = (page - 1) * page_size
    end_index = min(start_index + page_size, total_items)
    
    # Generate data for current page
    data = []
    for i in range(start_index, end_index):
        data.append(generate_data_object_with_different_dates(i + 1))
    
    return PaginatedResponseWithDifferentDates(
        data=data,
        total=total_items,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1
    )

@app.get("/api/endpoints")
async def get_available_endpoints():
    """Get all available API endpoints with their descriptions."""
    return {
        "endpoints": [
            {
                "path": "/api/data",
                "name": "Standard Data API",
                "description": "Returns JSON objects with standard date formats (ISO) and all common data types including integers, floats, booleans, strings, arrays, and objects.",
                "parameters": [
                    {"name": "page", "type": "integer", "default": 1, "description": "Page number (starts from 1)"},
                    {"name": "page_size", "type": "integer", "default": 10, "description": "Number of items per page (1-100)"},
                    {"name": "total_records", "type": "integer", "default": 1000, "description": "Total number of records to generate (1-10000)"}
                ],
                "example": "/api/data?page=1&page_size=10&total_records=500"
            },
            {
                "path": "/api/data-with-date-formats",
                "name": "Date Formats API",
                "description": "Returns JSON objects with multiple date format variations including ISO, US, EU, long format, timestamps, and readable formats. Perfect for testing different date parsing scenarios.",
                "parameters": [
                    {"name": "page", "type": "integer", "default": 1, "description": "Page number (starts from 1)"},
                    {"name": "page_size", "type": "integer", "default": 10, "description": "Number of items per page (1-100)"},
                    {"name": "total_records", "type": "integer", "default": 1000, "description": "Total number of records to generate (1-10000)"}
                ],
                "example": "/api/data-with-date-formats?page=1&page_size=10&total_records=500",
                "special_fields": [
                    "birth_date_iso (ISO format: 2023-12-25)",
                    "birth_date_us (US format: 12/25/2023)",
                    "birth_date_eu (EU format: 25/12/2023)",
                    "birth_date_long (Long format: December 25, 2023)",
                    "created_at_iso (ISO datetime: 2023-12-25T10:30:00)",
                    "created_at_timestamp (Unix timestamp: 1703505000)",
                    "created_at_readable (Readable: Mon, Dec 25 2023 10:30 AM)"
                ]
            },
            {
                "path": "/api/schema",
                "name": "Schema API",
                "description": "Returns the JSON schema for the data objects, useful for validation and understanding the data structure.",
                "parameters": [],
                "example": "/api/schema"
            }
        ]
    }

@app.get("/api/schema")
async def get_schema():
    """Get the JSON schema for the data objects."""
    return {
        "title": "DataObject Schema",
        "description": "Schema for the JSON objects returned by the API",
        "type": "object",
        "properties": {
            "id": {"type": "integer", "description": "Unique identifier"},
            "uuid": {"type": "string", "format": "uuid", "description": "UUID string"},
            "name": {"type": "string", "description": "User name"},
            "email": {"type": "string", "format": "email", "description": "Email address"},
            "age": {"type": "integer", "minimum": 0, "maximum": 150, "description": "Age in years"},
            "height": {"type": "number", "description": "Height in centimeters"},
            "weight": {"type": "number", "description": "Weight in kilograms"},
            "is_active": {"type": "boolean", "description": "Active status"},
            "balance": {"type": "number", "description": "Account balance"},
            "birth_date": {"type": "string", "format": "date", "description": "Birth date in ISO format"},
            "created_at": {"type": "string", "format": "date-time", "description": "Creation timestamp"},
            "tags": {"type": "array", "items": {"type": "string"}, "description": "Array of tags"},
            "metadata": {"type": "object", "description": "Additional metadata object"},
            "score": {"type": ["number", "null"], "description": "Optional score value"},
            "description": {"type": ["string", "null"], "description": "Optional description"}
        },
        "required": ["id", "uuid", "name", "email", "age", "height", "weight", "is_active", 
                    "balance", "birth_date", "created_at", "tags", "metadata"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
