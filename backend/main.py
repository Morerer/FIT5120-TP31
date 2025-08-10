from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import json

# Create FastAPI app instance
app = FastAPI(
    title="Melbourne CBD Parking System API",
    description="API for Melbourne CBD parking system with population and traffic trends",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Create React App
        "http://localhost:5173",    # Vite
        "http://localhost:3001",    # Alternative React port
        "http://127.0.0.1:3000",    # Alternative localhost
        "http://127.0.0.1:5173"     # Alternative localhost
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class PopulationData(BaseModel):
    year: int
    population: int

class TrendData(BaseModel):
    year: str
    population: Optional[float] = None
    congestion: Optional[float] = None
    car: Optional[float] = None

class TrendsResponse(BaseModel):
    data: List[TrendData]
    total_records: int
    data_type: str

# Real Melbourne CBD population data
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


def generate_mock_congestion():
    """Generate mock congestion data based on population trends"""
    congestion_data = []
    for item in MELBOURNE_POPULATION_DATA:
        year = item["year"]
        # Simulate congestion increasing with population but with some variance
        base_congestion = 15 + (year - 2001) * 1.5
        # Add some realistic fluctuation
        if year in [2020, 2021]:  # COVID impact
            base_congestion *= 0.7
        congestion_data.append({
            "year": year,
            "congestion": round(base_congestion, 1)
        })
    return congestion_data

def generate_mock_car_ownership():
    """Generate mock car ownership data"""
    car_data = []
    for item in MELBOURNE_POPULATION_DATA:
        year = item["year"]
        # Simulate car ownership decreasing over time in CBD
        base_car = 65 - (year - 2001) * 0.8
        if year in [2020, 2021]:  # COVID impact
            base_car *= 1.1
        car_data.append({
            "year": year,
            "car": round(base_car, 1)
        })
    return car_data

# Generate mock data
CONGESTION_DATA = generate_mock_congestion()
CAR_OWNERSHIP_DATA = generate_mock_car_ownership()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Melbourne CBD Parking System API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "population_trends": "/api/trends/population",
            "congestion_trends": "/api/trends/congestion",
            "car_ownership_trends": "/api/trends/car-ownership",
            "combined_trends": "/api/trends/combined",
            "api_docs": "/docs",
            "health_check": "/health"
        }
    }

# Population trends endpoint
@app.get("/api/trends/population", response_model=TrendsResponse)
async def get_population_trends():
    """
    Get population trends data for Melbourne CBD
    Returns actual population data from 2001-2021
    """
    trend_data = [
        TrendData(
            year=str(item["year"]),
            population=round(item["population"] / 1000, 1)  # Convert to thousands for better chart display
        )
        for item in MELBOURNE_POPULATION_DATA
    ]
    
    return TrendsResponse(
        data=trend_data,
        total_records=len(trend_data),
        data_type="population"
    )

# Congestion trends endpoint
@app.get("/api/trends/congestion", response_model=TrendsResponse)
async def get_congestion_trends():
    """
    Get congestion trends data for Melbourne CBD
    """
    trend_data = [
        TrendData(
            year=str(item["year"]),
            congestion=item["congestion"]
        )
        for item in CONGESTION_DATA
    ]
    
    return TrendsResponse(
        data=trend_data,
        total_records=len(trend_data),
        data_type="congestion"
    )

# Car ownership trends endpoint
@app.get("/api/trends/car-ownership", response_model=TrendsResponse)
async def get_car_ownership_trends():
    """
    Get car ownership trends data for Melbourne CBD
    """
    trend_data = [
        TrendData(
            year=str(item["year"]),
            car=item["car"]
        )
        for item in CAR_OWNERSHIP_DATA
    ]
    
    return TrendsResponse(
        data=trend_data,
        total_records=len(trend_data),
        data_type="car_ownership"
    )

# Combined trends endpoint for "both" view
@app.get("/api/trends/combined", response_model=TrendsResponse)
async def get_combined_trends():
    """
    Get combined population and congestion data
    """
    trend_data = []
    
    for i, pop_item in enumerate(MELBOURNE_POPULATION_DATA):
        year = str(pop_item["year"])
        congestion_item = CONGESTION_DATA[i]
        
        trend_data.append(TrendData(
            year=year,
            population=round(pop_item["population"] / 1000, 1),  # Convert to thousands
            congestion=congestion_item["congestion"]
        ))
    
    return TrendsResponse(
        data=trend_data,
        total_records=len(trend_data),
        data_type="combined"
    )

# Get trends by year range
@app.get("/api/trends/{trend_type}/range")
async def get_trends_by_range(
    trend_type: str,
    start_year: int = 2001,
    end_year: int = 2021
):
    """
    Get trend data for a specific year range
    
    Args:
        trend_type: Type of trend (population, congestion, car-ownership, combined)
        start_year: Starting year (default: 2001)
        end_year: Ending year (default: 2021)
    """
    if trend_type not in ["population", "congestion", "car-ownership", "combined"]:
        raise HTTPException(status_code=400, detail="Invalid trend type")
    
    if start_year > end_year:
        raise HTTPException(status_code=400, detail="Start year must be before end year")
    
    # Filter data based on year range
    if trend_type == "population":
        filtered_data = [
            item for item in MELBOURNE_POPULATION_DATA
            if start_year <= item["year"] <= end_year
        ]
        trend_data = [
            TrendData(
                year=str(item["year"]),
                population=round(item["population"] / 1000, 1)
            )
            for item in filtered_data
        ]
    elif trend_type == "congestion":
        filtered_data = [
            item for item in CONGESTION_DATA
            if start_year <= item["year"] <= end_year
        ]
        trend_data = [
            TrendData(year=str(item["year"]), congestion=item["congestion"])
            for item in filtered_data
        ]
    elif trend_type == "car-ownership":
        filtered_data = [
            item for item in CAR_OWNERSHIP_DATA
            if start_year <= item["year"] <= end_year
        ]
        trend_data = [
            TrendData(year=str(item["year"]), car=item["car"])
            for item in filtered_data
        ]
    else:  # combined
        filtered_pop = [
            item for item in MELBOURNE_POPULATION_DATA
            if start_year <= item["year"] <= end_year
        ]
        filtered_congestion = [
            item for item in CONGESTION_DATA
            if start_year <= item["year"] <= end_year
        ]
        
        trend_data = []
        for i, pop_item in enumerate(filtered_pop):
            if i < len(filtered_congestion):
                trend_data.append(TrendData(
                    year=str(pop_item["year"]),
                    population=round(pop_item["population"] / 1000, 1),
                    congestion=filtered_congestion[i]["congestion"]
                ))
    
    return TrendsResponse(
        data=trend_data,
        total_records=len(trend_data),
        data_type=trend_type
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "melbourne-parking-api",
        "data_records": {
            "population": len(MELBOURNE_POPULATION_DATA),
            "congestion": len(CONGESTION_DATA),
            "car_ownership": len(CAR_OWNERSHIP_DATA)
        }
    }

# Get available years
@app.get("/api/trends/years")
async def get_available_years():
    """Get list of available years for trend data"""
    years = sorted([item["year"] for item in MELBOURNE_POPULATION_DATA])
    return {
        "years": years,
        "start_year": min(years),
        "end_year": max(years),
        "total_years": len(years)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)