from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the saved LabelEncoders and model
le_market_segment = joblib.load('le_market_segment.joblib')
le_floor_range = joblib.load('le_floor_range.joblib')
model = joblib.load('best_condo_price_predictor.joblib')
price_mean, price_std = joblib.load('normalization_params.joblib')

def prepare_data_for_inference(market_segment, months_since_contract_date, months_since_commence_date, 
                               area, floor_range):
    data = {
        'market_segment': [le_market_segment.transform([market_segment])[0]],
        'months_since_contract_date': [months_since_contract_date],
        'months_since_commence_date': [months_since_commence_date],
        'area': [area],
        'floor_range': [le_floor_range.transform([floor_range])[0]],
    }
    return pd.DataFrame(data)

@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from request
    data = request.json
    market_segment = data['market_segment']
    months_since_contract_date = data['months_since_contract_date']
    months_since_commence_date = data['months_since_commence_date']
    area = data['area']
    floor_range = data['floor_range']
    
    # Prepare data for inference
    new_data = prepare_data_for_inference(market_segment, months_since_contract_date, 
                                          months_since_commence_date, area, floor_range)
    
    # Make prediction
    normalized_predicted_price = model.predict(new_data)
    predicted_price = normalized_predicted_price * price_std + price_mean
    
    return jsonify({'predicted_price': predicted_price[0]})

if __name__ == '__main__':
    pass