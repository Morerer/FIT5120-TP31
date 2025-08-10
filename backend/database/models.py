# database/models.py
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./melbourne_parking.db")

# Create engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

# Population trends table
class PopulationTrend(Base):
    __tablename__ = "population_trends"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, unique=True, index=True)
    population = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Traffic congestion table
class CongestionTrend(Base):
    __tablename__ = "congestion_trends"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, unique=True, index=True)
    congestion_index = Column(Float, nullable=False)
    average_speed_kmh = Column(Float)
    peak_hour_delay_minutes = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Car ownership table
class CarOwnershipTrend(Base):
    __tablename__ = "car_ownership_trends"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, unique=True, index=True)
    cars_per_100_households = Column(Float, nullable=False)
    total_registered_vehicles = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Parking zones table
class ParkingZone(Base):
    __tablename__ = "parking_zones"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String(100), nullable=False, unique=True, index=True)
    zone_code = Column(String(10), nullable=False, unique=True)
    latitude = Column(Float)
    longitude = Column(Float)
    total_spaces = Column(Integer)
    hourly_rate = Column(Float)
    max_duration_hours = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to parking usage
    usage_records = relationship("ParkingUsage", back_populates="zone")

# Parking usage/occupancy table
class ParkingUsage(Base):
    __tablename__ = "parking_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("parking_zones.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    occupied_spaces = Column(Integer, nullable=False)
    total_spaces = Column(Integer, nullable=False)
    occupancy_rate = Column(Float)  # Percentage (0-100)
    hour_of_day = Column(Integer, index=True)  # 0-23 for analysis
    day_of_week = Column(Integer, index=True)  # 0-6 (Monday=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to parking zone
    zone = relationship("ParkingZone", back_populates="usage_records")

# Traffic sensor data table
class TrafficSensor(Base):
    __tablename__ = "traffic_sensors"
    
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String(50), nullable=False, unique=True, index=True)
    location_name = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)
    road_type = Column(String(50))  # arterial, freeway, local, etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to traffic data
    traffic_data = relationship("TrafficData", back_populates="sensor")

# Traffic data table
class TrafficData(Base):
    __tablename__ = "traffic_data"
    
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("traffic_sensors.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    vehicle_count = Column(Integer)
    average_speed = Column(Float)
    congestion_level = Column(String(20))  # low, medium, high, severe
    hour_of_day = Column(Integer, index=True)
    day_of_week = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to traffic sensor
    sensor = relationship("TrafficSensor", back_populates="traffic_data")

# Environmental data table
class EnvironmentalData(Base):
    __tablename__ = "environmental_data"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    month = Column(Integer, index=True)
    co2_emissions_tonnes = Column(Float)
    air_quality_index = Column(Float)
    noise_level_db = Column(Float)
    green_transport_percentage = Column(Float)  # % using public transport/cycling/walking
    created_at = Column(DateTime, default=datetime.utcnow)

# Create all tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()