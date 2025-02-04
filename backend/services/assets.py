from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.assets import AssetDetails,AssetCreate,UserAssetDisplayResponse, ListUserAssetDisplayResponse
from model import Asset, UserAsset
from typing import List, Optional
import pandas as pd
import yfinance as yf
import logging
import time
import uuid
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AssetService:
    def __init__(self, db: Session):
            self.db = db

    def create_asset(self, asset: AssetCreate):

        try:

            stock = yf.Ticker(asset.label)  
            info = stock.info

        except Exception as e:
            raise ValueError(f"Could not retrieve data from yfinance for {asset.label}. Error: {e}")
        

        existing_asset = self.get_asset_by_label(asset.label)
        if existing_asset:
            raise ValueError(f"asset alraeady exit")
        if '-USD' in asset.label:  
            asset_type = 'crypto'
        elif info.get('quoteType') == 'EQUITY':  
            asset_type = 'stock'
        elif info.get('quoteType') == 'ETF': 
            asset_type = 'etf'
        elif info.get('quoteType') == 'MUTUALFUND':  
            asset_type = 'mutual_fund'
        else:
            asset_type = 'other' 

        name = info.get('shortName') or info.get('longName') or asset.label
        db_asset = Asset(
            name=name,
            asset_type=asset_type,
            label =asset.label
        )
        self.db.add(db_asset)
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset

    def get_asset_by_id(self, asset_id: int):
        return self.db.query(Asset).filter(Asset.id == asset_id).first()
    def get_asset_price(self, asset_id: int) -> AssetDetails:
        asset = self.db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            raise ValueError("Asset not found.")
        try:
            stock = yf.Ticker(asset.label) 
            data = stock.history()
            info = stock.info
            print(data)
        
        except Exception as e:
            raise ValueError(f"Could not retrieve data from yfinance for {asset.name}. Error: {e}")
        
        asset_details = AssetDetails(
            asset_id=asset_id,
            name=asset.label,
            current_price=data['Close'].iloc[-1],
            previous_close=info.get("previousClose"),
            open_price=info.get("open"),
            day_high=info.get("dayHigh"),
            day_low=info.get("dayLow"),
            market_cap=info.get("marketCap"),
            volume=info.get("volume"),
            currency=info.get("currency"),
            sector=info.get("sector"),
            industry=info.get("industry"),
        )

        return asset_details

    def get_asset_by_name(self, name: str) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.name == name).first()
    def get_asset_by_label(self, label: str) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.label == label).first()
    def get_user_asset(self, user_id: uuid.UUID) -> Optional[List[UserAssetDisplayResponse]]:
        query = (
            self.db.query(UserAsset, Asset)
            .join(Asset, UserAsset.asset_id == Asset.id)
            .filter(UserAsset.user_id == user_id)
            .all()
        )

        if not query:
            return None

        assets = [
            UserAssetDisplayResponse(
                asset_id=ua.asset_id,
                name=asset.name,
                amount=ua.total_value,
                average_price=ua.average_price,
            )
            for ua, asset in query
        ]
        return ListUserAssetDisplayResponse(response=assets)
    
    
    def list_all_asset(self)-> Optional[Asset]:
         return self.db.query(Asset).all()
        
    def calculate_asset_type_distribution(db: Session, user_id: uuid.UUID) -> Optional[UserAssetTypeDistribution]:

        try:
            user_assets = db.query(UserAsset).filter(UserAsset.user_id == user_id).all()
            if not user_assets:
                logger.info(f"No assets found for user {user_id}.")
                return None

            asset_type_values = {}
            total_portfolio_value = 0.0

            for user_asset in user_assets:
                asset = db.query(Asset).filter(Asset.id == user_asset.asset_id).first()
                if not asset:
                    logger.warning(f"Asset with ID {user_asset.asset_id} not found in the database.")
                    continue

                try:
                    ticker = yf.Ticker(asset.label)
                    history = ticker.history(period="1d")
                    if history.empty:
                        logger.warning(f"No price data found for asset {asset.label}.")
                        continue

                    current_price = history['Close'].iloc[-1]
                    asset_value = user_asset.total_value * current_price

                    if asset.asset_type in asset_type_values:
                        asset_type_values[asset.asset_type] += asset_value
                    else:
                        asset_type_values[asset.asset_type] = asset_value

                    total_portfolio_value += asset_value

                except Exception as e:
                    logger.error(f"Error fetching price data for asset {asset.label}: {e}")
                    continue

            if total_portfolio_value == 0:
                logger.info(f"Total portfolio value for user {user_id} is zero.")
                return None

            asset_type_percentages = {
                asset_type: (value 
                             / total_portfolio_value) * 100
                for asset_type, value in asset_type_values.items()
            }

            return UserAssetTypeDistribution(
                asset_type_values=asset_type_values,
                total_value=total_portfolio_value,
                asset_type_percentages=asset_type_percentages
            )

        except Exception as e:
            logger.error(f"An error occurred while calculating asset type distribution: {e}")
            return None

    # for data injectionnnnnnnnnnnnnnnnnn
    def import_assets_from_csv(self):
        try:
            # Read the CSV file
            csv_path = './services/NASDAQ.csv'
            df = pd.read_csv(csv_path)
            if 'Symbol' not in df.columns:
                logger.error("CSV does not contain 'Symbol' column.")
                return

            symbols = df['Symbol'].dropna().unique().tolist()
            logger.info(f"Found {len(symbols)} unique symbols to process.")

            for i, symbol in enumerate(symbols):
                try:
                    # Introduce a delay to avoid hitting the rate limit
                    if i > 0 and i % 5 == 0:  # Adjust batch size as needed
                        logger.info("Pausing for 2 seconds to respect rate limits...")
                        time.sleep(2)  # Pause to avoid rate limits

                    # Check if asset already exists
                    existing_asset = self.get_asset_by_label(symbol)
                    if existing_asset:
                        logger.info(f"Asset '{symbol}' already exists. Skipping.")
                        continue

                    # Fetch data from yfinance
                    ticker = yf.Ticker(symbol)
                    info = ticker.info

                    # Determine the type of asset
                    if '-USD' in symbol:  # Crypto assets typically have '-USD' suffix
                        asset_type = 'crypto'
                    elif info.get('quoteType') == 'EQUITY':  # Stocks
                        asset_type = 'stock'
                    elif info.get('quoteType') == 'ETF':  # ETFs
                        asset_type = 'etf'
                    elif info.get('quoteType') == 'MUTUALFUND':  # Mutual funds
                        asset_type = 'mutual_fund'
                    else:
                        asset_type = 'other'  # Catch-all for unclassified assets

                    # Extract the asset name or fallback to the symbol
                    name = info.get('shortName') or info.get('longName') or symbol

                    # Prepare AssetCreate schema
                    asset_data = AssetCreate(
                        name=name,
                        asset_type=asset_type,
                        label=symbol
                    )

                    # Create the asset
                    asset = self.create_asset(asset_data)
                    logger.info(f"Asset '{symbol}' ({asset_type}) imported successfully.")

                except Exception as e:
                    logger.error(f"Error processing symbol '{symbol}': {e}")

            logger.info("Asset import completed successfully.")

        except FileNotFoundError:
            logger.error(f"CSV file not found at path: {csv_path}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during import: {e}")
