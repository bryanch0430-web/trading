from sqlalchemy.orm import Session
from ..schemas import assets
from ..model import Asset


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


