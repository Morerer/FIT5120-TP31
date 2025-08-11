# main.py - Updated FastAPI with Database
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta


# Import database models and dependencies
from database.models import (
    get_db, PopulationTrend, CongestionTrend, CarOwnershipTrend,
    ParkingZone, ParkingUsage, EnvironmentalData
)

# Create FastAPI app instance
app = FastAPI(
    title="Melbourne CBD Parking System API",
    description="API for Melbourne CBD parking system with real database integration",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173", 
        "https://fit5120-tp31-1.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Pydantic models for API responses
class TrendData(BaseModel):
    year: str
    population: Optional[float] = None
    congestion: Optional[float] = None
    car: Optional[float] = None

class TrendsResponse(BaseModel):
    data: List[TrendData]
    total_records: int
    data_type: str
    date_range: str

class ParkingZoneInfo(BaseModel):
    id: int
    zone_name: str
    zone_code: str
    latitude: Optional[float]
    longitude: Optional[float]
    total_spaces: int
    hourly_rate: float
    current_occupancy: Optional[float] = None

class ParkingUsageData(BaseModel):
    timestamp: datetime
    zone_name: str
    occupied_spaces: int
    total_spaces: int
    occupancy_rate: float

class EnvironmentalMetrics(BaseModel):
    year: int
    month: int
    co2_emissions_tonnes: float
    air_quality_index: float
    green_transport_percentage: float

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Melbourne CBD Parking System API v2.0",
        "database": "SQLite with SQLAlchemy ORM",
        "status": "operational",
        "endpoints": {
            "population_trends": "/api/trends/population",
            "congestion_trends": "/api/trends/congestion",
            "car_ownership_trends": "/api/trends/car-ownership",
            "combined_trends": "/api/trends/combined",
            "parking_zones": "/api/parking/zones",
            "live_parking": "/api/parking/live",
            "environmental": "/api/environmental",
            "api_docs": "/docs"
        }
    }

# Population trends endpoint
@app.get("/api/trends/population", response_model=TrendsResponse)
async def get_population_trends(db: Session = Depends(get_db)):
    """Get population trends data from database"""
    try:
        records = db.query(PopulationTrend).order_by(PopulationTrend.year).all()
        
        if not records:
            raise HTTPException(status_code=404, detail="No population data found")
        
        trend_data = [
            TrendData(
                year=str(record.year),
                population=round(record.population / 1000, 1)  # Convert to thousands
            )
            for record in records
        ]
        
        years = [record.year for record in records]
        date_range = f"{min(years)}–{max(years)}"
        
        return TrendsResponse(
            data=trend_data,
            total_records=len(trend_data),
            data_type="population",
            date_range=date_range
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Congestion trends endpoint
@app.get("/api/trends/congestion", response_model=TrendsResponse)
async def get_congestion_trends(db: Session = Depends(get_db)):
    """Get congestion trends data from database"""
    try:
        records = db.query(CongestionTrend).order_by(CongestionTrend.year).all()
        
        if not records:
            raise HTTPException(status_code=404, detail="No congestion data found")
        
        trend_data = [
            TrendData(
                year=str(record.year),
                congestion=record.congestion_index
            )
            for record in records
        ]
        
        years = [record.year for record in records]
        date_range = f"{min(years)}–{max(years)}"
        
        return TrendsResponse(
            data=trend_data,
            total_records=len(trend_data),
            data_type="congestion",
            date_range=date_range
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Car ownership trends endpoint
@app.get("/api/trends/car-ownership", response_model=TrendsResponse)
async def get_car_ownership_trends(db: Session = Depends(get_db)):
    """Get car ownership trends data from database"""
    try:
        records = db.query(CarOwnershipTrend).order_by(CarOwnershipTrend.year).all()
        
        if not records:
            raise HTTPException(status_code=404, detail="No car ownership data found")
        
        trend_data = [
            TrendData(
                year=str(record.year),
                car=record.cars_per_100_households
            )
            for record in records
        ]
        
        years = [record.year for record in records]
        date_range = f"{min(years)}–{max(years)}"
        
        return TrendsResponse(
            data=trend_data,
            total_records=len(trend_data),
            data_type="car_ownership",
            date_range=date_range
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Combined trends endpoint
@app.get("/api/trends/combined", response_model=TrendsResponse)
async def get_combined_trends(db: Session = Depends(get_db)):
    """Get combined population and congestion data from database"""
    try:
        pop_records = db.query(PopulationTrend).order_by(PopulationTrend.year).all()
        cong_records = db.query(CongestionTrend).order_by(CongestionTrend.year).all()
        
        if not pop_records or not cong_records:
            raise HTTPException(status_code=404, detail="Insufficient data for combined view")
        
        # Create dictionaries for easier lookup
        pop_dict = {record.year: record.population for record in pop_records}
        cong_dict = {record.year: record.congestion_index for record in cong_records}
        
        # Get common years
        common_years = set(pop_dict.keys()) & set(cong_dict.keys())
        
        trend_data = [
            TrendData(
                year=str(year),
                population=round(pop_dict[year] / 1000, 1),
                congestion=cong_dict[year]
            )
            for year in sorted(common_years)
        ]
        
        years = sorted(common_years)
        date_range = f"{min(years)}–{max(years)}" if years else "No data"
        
        return TrendsResponse(
            data=trend_data,
            total_records=len(trend_data),
            data_type="combined",
            date_range=date_range
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Parking zones endpoint
@app.get("/api/parking/zones", response_model=List[ParkingZoneInfo])
async def get_parking_zones(db: Session = Depends(get_db)):
    """Get all parking zones with current occupancy"""
    try:
        zones = db.query(ParkingZone).filter(ParkingZone.is_active == True).all()
        
        zone_info = []
        for zone in zones:
            # Get latest occupancy data
            latest_usage = db.query(ParkingUsage).filter(
                ParkingUsage.zone_id == zone.id
            ).order_by(ParkingUsage.timestamp.desc()).first()
            
            current_occupancy = latest_usage.occupancy_rate if latest_usage else None
            
            zone_info.append(ParkingZoneInfo(
                id=zone.id,
                zone_name=zone.zone_name,
                zone_code=zone.zone_code,
                latitude=zone.latitude,
                longitude=zone.longitude,
                total_spaces=zone.total_spaces,
                hourly_rate=zone.hourly_rate,
                current_occupancy=current_occupancy
            ))
        
        return zone_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Live parking data endpoint
@app.get("/api/parking/live", response_model=List[ParkingUsageData])
async def get_live_parking_data(
    hours_back: int = 24,
    db: Session = Depends(get_db)
):
    """Get recent parking usage data"""
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        # Query recent usage data with zone information
        results = db.query(ParkingUsage, ParkingZone).join(
            ParkingZone, ParkingUsage.zone_id == ParkingZone.id
        ).filter(
            ParkingUsage.timestamp >= cutoff_time
        ).order_by(ParkingUsage.timestamp.desc()).limit(100).all()
        
        usage_data = [
            ParkingUsageData(
                timestamp=usage.timestamp,
                zone_name=zone.zone_name,
                occupied_spaces=usage.occupied_spaces,
                total_spaces=usage.total_spaces,
                occupancy_rate=usage.occupancy_rate
            )
            for usage, zone in results
        ]
        
        return usage_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Environmental data endpoint
@app.get("/api/environmental", response_model=List[EnvironmentalMetrics])
async def get_environmental_data(
    year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get environmental impact data"""
    try:
        query = db.query(EnvironmentalData)
        
        if year:
            query = query.filter(EnvironmentalData.year == year)
        
        records = query.order_by(EnvironmentalData.year, EnvironmentalData.month).all()
        
        return [
            EnvironmentalMetrics(
                year=record.year,
                month=record.month,
                co2_emissions_tonnes=record.co2_emissions_tonnes,
                air_quality_index=record.air_quality_index,
                green_transport_percentage=record.green_transport_percentage
            )
            for record in records
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Get parking zone by ID
@app.get("/api/parking/zones/{zone_id}")
async def get_parking_zone(zone_id: int, db: Session = Depends(get_db)):
    """Get specific parking zone details"""
    zone = db.query(ParkingZone).filter(ParkingZone.id == zone_id).first()
    
    if not zone:
        raise HTTPException(status_code=404, detail="Parking zone not found")
    
    # Get recent usage for this zone
    recent_usage = db.query(ParkingUsage).filter(
        ParkingUsage.zone_id == zone_id
    ).order_by(ParkingUsage.timestamp.desc()).limit(24).all()
    
    return {
        "zone_info": {
            "id": zone.id,
            "name": zone.zone_name,
            "code": zone.zone_code,
            "location": {"lat": zone.latitude, "lng": zone.longitude},
            "total_spaces": zone.total_spaces,
            "hourly_rate": zone.hourly_rate,
            "max_duration_hours": zone.max_duration_hours
        },
        "recent_usage": [
            {
                "timestamp": usage.timestamp,
                "occupancy_rate": usage.occupancy_rate,
                "occupied_spaces": usage.occupied_spaces
            }
            for usage in recent_usage
        ]
    }

# Analytics endpoint for dashboard
@app.get("/api/analytics/summary")
async def get_analytics_summary(db: Session = Depends(get_db)):
    """Get summary analytics for dashboard"""
    try:
        # Get latest population data
        latest_population = db.query(PopulationTrend).order_by(
            PopulationTrend.year.desc()
        ).first()
        
        # Get latest congestion data
        latest_congestion = db.query(CongestionTrend).order_by(
            CongestionTrend.year.desc()
        ).first()
        
        # Get current parking occupancy
        total_zones = db.query(ParkingZone).filter(ParkingZone.is_active == True).count()
        
        # Get average occupancy from last 24 hours
        cutoff_time = datetime.now() - timedelta(hours=24)
        avg_occupancy = db.query(ParkingUsage).filter(
            ParkingUsage.timestamp >= cutoff_time
        ).with_entities(
            db.func.avg(ParkingUsage.occupancy_rate)
        ).scalar()
        
        return {
            "population": {
                "current": latest_population.population if latest_population else None,
                "year": latest_population.year if latest_population else None
            },
            "congestion": {
                "current_index": latest_congestion.congestion_index if latest_congestion else None,
                "year": latest_congestion.year if latest_congestion else None
            },
            "parking": {
                "total_zones": total_zones,
                "avg_occupancy_24h": round(avg_occupancy, 1) if avg_occupancy else None
            },
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")

# Health check with database status
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check with database connectivity"""
    try:
        # Test database connection
        population_count = db.query(PopulationTrend).count()
        zones_count = db.query(ParkingZone).count()
        
        return {
            "status": "healthy",
            "service": "melbourne-parking-api",
            "database": "connected",
            "data_records": {
                "population_trends": population_count,
                "parking_zones": zones_count
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "melbourne-parking-api", 
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Startup event to ensure database is initialized
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        # Import and run database setup
        from database.models import create_tables
        create_tables()
        print("Database tables verified/created on startup")
    except Exception as e:
        print(f"Database startup error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)