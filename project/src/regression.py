import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def run_linear_regression(df: pd.DataFrame, features: list = ['open', 'days_sequence'], target: str = 'close', test_size: float = 0.2):
    """
    Runs a linear regression on the specified features and target.
    Prints R² score and Mean Squared Error on the test set.
    Returns: model, prediction
    """
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=False)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("MARK DOWN ASSUMPTION: Linear relation")
    print(f"Test R² score: {r2:.4f}")
    print(f"Test Mean Squared Error: {mse:.4f}")

    return model, y_pred

def run_prediction(model: LinearRegression, features: list, open_price: float, day_sequence: int):
    """
    Uses the trained model to predict the closing price for a given open price and day sequence.
    """
    input_df = pd.DataFrame([{
        'open': open_price,
        'days_sequence': day_sequence
    }])[features]  # Ensure column order and names match training

    prediction = model.predict(input_df)[0]
    print(f"Predicted next close: ${prediction:.2f}")
    return prediction
