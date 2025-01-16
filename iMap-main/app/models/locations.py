from app import db
from sqlalchemy import Column, Integer, String, Float

class Location(db.Model):

    __tablename__ = "locations"

    id = Column(Integer, primary_key = True, autoincrement=True)
    # 经度
    lng = Column(Float, nullable=False)
    # 纬度
    lat = Column(Float, nullable=False)
    # 地址
    address = Column(String(255), nullable=False)
    # 标签
    tag = Column(String(100), nullable=False)
    
    def __init__(self, lng, lat, address, tag):
        self.lng = lng
        self.lat = lat
        self.address = address
        self.tag = tag

    # 方便查看日志
    def __repr__(self):
        return f"<Location(id={self.id}, lng={self.lng}, lat={self.lat}, address={self.address}, tag={self.tag})>"

    def __str__(self):
        return f"Location {self.address} ({self.lat}, {self.lng})"
