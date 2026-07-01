print("🚀 Script Starting... Python & Libraries Working!")
import json
from opencage.geocoder import OpenCageGeocode
from timezonefinder import TimezoneFinder
from datetime import datetime, timezone
import os

# Load environment variables from .env file if it exists
if os.path.exists('.env'):
    with open('.env', encoding='utf-8') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key.strip()] = value.strip().strip('\'"')

API_KEY = os.getenv('OPENCAGE_API_KEY')
if not API_KEY:
    raise ValueError("OPENCAGE_API_KEY environment variable is missing.")
geocoder = OpenCageGeocode(API_KEY)


def get_worldwide_address_details(raw_address):
    # 1. Query OpenCage API
    result = geocoder.geocode(raw_address, no_annotations=0, limit=1)
    
    if not result:
        return {"error": "Address not found anywhere in the world. Please check the spelling."}

    location = result[0]
    coords = location['geometry']
    components = location.get('components', {})
    annotations = location.get('annotations', {})
    
    # 2. Calculate Timezone & UTC Offset
    tf = TimezoneFinder()
    tz_str = tf.timezone_at(lng=coords['lng'], lat=coords['lat'])
    
    try:
        from zoneinfo import ZoneInfo # Python 3.9+
        tz = ZoneInfo(tz_str)
        utc_offset = datetime.now(tz).strftime('%z')
        utc_offset = f"{utc_offset[:3]}:{utc_offset[3:]}"
    except Exception:
        utc_offset = "+00:00"
        tz_str = "UTC"

    # 3. Global Fallback Logic for Address Components
    # Different countries use different terms for the same thing
    state = (components.get('state') or 
             components.get('province') or 
             components.get('state_district') or 
             components.get('prefecture') or 
             components.get('region'))
             
    city = (components.get('city') or 
            components.get('town') or 
            components.get('village') or 
            components.get('municipality') or 
            components.get('county'))
            
    district = components.get('county') or components.get('state_district') or city

    # 4. Quality Score & Missing Components Calculation
    required_fields = ['country', 'state', 'city', 'postcode', 'road']
    missing_components = []
    present_count = 0

    # Map our parsed variables to required fields for checking
    parsed_check = {
        'country': components.get('country'),
        'state': state,
        'city': city,
        'postcode': components.get('postcode'),
        'road': components.get('road')
    }

    for field in required_fields:
        if not parsed_check.get(field):
            missing_components.append(field)
        else:
            present_count += 1

    quality_score = int((present_count / len(required_fields)) * 100)
    confidence = 98.0 if quality_score >= 80 else 80.0
    validation_status = "Valid" if quality_score >= 60 else "Partial"

    # 5. Build the Final Standardized JSON
    final_json = {
        "raw_address": raw_address,
        "cleaned_address": location.get('formatted', raw_address),
        "latitude": round(coords['lat'], 6),
        "longitude": round(coords['lng'], 6),
        "country": components.get('country', 'Unknown'),
        "country_code": components.get('country_code', 'Unknown').upper(),
        "continent": annotations.get('continent', 'Unknown'),
        "state": state,
        "district": district,
        "city": city,
        "locality": components.get('suburb') or components.get('neighbourhood') or components.get('city_district'),
        "road": components.get('road'),
        "house_number": components.get('house_number'),
        "postcode": components.get('postcode'),
        "timezone": tz_str,
        "utc_offset": utc_offset,
        "region_type": "Urban" if city else "Rural",
        "area_type": "City" if city else "Town",
        "quality_score": quality_score,
        "validation_status": validation_status,
        "confidence_percentage": confidence,
        "missing_components": missing_components,
        "formatted_address": location.get('formatted', raw_address),
        "ai_parsed": {
            "cleaned_full_address": location.get('formatted', raw_address),
            "currency": annotations.get('currency', {}).get('iso_code', 'Unknown'),
            "calling_code": annotations.get('callingcode', 'Unknown')
        }
    }
    
    return final_json

# --- Test the Code with Worldwide Addresses ---
if __name__ == "__main__":
    # Test 1: India
    # Test 2: USA
    # Test 3: UK
    # Test 4: Japan
    
    test_addresses = [
        "1600 Amphitheatre Parkway, Mountain View, CA", # USA
        "10 Downing St, London SW1A 2AA, UK",           # UK
        "Tokyo Station, 1 Chome Marunouchi, Chiyoda City, Tokyo, Japan" # Japan
    ]
    
    for addr in test_addresses:
        print(f"\n--- Fetching data for: '{addr}' ---")
        output = get_worldwide_address_details(addr)
        print(json.dumps(output, indent=2, ensure_ascii=False))