# database/setup.py
from sqlalchemy.orm import Session
from database.models import (
    create_tables, get_db, engine, SessionLocal,
    PopulationTrend, CongestionTrend, CarOwnershipTrend,
    ParkingZone, ParkingUsage, TrafficSensor, TrafficData,
    EnvironmentalData
)
from datetime import datetime, timedelta
import random


MELBOURNE_POPULATION_DATA = [
    {"year": 2001, "population": 55399},
    {"year": 2002, "population": 60592},
    {"year": 2003, "population": 66149},
    {"year": 2004, "population": 71532},
    {"year": 2005, "population": 76197},
    {"year": 2006, "population": 80154},
    {"year": 2007, "population": 85141},
    {"year": 2008, "population": 89792},
    {"year": 2009, "population": 94330},
    {"year": 2010, "population": 97578},
    {"year": 2011, "population": 100228},
    {"year": 2012, "population": 107573},
    {"year": 2013, "population": 118707},
    {"year": 2014, "population": 127975},
    {"year": 2015, "population": 136873},
    {"year": 2016, "population": 146099},
    {"year": 2017, "population": 155992},
    {"year": 2018, "population": 163449},
    {"year": 2019, "population": 169106},
    {"year": 2020, "population": 170785},
    {"year": 2021, "population": 153655}
]

def setup_database():
    """Initialize database and create all tables"""
    print("Creating database tables...")
    create_tables()
    print("✅ Database tables created successfully!")

def populate_population_data(db: Session):
    """Populate population trends table"""
    print("Populating population data...")
    
    for item in MELBOURNE_POPULATION_DATA:
        # Check if data already exists
        existing = db.query(PopulationTrend).filter(PopulationTrend.year == item["year"]).first()
        if not existing:
            population_record = PopulationTrend(
                year=item["year"],
                population=item["population"]
            )
            db.add(population_record)
    
    db.commit()
    print("✅ Population data populated!")

def populate_congestion_data(db: Session):
    """Generate and populate congestion data"""
    print("Populating congestion data...")
    
    for item in MELBOURNE_POPULATION_DATA:
        year = item["year"]
        existing = db.query(CongestionTrend).filter(CongestionTrend.year == year).first()
        
        if not existing:
            # Generate realistic congestion data
            base_congestion = 15 + (year - 2001) * 1.5
            
            # COVID-19 impact
            if year in [2020, 2021]:
                base_congestion *= 0.7
            
            # Add some variance
            congestion_index = round(base_congestion + random.uniform(-2, 2), 1)
            avg_speed = round(25 + random.uniform(-5, 10), 1)  # km/h in CBD
            peak_delay = round(congestion_index * 0.8 + random.uniform(-2, 3), 1)
            
            congestion_record = CongestionTrend(
                year=year,
                congestion_index=congestion_index,
                average_speed_kmh=avg_speed,
                peak_hour_delay_minutes=peak_delay
            )
            db.add(congestion_record)
    
    db.commit()
    print("✅ Congestion data populated!")

def populate_car_ownership_data(db: Session):
    """Generate and populate car ownership data"""
    print("Populating car ownership data...")
    
    for item in MELBOURNE_POPULATION_DATA:
        year = item["year"]
        existing = db.query(CarOwnershipTrend).filter(CarOwnershipTrend.year == year).first()
        
        if not existing:
            # Generate realistic car ownership data (decreasing over time in CBD)
            base_car = 65 - (year - 2001) * 0.8
            
            # COVID-19 impact (slight increase due to avoiding public transport)
            if year in [2020, 2021]:
                base_car *= 1.1
            
            cars_per_100 = round(base_car + random.uniform(-3, 3), 1)
            total_vehicles = int(item["population"] * (cars_per_100 / 100) * random.uniform(0.8, 1.2))
            
            car_record = CarOwnershipTrend(
                year=year,
                cars_per_100_households=cars_per_100,
                total_registered_vehicles=total_vehicles
            )
            db.add(car_record)
    
    db.commit()
    print("✅ Car ownership data populated!")

def populate_parking_zones(db: Session):
    """Create sample parking zones in Melbourne CBD"""
    print("Populating parking zones...")
    
    zones = [
        {"name": "Collins Street East", "code": "CSE", "lat": -37.8136, "lng": 144.9631, "spaces": 150, "rate": 8.50, "max_hours": 4},
        {"name": "Bourke Street Mall", "code": "BSM", "lat": -37.8140, "lng": 144.9633, "spaces": 200, "rate": 10.00, "max_hours": 2},
        {"name": "Flinders Street", "code": "FS", "lat": -37.8183, "lng": 144.9671, "spaces": 180, "rate": 7.50, "max_hours": 8},
        {"name": "Queen Street", "code": "QS", "lat": -37.8136, "lng": 144.9613, "spaces": 120, "rate": 9.00, "max_hours": 4},
        {"name": "Elizabeth Street", "code": "ES", "lat": -37.8118, "lng": 144.9618, "spaces": 160, "rate": 8.00, "max_hours": 6},
        {"name": "Spring Street", "code": "SS", "lat": -37.8136, "lng": 144.9742, "spaces": 90, "rate": 6.50, "max_hours": 8},
        {"name": "Lonsdale Street", "code": "LS", "lat": -37.8118, "lng": 144.9648, "spaces": 140, "rate": 7.00, "max_hours": 6},
        {"name": "Little Collins", "code": "LC", "lat": -37.8118, "lng": 144.9648, "spaces": 100, "rate": 9.50, "max_hours": 3}
    ]
    
    for zone_data in zones:
        existing = db.query(ParkingZone).filter(ParkingZone.zone_code == zone_data["code"]).first()
        if not existing:
            zone = ParkingZone(
                zone_name=zone_data["name"],
                zone_code=zone_data["code"],
                latitude=zone_data["lat"],
                longitude=zone_data["lng"],
                total_spaces=zone_data["spaces"],
                hourly_rate=zone_data["rate"],
                max_duration_hours=zone_data["max_hours"]
            )
            db.add(zone)
    
    db.commit()
    print("✅ Parking zones populated!")

def populate_sample_usage_data(db: Session):
    """Generate sample parking usage data for the last 30 days"""
    print("Populating sample parking usage data...")
    
    zones = db.query(ParkingZone).all()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    current_date = start_date
    while current_date <= end_date:
        for zone in zones:
            # Generate hourly data for peak hours (7-9 AM, 12-2 PM, 5-7 PM)
            peak_hours = [7, 8, 9, 12, 13, 14, 17, 18, 19]
            
            for hour in peak_hours:
                timestamp = current_date.replace(hour=hour, minute=0, second=0, microsecond=0)
                
                # Generate realistic occupancy based on hour and day
                base_occupancy = 0.6  # 60% base occupancy
                
                if current_date.weekday() < 5:  # Weekday
                    if hour in [8, 13, 18]:  # Peak hours
                        base_occupancy = 0.85
                    elif hour in [7, 9, 12, 14, 17, 19]:  # Near peak
                        base_occupancy = 0.75
                else:  # Weekend
                    base_occupancy = 0.4
                
                # Add some randomness
                occupancy_rate = max(0, min(100, base_occupancy * 100 + random.uniform(-15, 15)))
                occupied_spaces = int((occupancy_rate / 100) * zone.total_spaces)
                
                existing = db.query(ParkingUsage).filter(
                    ParkingUsage.zone_id == zone.id,
                    ParkingUsage.timestamp == timestamp
                ).first()
                
                if not existing:
                    usage = ParkingUsage(
                        zone_id=zone.id,
                        timestamp=timestamp,
                        occupied_spaces=occupied_spaces,
                        total_spaces=zone.total_spaces,
                        occupancy_rate=round(occupancy_rate, 1),
                        hour_of_day=hour,
                        day_of_week=current_date.weekday()
                    )
                    db.add(usage)
        
        current_date += timedelta(days=1)
    
    db.commit()
    print("✅ Sample parking usage data populated!")

def populate_environmental_data(db: Session):
    """Generate environmental impact data"""
    print("Populating environmental data...")
    
    for year in range(2015, 2022):  # Last 7 years
        for month in range(1, 13):
            existing = db.query(EnvironmentalData).filter(
                EnvironmentalData.year == year,
                EnvironmentalData.month == month
            ).first()
            
            if not existing:
                # Generate realistic environmental data
                base_co2 = 1500 + (year - 2015) * 50  # Increasing trend
                if year in [2020, 2021]:  # COVID reduction
                    base_co2 *= 0.8
                
                env_data = EnvironmentalData(
                    year=year,
                    month=month,
                    co2_emissions_tonnes=round(base_co2 + random.uniform(-200, 200), 1),
                    air_quality_index=round(45 + random.uniform(-10, 25), 1),
                    noise_level_db=round(65 + random.uniform(-5, 10), 1),
                    green_transport_percentage=round(35 + random.uniform(-5, 15), 1)
                )
                db.add(env_data)
    
    db.commit()
    print("✅ Environmental data populated!")

def main():
    """Main setup function"""
    print("🚀 Setting up Melbourne CBD Parking Database...")
    print("=" * 50)
    
    # Create database and tables
    setup_database()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Populate all data
        populate_population_data(db)
        populate_congestion_data(db)
        populate_car_ownership_data(db)
        populate_parking_zones(db)
        populate_sample_usage_data(db)
        populate_environmental_data(db)
        
        print("=" * 50)
        print("🎉 Database setup completed successfully!")
        print(f"📊 Database location: melbourne_parking.db")
        print(f"🔗 You can now start your FastAPI server!")
        
        # Show summary
        population_count = db.query(PopulationTrend).count()
        congestion_count = db.query(CongestionTrend).count()
        parking_zones_count = db.query(ParkingZone).count()
        usage_records_count = db.query(ParkingUsage).count()
        
        print(f"\n📈 Data Summary:")
        print(f"   • Population records: {population_count}")
        print(f"   • Congestion records: {congestion_count}")
        print(f"   • Parking zones: {parking_zones_count}")
        print(f"   • Usage records: {usage_records_count}")
        
    except Exception as e:
        print(f"❌ Error during setup: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()