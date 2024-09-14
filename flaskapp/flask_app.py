from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the saved LabelEncoders and model for 5 years mark model
le_market_segment = joblib.load('le_market_segment.joblib')
le_floor_range = joblib.load('le_floor_range.joblib')
model = joblib.load('best_condo_price_predictor.joblib')
scaler = model.named_steps['scaler']

# Get the mean and standard deviation
means = scaler.mean_
stds = scaler.scale_
print("X Means of features:", means)
print("X Standard deviations of features:", stds)

# Load the saved LabelEncoders and model for 10 years mark model
le_market_segment_10yrs = joblib.load('le_market_segment_10yrs.joblib')
le_floor_range_10yrs = joblib.load('le_floor_range_10yrs.joblib')
model_10yrs = joblib.load('best_condo_price_predictor_10yrs.joblib')
scaler_10yrs = model_10yrs.named_steps['scaler']
# Get the mean and standard deviation
means_10yrs = scaler_10yrs.mean_
stds_10yrs = scaler_10yrs.scale_
print("X Means of features (10 years mark model):", means_10yrs)
print("X Standard deviations of features (10 years mark model):", stds_10yrs)

price_mean, price_std = joblib.load('normalization_params.joblib')
price_mean_10yrs, price_std_10yrs = joblib.load('normalization_params_10yrs.joblib')

def prepare_data_for_inference(market_segment, months_since_contract_date, months_since_commence_date, 
                               area, floor_range):
    if months_since_commence_date - months_since_contract_date  < 119:
        data = {
            'market_segment': [le_market_segment.transform([market_segment])[0]],
            'months_since_contract_date': [months_since_contract_date],
            'months_since_commence_date': [months_since_commence_date],
            'area': [area],
            'floor_range': [le_floor_range.transform([floor_range])[0]],
        }
    else:
        data = {
            'market_segment': [le_market_segment_10yrs.transform([market_segment])[0]],
            'months_since_contract_date': [months_since_contract_date],
            'months_since_commence_date': [months_since_commence_date],
            'area': [area],
            'floor_range': [le_floor_range_10yrs.transform([floor_range])[0]],
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
    if months_since_commence_date - months_since_contract_date  < 119:
        print(f"Using 5 years mark model inference")
        normalized_predicted_price = model.predict(new_data)
        predicted_price = normalized_predicted_price * price_std + price_mean
    else:
        print(f"Using 10 years mark model inference")
        normalized_predicted_price = model_10yrs.predict(new_data)
        predicted_price = normalized_predicted_price * price_std_10yrs + price_mean_10yrs
    
    return jsonify({'predicted_price': predicted_price[0]})


if __name__ == '__main__':
    # app.run(debug=True)
    pass