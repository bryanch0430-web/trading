from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas import assets
from model import Asset, UserAsset
from typing import Optional
import pandas as pd
import yfinance as yf
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AssetService:
    def __init__(self, db: Session):
            self.db = db

    def create_asset(self, asset: assets.AssetCreate, user_id: int):
        db_asset = Asset(
            name=asset.name,
            asset_type=asset.asset_type,
            total_value=asset.total_value,
            user_id=user_id
        )
        self.db.add(db_asset)
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset

    def get_asset_by_id(self, asset_id: int):
        return self.db.query(Asset).filter(Asset.id == asset_id).first()


    def get_asset_by_name(self, name: str) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.name == name).first()

    def associate_asset_with_user(self, asset: Asset, user_id: str, total_value: float = 0.0, average_price: float = 0.0) -> Optional[UserAsset]:
        """
        Associates an Asset with a User by creating a UserAsset entry.

        Args:
            asset (Asset): The asset to associate.
            user_id (str): The UUID of the user.
            total_value (float): The total value of the asset for the user.
            average_price (float): The average price of the asset for the user.

        Returns:
            UserAsset: The created association.
        """
        user_asset = UserAsset(
            user_id=user_id,
            asset_id=asset.id,
            total_value=total_value,
            average_price=average_price
        )
        self.db.add(user_asset)
        try:
            self.db.commit()
            logger.info(f"Asset '{asset.name}' associated with User ID: {user_id}")
            return user_asset
        except IntegrityError:
            self.db.rollback()
            logger.warning(f"Asset '{asset.name}' is already associated with User ID: {user_id}")
            return self.get_user_asset(user_id, asset.id)

    def get_user_asset(self, user_id: str, asset_id: str) -> Optional[UserAsset]:
        return self.db.query(UserAsset).filter(UserAsset.user_id == user_id, UserAsset.asset_id == asset_id).first()

    def import_assets_from_csv(self, csv_path: str, user_id: Optional[str] = None):
        """
        Imports assets from a CSV file and saves them into the Asset table.
        Optionally associates them with a user.

        Args:
            csv_path (str): Path to the NASDAQ.csv file.
            user_id (Optional[str]): UUID of the user to associate assets with (if applicable).
        """
        try:
            # Read the CSV file
            df = pd.read_csv(csv_path)
            if 'symbol' not in df.columns:
                logger.error("CSV does not contain 'symbol' column.")
                return

            symbols = df['symbol'].dropna().unique().tolist()
            logger.info(f"Found {len(symbols)} unique symbols to process.")

            for symbol in symbols:
                try:
                    # Fetch data from yfinance
                    ticker = yf.Ticker(symbol)
                    info = ticker.info

                    # Extract required fields
                    name = info.get('shortName') or info.get('longName') or symbol
                    asset_type = 'stock'  # Assuming all are stocks. Adjust if needed.

                    # Prepare AssetCreate schema
                    asset_data = assets.AssetCreate(
                        name=name,
                        asset_type=asset_type,
                        total_value=0.0  # Initialize as needed
                    )

                    # Create or get existing asset
                    asset = self.create_asset(asset_data)

                    # If user_id is provided, associate the asset with the user
                    if user_id:
                        self.associate_asset_with_user(asset, user_id)

                except Exception as e:
                    logger.error(f"Error processing symbol '{symbol}': {e}")

            logger.info("Asset import completed successfully.")

        except FileNotFoundError:
            logger.error(f"CSV file not found at path: {csv_path}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during import: {e}")