import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import MACD
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import mean_squared_error, r2_score

# Define the Bayesian LSTM model in PyTorch
class BayesianLSTM(nn.Module):
    def __init__(self, units, output_size, features, dropout_rate=0.5):
        super(BayesianLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size=features, hidden_size=units, batch_first=True)
        self.fc1 = nn.Linear(units, units)
        self.dropout = nn.Dropout(dropout_rate)
        self.fc2 = nn.Linear(units, output_size)
        self.relu = nn.ReLU()

    def forward(self, x, training=False):
        lstm_out, _ = self.lstm(x)
        lstm_out = lstm_out[:, -1, :]  # Take the last timestep's output
        x = self.relu(self.fc1(lstm_out))
        if training:
            x = self.dropout(x)
        x = self.fc2(x)
        return x

    def predict_with_dropout(self, x, n_samples=100):
        self.train()  # Set model to training mode to enable dropout
        with torch.no_grad():
            predictions = torch.stack([self(x, training=True) for _ in range(n_samples)])
        return predictions.numpy()

# Function to plot results
def plot_ticker_results(y_test, predictions, ticker):
    mean_predictions = predictions.mean(axis=0)
    std_predictions = predictions.std(axis=0)
    
    lower_bound = (mean_predictions - std_predictions).squeeze()
    upper_bound = (mean_predictions + std_predictions).squeeze()

    plt.figure(figsize=(14, 7))
    plt.plot(y_test, label='Actual')
    plt.plot(mean_predictions.squeeze(), label='Predicted')
    plt.fill_between(range(len(y_test)), lower_bound, upper_bound, color='orange', alpha=0.3, label='Uncertainty')
    plt.title(f'Actual vs Predicted Values with Uncertainty for {ticker}')
    plt.xlabel('Time Step')
    plt.ylabel('Target Variable')
    plt.legend()
    plt.show()

# Download and process data
setTicker = ['JASMY-USD', 'ENS-USD', 'BNB-USD', 'SOL-USD', 'MSTR', 'BTC-USD', 'ETH-USD']
dataframes = []

for ticker in setTicker:
    df = yf.download(ticker, start="2020-01-01", end="2023-12-31")
    print(df)
    df = df.dropna()
    # df['RSI'] = RSIIndicator(df['Close']).rsi()
    indicator_bb = BollingerBands(df['Close'])
    # df['BB_MAVG'] = indicator_bb.bollinger_mavg()
    # df['BB_HBAND'] = indicator_bb.bollinger_hband()
    # df['BB_LBAND'] = indicator_bb.bollinger_lband()
    df['Prev Close'] = df['Close'].shift(1)
    df = df.dropna()
    df['Ticker'] = ticker
    dataframes.append(df)

# Process each ticker
for ticker_df in dataframes:
    ticker = ticker_df['Ticker'].iloc[0]
    print(f"Processing {ticker}")
#  'RSI',, 'BB_MAVG', 'BB_HBAND', 'BB_LBAND', 'MACD'
    feature_names = ['Prev Close', 'Open', 'High', 'Low']
    X = ticker_df[feature_names].values
    y = ticker_df['Close'].values  

    timesteps = 10
    X_lstm = np.array([X[i - timesteps:i, :] for i in range(timesteps, len(X))])
    y_lstm = y[timesteps:]

    X_train, X_test, y_train, y_test = train_test_split(X_lstm, y_lstm, test_size=0.2, random_state=42)

    # Convert to PyTorch tensors
    X_train = torch.tensor(X_train, dtype=torch.float32)
    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
    y_test = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

    # Create DataLoader
    train_dataset = TensorDataset(X_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    # Initialize model, loss, and optimizer
    units = 50
    output_size = 1
    features = len(feature_names)
    model = BayesianLSTM(units=units, output_size=output_size, features=features)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters())

    # Training loop
    epochs = 100
    for epoch in range(epochs):
        model.train()
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_X, training=True)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()

    # Predict with dropout
    model.eval()
    predictions = model.predict_with_dropout(X_test, n_samples=10)

    # Align y_test with predictions
    if len(y_test) > len(predictions.mean(axis=0)):
        y_test = y_test[-len(predictions.mean(axis=0)):]

    # Plot results
    plot_ticker_results(y_test.numpy(), predictions, ticker)

    # Calculate metrics
    mean_predictions = predictions.mean(axis=0)
    r2 = r2_score(y_test.numpy(), mean_predictions)
    rmse = np.sqrt(mean_squared_error(y_test.numpy(), mean_predictions))
    print(f"R-squared (R²): {r2}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")