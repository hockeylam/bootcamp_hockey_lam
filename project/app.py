from flask import Flask, request, render_template
import joblib
import os
from src.regression import run_prediction

app = Flask(__name__)

model_path = os.path.join(os.path.dirname(__file__), 'model', 'linear_model.pkl')
model = joblib.load(model_path)

features = ['open', 'days_sequence']

latest_day_sequence = 471 #check what number the last entry was when training model
                          #for this specific model the last entry was 470

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None

    if request.method == 'POST':
        open_price = request.form.get('open_price')
        if open_price:
            try:
                prediction = run_prediction(
                    model,
                    features=features,
                    open_price=float(open_price),
                    day_sequence=latest_day_sequence
                )
            except Exception as e:
                prediction = f"Error: {str(e)}"

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)