#!/usr/bin/env python3
"""
Simple test script to verify the API endpoints work correctly.
"""

import requests
import json
import sys

def test_api():
    """Test the API endpoints."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing HTTP Data Serve API...")
    print("=" * 50)
    
    try:
        # Test the main data endpoint with custom total records
        print("📊 Testing /api/data endpoint with custom total records...")
        response = requests.get(f"{base_url}/api/data?page=1&page_size=3&total_records=100")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"✅ Total items: {data['total']}")
            print(f"✅ Items returned: {len(data['data'])}")
            print(f"✅ Current page: {data['page']}")
            print(f"✅ Total pages: {data['total_pages']}")
            
            # Verify data structure
            if data['data']:
                first_item = data['data'][0]
                required_fields = ['id', 'uuid', 'name', 'email', 'age', 'height', 
                                 'weight', 'is_active', 'balance', 'birth_date', 
                                 'created_at', 'tags', 'metadata']
                
                missing_fields = [field for field in required_fields if field not in first_item]
                if not missing_fields:
                    print("✅ Data structure is correct")
                else:
                    print(f"❌ Missing fields: {missing_fields}")
                
                # Check data types
                print("\n🔍 Data type verification:")
                print(f"   id: {type(first_item['id']).__name__}")
                print(f"   uuid: {type(first_item['uuid']).__name__}")
                print(f"   name: {type(first_item['name']).__name__}")
                print(f"   email: {type(first_item['email']).__name__}")
                print(f"   age: {type(first_item['age']).__name__}")
                print(f"   height: {type(first_item['height']).__name__}")
                print(f"   weight: {type(first_item['weight']).__name__}")
                print(f"   is_active: {type(first_item['is_active']).__name__}")
                print(f"   balance: {type(first_item['balance']).__name__}")
                print(f"   tags: {type(first_item['tags']).__name__}")
                print(f"   metadata: {type(first_item['metadata']).__name__}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"❌ Response: {response.text}")
            return False
            
        print("\n" + "=" * 50)
        
        # Test the schema endpoint
        print("📋 Testing /api/schema endpoint...")
        schema_response = requests.get(f"{base_url}/api/schema")
        
        if schema_response.status_code == 200:
            schema = schema_response.json()
            print(f"✅ Status: {schema_response.status_code}")
            print(f"✅ Schema title: {schema.get('title', 'N/A')}")
            print(f"✅ Properties count: {len(schema.get('properties', {}))}")
        else:
            print(f"❌ Schema endpoint failed with status: {schema_response.status_code}")
            
        print("\n" + "=" * 50)
        
        # Test the date formats endpoint
        print("🗓️ Testing /api/data-with-date-formats endpoint...")
        date_response = requests.get(f"{base_url}/api/data-with-date-formats?page=1&page_size=2&total_records=50")
        
        if date_response.status_code == 200:
            date_data = date_response.json()
            print(f"✅ Status: {date_response.status_code}")
            print(f"✅ Total items: {date_data['total']}")
            print(f"✅ Items returned: {len(date_data['data'])}")
            
            # Verify date formats
            if date_data['data']:
                first_item = date_data['data'][0]
                date_fields = ['birth_date_iso', 'birth_date_us', 'birth_date_eu', 'birth_date_long',
                             'created_at_iso', 'created_at_timestamp', 'created_at_readable']
                
                missing_date_fields = [field for field in date_fields if field not in first_item]
                if not missing_date_fields:
                    print("✅ All date format fields present")
                    print(f"✅ Sample formats:")
                    print(f"   ISO: {first_item['birth_date_iso']}")
                    print(f"   US: {first_item['birth_date_us']}")
                    print(f"   EU: {first_item['birth_date_eu']}")
                    print(f"   Long: {first_item['birth_date_long']}")
                    print(f"   Timestamp: {first_item['created_at_timestamp']}")
                else:
                    print(f"❌ Missing date fields: {missing_date_fields}")
        else:
            print(f"❌ Date formats endpoint failed with status: {date_response.status_code}")
            
        print("\n" + "=" * 50)
        
        # Test pagination
        print("📄 Testing pagination...")
        page2_response = requests.get(f"{base_url}/api/data?page=2&page_size=5&total_records=200")
        
        if page2_response.status_code == 200:
            page2_data = page2_response.json()
            print(f"✅ Page 2 status: {page2_response.status_code}")
            print(f"✅ Page 2 items: {len(page2_data['data'])}")
            print(f"✅ Total records: {page2_data['total']}")
            print(f"✅ Has previous: {page2_data['has_previous']}")
            print(f"✅ Has next: {page2_data['has_next']}")
        else:
            print(f"❌ Pagination test failed with status: {page2_response.status_code}")
            
        print("\n🎉 All tests completed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the API server.")
        print("💡 Make sure the server is running: python run.py")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
