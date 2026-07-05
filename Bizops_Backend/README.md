# Business Data Integration and Analysis Backend

## Project Overview
This backend provides a comprehensive solution for business data integration, opportunity analysis, and API serving using Python, Flask, and machine learning technologies.

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Installation

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd <project-directory>
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### Required Dependencies
- Flask
- Flask-CORS
- scikit-learn
- XGBoost
- joblib
- folium
- pandas
- google-cloud-bigquery
- db-dtypes
- google-cloud-bigquery-storage

## Project Structure
- `bizOps_Model.py`: Machine learning model training script
- `app.py`: Flask API server
- `Map_Data_Integration.py`: Data integration script (in development)

## Running the Scripts

### 1. Model Training
Trains the Opportunity Analyzer Machine Learning Model:
```bash
python bizOps_Model.py
```

### 2. Start API Server
Launches the Flask API with React UI integration:
```bash
python app.py
```

## Data Integration Process
The `Map_Data_Integration.py` script is currently in development and will be used for consolidating and preprocessing business data in future iterations.

## Google Cloud BigQuery Setup
Ensure you have:
- Configured Google Cloud credentials
- Set up BigQuery project and dataset
- Placed credentials JSON in the appropriate location

## Environment Variables
Create a `.env` file in the project root and add:
```
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json
```

## Troubleshooting
- Verify all dependencies are correctly installed
- Check Google Cloud credentials
- Ensure Python version compatibility

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
[Specify your license here]

## Contact
[Your contact information or project maintainer details]
```

I've made the following changes:
- Kept `Map_Data_Integration.py` in the project structure
- Added a note about it being in development
- Removed the specific run command for that script
- Maintained the overall structure and clarity of the README

Is this more in line with what you were looking for?