# Real-Time Asset Management in Simulated Trading Platform & Predictive Analytics

Simulated Trading Platform is a simulation trading platform that enables users to create an account, log in, manage their assets and funds, and execute simulated buy/sell transactions using USD. The platform includes both a backend service (powered by Python FastAPI and PostgreSQL) and a frontend application (using Vue.js).

Additionally, there's an experimental Python function for crypto price prediction included in the repository, although it is not integrated into the deployed application at this time.

## Overview

| **Real-Time Asset Management in Simulated Trading Platform** | **Predictive Analytics (Experimental)** |
| ------------------------------------------------------------------ | ----------------------------------------- |
| This integrated platform combines simulated trading with real-time asset management. Users can create accounts, log in, monitor balances, execute simulated buy/sell transactions, and manage assets—with immediate updates and detailed asset information views. Deposits and withdrawals in USD are processed in real time to ensure consistent portfolio tracking. | This optional experimental module includes a Python function for cryptocurrency price prediction. It outputs key statistical metrics (e.g., R-squared and RMSE) for the prediction of various crypto assets. Although not part of the live trading system, it provides a sandbox for running prediction scripts locally and exploring alternative trading strategies. |


## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#usage)
  - [User Flow & Routes](#user-flow--routes)
- [Database Configuration](#database-configuration)
- [Project Structure](#project-structure)
- [Additional Predictive Analytics (Experimental)](#additional-predictive-analytics-experimental)

## Features

- **Authentication:** User creation and login on the landing page (`/`).
- **Asset Management:**  
  - View detailed asset information on `/assets`, including deposit and withdrawal management using USD.
  - Browse and create new assets (using Yahoo Finance labels) on `/all-assets`.
- **Trading Simulation:**  
  - Access detailed asset pages to enter specific buy/sell amounts (buying/selling assets using USD).
  - View transaction details on `/transacts`.
- **Backend & Frontend Integration:** Easy local development using virtual environments and integrated PostgreSQL database configuration.

## Installation

### Prerequisites

- Python 3.12.2
- Node.js and npm
- PostgreSQL (Ensure you have it installed and a database created)
- Internet connection (for real time data in yfinance)

### Virtual Environment and Dependency Installation

You can choose your preferred virtual environment tool (such as `venv`, `virtualenv`, or `conda`). For example, with Python's built-in `venv`:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

### Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd trading/backend
   ```

2. Run the main backend application:

   ```bash
   python main.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd trading/frontend/trading-platform
   ```

2. Install npm packages and start the development server:

   ```bash
   npm install
   npm run dev
   ```

## Usage

### User Flow & Routes

- **Login & User Creation (`/`):**  
  The root page serves as the login page. Here, new users can register and existing users can log in.
  ![image](https://github.com/user-attachments/assets/e8ff2ac5-20e7-4590-861c-ec82f5f37ae9)
  ![image](https://github.com/user-attachments/assets/f486ed07-0b76-4d59-a0ab-befb411d5f0e)



- **User Asset Details (`/assets`):**  
  After logging in, users can view their asset details. This page also provides functionality to manage funds via deposit and withdrawal options (in USD).
![Screenshot 2025-02-05 201347](https://github.com/user-attachments/assets/0b591b90-84bc-43ee-a702-4c9d5548ee29)
![Screenshot 2025-02-05 201409](https://github.com/user-attachments/assets/5aa99a0d-fea4-44b1-b5e9-e5a1feb6e895)

- **View & Create Assets (`/all-assets`):**  
  Users can view all available assets on the platform. Additionally, there's an option to create a new asset by entering a label from Yahoo Finance.
![image](https://github.com/user-attachments/assets/0010f8f2-5f00-499d-bfbb-79278fd2b1f5)
![image](https://github.com/user-attachments/assets/85cd126e-7018-4f9e-bf65-61d9fbe4a189)


- **Asset Transaction: (`/all-assets/:id`):**  
  Users can click on an asset to view its details, where they can specify an amount to buy or sell the asset using USD.  
![Screenshot 2025-02-05 201532](https://github.com/user-attachments/assets/9555c5ec-fe23-4475-8ee3-56333d147d50)

- **Transaction History (`/transacts`):**  
  Post any transaction, users can check the transaction history and details on the `/transacts` route.
 ![Screenshot 2025-02-05 201227](https://github.com/user-attachments/assets/2a8807bb-acd5-4f67-9a3b-bba5ecac1a8b)

## Database Configuration

Before running the backend, ensure you have PostgreSQL installed and configured. Update the `SQLALCHEMY_DATABASE_URL` in `database.py` file with your PostgreSQL connection string:

```python
# Example: postgresql://user:password@postgresserver/dbname
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/dbname"
# noramlly Postgresql 16/17 =localhost:5432/localhost:5433
```

Make sure to create your PostgreSQL database(dbname) as referenced in the URL.

## Project Structure

```
trading
├── Prediction
├── backend
│   ├── routers
│   │   └── __pycache__
│   ├── schemas
│   │   └── __pycache__
│   ├── services
│   │   └── __pycache__
│   ├── utils
│   │   └── __pycache__
│   └── __pycache__
└── frontend
    └── trading-platform
        ├── .vscode
        ├── node_modules
        │   └── (dependencies and binaries)
        ├── public
        └── src
            ├── api
            ├── assets
            ├── components
            ├── router
            ├── store
            └── views
```

- **Backend:** Contains Python modules for routing, data schemas, services, and utility functions for the trading simulation and asset management.
- **Frontend:** Houses the trading platform’s client-side code with components, routing, state management, and views for user interaction.
- **Prediction** Contains Python modules for experimental price prediction function
---

## Additional Predictive Analytics (Experimental)

An experimental crypto price prediction function is available in the repository. Although it's not integrated into the deployed application, you can try it out locally by following these steps:

1. Navigate to the `Prediction` folder.
   ```bash
   cd trading/Prediction
   ```
3. Install the additional dependencies by running (please also install the requirements.txt):
    
    ```bash
    pip install -r additional_requirements.txt
    
    ```
    
4. Run the prediction script:
    
    ```bash
    python Crypto.py
    
    ```
    

By default, the script uses the following tickers:

```python
setTicker = ['JASMY-USD', 'ENS-USD', 'BNB-USD', 'SOL-USD', 'MSTR', 'BTC-USD', 'ETH-USD']

```

You can modify this list to predict for different cryptocurrencies. For example, the output might look like this:

```
Processing JASMY-USD
R-squared (R²): 0.9646150469779968
Root Mean Squared Error (RMSE): 0.0975302741995915
Processing ENS-USD
R-squared (R²): 0.9369181394577026
Root Mean Squared Error (RMSE): 2.4010781528792706
Processing BNB-USD
R-squared (R²): 0.9241467714309692
Root Mean Squared Error (RMSE): 44.71335844944019
Processing SOL-USD
R-squared (R²): 0.9618353247642517
Root Mean Squared Error (RMSE): 10.774511736009853
Processing MSTR
R-squared (R²): 0.9533594846725464
Root Mean Squared Error (RMSE): 4.585159469709957
Processing BTC-USD
R-squared (R²): -2.3547894954681396
Root Mean Squared Error (RMSE): 28065.625950617956
Processing ETH-USD
R-squared (R²): 0.6672559976577759
Root Mean Squared Error (RMSE): 641.7567198713232

```

![Screenshot 2025-02-06 002945](https://github.com/user-attachments/assets/dadcc5c4-5c28-47a0-a268-b95f53e91f8b)


Feel free to adjust the `setTicker` list in `Crypto.py` to test with other crypto assets.

---
