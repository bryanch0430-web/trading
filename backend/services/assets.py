from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas import assets
from model import Asset, UserAsset
from typing import Optional
import pandas as pd
import yfinance as yf
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AssetService:
    def __init__(self, db: Session):
            self.db = db

    def create_asset(self, asset: assets.AssetCreate):
        db_asset = Asset(
            name=asset.name,
            asset_type=asset.asset_type,
            label =asset.label
        )
        self.db.add(db_asset)
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset

    def get_asset_by_id(self, asset_id: int):
        return self.db.query(Asset).filter(Asset.id == asset_id).first()


    def get_asset_by_name(self, name: str) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.name == name).first()
    def get_asset_by_label(self, label: str) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.label == label).first()
    def get_user_asset(self, user_id: str, asset_id: str) -> Optional[UserAsset]:
        return self.db.query(UserAsset).filter(UserAsset.user_id == user_id, UserAsset.asset_id == asset_id).first()
    def list_all_asset(self)-> Optional[Asset]:
         return self.db.query(Asset).all()
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
                    asset_data = assets.AssetCreate(
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