# 🌍 Worldwide Address Parser (JSON)

An AI-powered web application and API that parses, validates, and cleanses address inputs from anywhere in the world into a standardized JSON format. It integrates geocoding, AI-driven spelling correction, local postal API queries, and intelligent timezone detection.

---

## 🚀 Features

- **🧠 AI-Powered Address Correction**: Automatically fixes typos, abbreviations, and incomplete text using Groq's Llama 3.1 model.
- **🗺️ Geocoding**: Resolves coordinates (latitude & longitude) and structured location attributes using the OpenCage Geocoder API.
- **✉️ Postal Code Integrations**:
  - Direct integration with the **India Pincode API** for highly accurate details within India.
  - Integration with the **GeoNames Postal Code API** for worldwide postal-level details.
- **⏰ Smart Timezone Detection**: 100% accurate timezone and UTC offset calculation based on geographical rules and coordinates.
- **📊 Quality Score & Validation**: Computes an address quality score, validation status (Valid/Partial), and returns a list of missing components.
- **💻 Minimal Web UI & REST API**: Comes with an interactive frontend template and clean JSON endpoint integrations.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **AI Engine**: Groq SDK (`llama-3.1-8b-instant`)
- **Geocoding APIs**: OpenCage API, GeoNames API, Postal Pincode API (India)
- **Timezones**: ZoneInfo, datetime

---

## 📦 Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/RAMAN23-stack/Worldwide-Address-Parser-JSON-.git
   cd Worldwide-Address-Parser-JSON-
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure you have `Flask`, `groq`, `opencage`, `requests`, and `timezonefinder` installed)*

4. **Configure Environment Variables**:
   Create a file named `.env` in the root directory:
   ```env
   OPENCAGE_API_KEY=your_opencage_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```
   *(Note: The `.env` file is excluded in `.gitignore` to keep credentials secure)*

---

## 🚦 Running the Application

Start the Flask development server:
```bash
python app.py
```

The application will start running at:
`http://127.0.0.1:5000/`

---

## 🔌 API Documentation

### 1. Web UI Interface
- **Route**: `GET /`
- **Description**: Renders the frontend interface to type in addresses and submit them.

### 2. URL-based Address Parsing
- **Route**: `GET /<address>`
- **Example**: `GET http://127.0.0.1:5000/10 Downing St, London`
- **Response**: Returns a JSON representation of the address components.

### 3. Search POST Endpoint
- **Route**: `POST /search`
- **Form Data**: `address=<your address text>`
- **Response**: Standardized JSON details.

### Example JSON Output
```json
{
  "raw_address": "10 Downing St, London",
  "ai_corrected_address": "10 Downing St, London",
  "cleaned_address": "10 Downing Street, London SW1A 2AA, United Kingdom",
  "latitude": 51.503364,
  "longitude": -0.127625,
  "country": "United Kingdom",
  "country_code": "GB",
  "continent": "Europe",
  "state": "England",
  "district": "Greater London",
  "city": "London",
  "locality": "Westminster",
  "road": "Downing Street",
  "house_number": "10",
  "postcode": "SW1A 2AA",
  "timezone": "Europe/London",
  "utc_offset": "+01:00",
  "region_type": "Urban",
  "area_type": "City",
  "quality_score": 100,
  "validation_status": "Valid",
  "confidence_percentage": 98.0,
  "missing_components": [],
  "formatted_address": "10 Downing Street, London SW1A 2AA, United Kingdom",
  "ai_parsed": {
    "cleaned_full_address": "10 Downing Street, London SW1A 2AA, United Kingdom",
    "currency": "GBP",
    "calling_code": "44"
  }
}
```
