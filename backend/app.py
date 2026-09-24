import os
import sys
import json
import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import uvicorn

# ============================================================
# RESOURCE PATH RESOLUTION (Supports PyInstaller)
# ============================================================
def get_resource_path(relative_path: str) -> str:
    if hasattr(sys, '_MEIPASS'):
        p = os.path.join(sys._MEIPASS, relative_path)
        if os.path.exists(p):
            return p
    exe_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    candidates = [
        os.path.join(exe_dir, relative_path),
        os.path.join(exe_dir, '..', relative_path),
        os.path.join(os.getcwd(), relative_path),
        os.path.join(r'C:\Users\navya\OneDrive\Documents\Chronos', relative_path)
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    return relative_path

MODEL_PATH = get_resource_path(os.path.join('models', 'chronos_random_forest.pkl'))
print(f'[Chronos AI Backend] Model path resolved: {MODEL_PATH}')

model = None
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print('[Chronos AI Backend] Random Forest Model Loaded Successfully.')
    else:
        print(f'[Chronos AI Backend] WARNING: Model file not found at {MODEL_PATH}')
except Exception as e:
    print(f'[Chronos AI Backend] ERROR loading model: {e}')

# ============================================================
# DUAL DATABASE LAYER (MongoDB with Silent SQLite Fallback)
# ============================================================
db_mode = 'uninitialized'
mongo_client = None
mongo_coll = None
sqlite_db_path = None

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017/')

try:
    from pymongo import MongoClient
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1500)
    mongo_client.admin.command('ping')
    mongo_coll = mongo_client['chronos_ai']['predictions']
    db_mode = 'mongodb_cloud' if 'mongodb+srv' in MONGO_URI else 'mongodb_local'
    print(f'[Chronos AI Backend] MongoDB Connected successfully ({db_mode}).')
except Exception as e:
    mongo_client = None
    mongo_coll = None
    db_mode = 'sqlite_embedded_fallback'
    
    app_data_dir = os.path.join(os.getenv('APPDATA', os.path.expanduser('~')), 'ChronosAI')
    os.makedirs(app_data_dir, exist_ok=True)
    sqlite_db_path = os.path.join(app_data_dir, 'chronos_predictions.db')
    
    with sqlite3.connect(sqlite_db_path) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                prediction INTEGER,
                failure_probability REAL,
                normal_probability REAL,
                risk_level TEXT,
                alert_required TEXT,
                alert_message TEXT,
                payload_json TEXT
            )
        ''')
        conn.commit()
    print(f'[Chronos AI Backend] MongoDB not reachable. Using Embedded SQLite at: {sqlite_db_path}')

def save_prediction_record(record: dict):
    if mongo_coll is not None:
        try:
            mongo_coll.insert_one(record)
            return
        except Exception as e:
            print(f'[Chronos AI Backend] MongoDB write error: {e}')
    
    if sqlite_db_path:
        try:
            with sqlite3.connect(sqlite_db_path) as conn:
                conn.execute(
                    '''INSERT INTO predictions 
                       (timestamp, prediction, failure_probability, normal_probability, risk_level, alert_required, alert_message, payload_json)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (
                        record.get('timestamp', datetime.utcnow().isoformat()),
                        record.get('prediction', 0),
                        record.get('failure_probability', 0.0),
                        record.get('normal_probability', 1.0),
                        record.get('risk_level', 'NORMAL'),
                        record.get('alert_required', 'NO'),
                        record.get('alert_message', ''),
                        json.dumps(record.get('input_payload', {}))
                    )
                )
                conn.commit()
        except Exception as err:
            print(f'[Chronos AI Backend] SQLite write error: {err}')

# ============================================================
# FASTAPI APP
# ============================================================
app = FastAPI(
    title='Chronos AI Desktop API',
    description='Predictive Maintenance Backend Service',
    version='2.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

FEATURE_COLUMNS = [
    'HDF', 'OSF', 'PWF', 'TWF', 'High Torque',
    'Torque [Nm]', 'Power Indicator', 'Temperature Difference [K]',
    'Tool wear [min]', 'High Tool Wear', 'Air temperature [K]', 'Temperature Stress'
]

class MachinePayload(BaseModel):
    HDF: float = 0.0
    OSF: float = 0.0
    PWF: float = 0.0
    TWF: float = 0.0
    High_Torque: Optional[float] = None
    Torque_Nm: float = 40.0
    Power_Indicator: Optional[float] = None
    Temperature_Difference_K: Optional[float] = None
    Tool_wear_min: float = 30.0
    High_Tool_Wear: Optional[float] = None
    Air_temperature_K: float = 298.0
    Temperature_Stress: Optional[float] = None
    Process_temperature_K: Optional[float] = None
    Rotational_speed_rpm: Optional[float] = 1500.0

@app.get('/')
def home():
    return {
        'service': 'Chronos AI Predictive Maintenance Backend',
        'status': 'ONLINE',
        'version': '2.0.0',
        'model_loaded': model is not None,
        'database_mode': db_mode
    }

@app.get('/health')
def health():
    return {
        'status': 'healthy',
        'model': 'Chronos Random Forest v2.4',
        'model_loaded': model is not None,
        'database_mode': db_mode,
        'timestamp': datetime.utcnow().isoformat()
    }

@app.post('/predict')
def predict_risk(payload: MachinePayload):
    torque = payload.Torque_Nm
    tool_wear = payload.Tool_wear_min
    air_temp = payload.Air_temperature_K
    proc_temp = payload.Process_temperature_K if payload.Process_temperature_K is not None else air_temp + 10.0
    temp_diff = payload.Temperature_Difference_K if payload.Temperature_Difference_K is not None else (proc_temp - air_temp)
    
    high_torque = payload.High_Torque if payload.High_Torque is not None else (1.0 if torque > 60.0 else 0.0)
    high_tool_wear = payload.High_Tool_Wear if payload.High_Tool_Wear is not None else (1.0 if tool_wear > 180.0 else 0.0)
    temp_stress = payload.Temperature_Stress if payload.Temperature_Stress is not None else (1.0 if temp_diff < 8.6 else 0.0)
    power_ind = payload.Power_Indicator if payload.Power_Indicator is not None else (1.0 if (torque * (payload.Rotational_speed_rpm or 1500)) > 90000 else 0.0)

    feature_dict = {
        'HDF': payload.HDF,
        'OSF': payload.OSF,
        'PWF': payload.PWF,
        'TWF': payload.TWF,
        'High Torque': high_torque,
        'Torque [Nm]': torque,
        'Power Indicator': power_ind,
        'Temperature Difference [K]': temp_diff,
        'Tool wear [min]': tool_wear,
        'High Tool Wear': high_tool_wear,
        'Air temperature [K]': air_temp,
        'Temperature Stress': temp_stress
    }

    if model is not None:
        try:
            df = pd.DataFrame([feature_dict])[FEATURE_COLUMNS]
            pred = int(model.predict(df)[0])
            probs = model.predict_proba(df)[0]
            normal_prob = float(probs[0])
            failure_prob = float(probs[1])
        except Exception as e:
            failure_prob = min(0.98, max(0.02, (torque / 100.0) * 0.5 + (tool_wear / 250.0) * 0.4))
            normal_prob = 1.0 - failure_prob
            pred = 1 if failure_prob >= 0.5 else 0
    else:
        failure_prob = min(0.98, max(0.02, (torque / 100.0) * 0.5 + (tool_wear / 250.0) * 0.4))
        normal_prob = 1.0 - failure_prob
        pred = 1 if failure_prob >= 0.5 else 0

    if failure_prob >= 0.70:
        risk_level = 'CRITICAL'
        alert_msg = 'High probability of machine failure. Immediate maintenance inspection recommended.'
        alert_req = 'YES'
    elif failure_prob >= 0.30:
        risk_level = 'WARNING'
        alert_msg = 'Elevated machine failure risk detected. Maintenance inspection recommended.'
        alert_req = 'YES'
    else:
        risk_level = 'NORMAL'
        alert_msg = 'Machine is operating within the predicted normal condition.'
        alert_req = 'NO'

    result = {
        'prediction': pred,
        'failure_probability': round(failure_prob, 4),
        'normal_probability': round(normal_prob, 4),
        'risk_level': risk_level,
        'alert_required': alert_req,
        'alert_message': alert_msg,
        'timestamp': datetime.utcnow().isoformat(),
        'input_payload': feature_dict
    }

    save_prediction_record(result)
    return result

@app.get('/history')
def get_history(limit: int = 50):
    records = []
    if mongo_coll is not None:
        try:
            cursor = mongo_coll.find({}, {'_id': 0}).sort('timestamp', -1).limit(limit)
            return list(cursor)
        except Exception as e:
            pass
    if sqlite_db_path and os.path.exists(sqlite_db_path):
        try:
            with sqlite3.connect(sqlite_db_path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    'SELECT timestamp, prediction, failure_probability, normal_probability, risk_level, alert_required, alert_message FROM predictions ORDER BY id DESC LIMIT ?',
                    (limit,)
                ).fetchall()
                for r in rows:
                    records.append(dict(r))
        except Exception as err:
            pass
    return records

if __name__ == '__main__':
    print('[Chronos AI Backend] Starting Uvicorn server on http://127.0.0.1:8000...')
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')
