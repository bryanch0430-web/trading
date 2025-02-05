# Simulated Trading Platform

Simulated Trading Platform is a simulation trading platform that enables users to create an account, log in, manage their assets and funds, and execute simulated buy/sell transactions using USD. The platform includes both a backend service (powered by Python FastAPI and PostgreSQL) and a frontend application (using Vue.js).

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
![image](https://github.com/user-attachments/assets/769a6253-daf3-4adb-ab58-1d97a52a313f)
![image](https://github.com/user-attachments/assets/86f5c764-58ae-4926-9465-f02c23d09f43)


- **User Asset Details (`/assets`):**  
  After logging in, users can view their asset details. This page also provides functionality to manage funds via deposit and withdrawal options (in USD).
![Screenshot 2025-02-05 201347](https://github.com/user-attachments/assets/0b591b90-84bc-43ee-a702-4c9d5548ee29)
![Screenshot 2025-02-05 201409](https://github.com/user-attachments/assets/5aa99a0d-fea4-44b1-b5e9-e5a1feb6e895)

- **View & Create Assets (`/all-assets`):**  
  Users can view all available assets on the platform. Additionally, there's an option to create a new asset by entering a label from Yahoo Finance.
![Screenshot 2025-02-05 201431](https://github.com/user-attachments/assets/eb03e745-88a3-450b-8420-ecef1bd59f5c)

- **Asset Transaction:**  
  Users can click on an asset to view its details, where they can specify an amount to buy or sell the asset using USD.  
![Screenshot 2025-02-05 201511](https://github.com/user-attachments/assets/24075609-ff29-4386-97c1-1c7943eece4f)

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

- **Backend:** Contains Python modules for routing, data schemas, services, and utility functions for the trading simulation.
- **Frontend:** Houses the trading platform’s client-side code with components, routing, state management, and views for user interaction.

