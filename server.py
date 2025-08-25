from fastapi import FastAPI
from pydantic import BaseModel
from simulation import run_simulation
import uvicorn
from typing import List
from datetime import datetime, timedelta
import random

app = FastAPI()

# Define input schema
class SimulationInput(BaseModel):
    n_servers: int = 1
    arrival_rate: float = 5.0
    service_time: float = 3.0
    sim_time: int = 50
    random_seed: int = 42
    verbose: bool = False

# Define workorder line details schema
class ProductionLineDetail(BaseModel):
    line_name: str
    time_spent_days: float
    start_date: str
    end_date: str
    status: str

# Define workorder line configuration schema
class ProductionLineConfiguration(BaseModel):
    line_name: str
    configured_time_days: float
    line_type: str
    capacity_per_day: int
    priority: int

# Define workorder response schema
class WorkorderResponse(BaseModel):
    workorder_number: str
    total_processing_time_days: float
    production_lines: List[ProductionLineDetail]
    current_status: str
    created_date: str

# Define workorder configuration response schema
class WorkorderConfigurationResponse(BaseModel):
    workorder_number: str
    total_configured_time_days: float
    production_line_configs: List[ProductionLineConfiguration]
    workorder_type: str
    priority_level: str

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

# Define the POST endpoint
@app.post("/simulate")
def simulate(input: SimulationInput):
    result = run_simulation(
        n_servers=input.n_servers,
        arrival_rate=input.arrival_rate,
        service_time=input.service_time,
        sim_time=input.sim_time,
        random_seed=input.random_seed,
        verbose=input.verbose
    )
    return result

@app.get("/workorder/{workorder_number}")
def get_workorder_details(workorder_number: str):
    """
    Get detailed information about a specific workorder including production lines and time spent
    """
    # Define available production lines
    production_lines = ["1200REI", "1200GR35", "MH", "QC", "Assembly", "Packaging", "Shipping"]
    
    # Generate realistic workorder data (in a real scenario, this would come from a database)
    # For demonstration, we'll create random but realistic data
    random.seed(hash(workorder_number) % 1000)  # Use workorder number as seed for consistent results
    
    # Randomly select 3-5 production lines for this workorder
    num_lines = random.randint(3, 5)
    selected_lines = random.sample(production_lines, num_lines)
    
    # Generate line details with realistic timing
    line_details = []
    current_date = datetime.now() - timedelta(days=random.randint(10, 30))
    
    for i, line_name in enumerate(selected_lines):
        # Random processing time between 0.5 to 3 days
        time_spent = round(random.uniform(0.5, 3.0), 1)
        
        start_date = current_date
        end_date = start_date + timedelta(days=time_spent)
        
        # Determine status based on position in sequence
        if i == len(selected_lines) - 1:
            status = "Completed"
        elif i == len(selected_lines) - 2:
            status = "In Progress"
        else:
            status = "Completed"
        
        line_detail = ProductionLineDetail(
            line_name=line_name,
            time_spent_days=time_spent,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            status=status
        )
        line_details.append(line_detail)
        
        # Move to next line start date
        current_date = end_date + timedelta(days=random.randint(0, 2))  # Small gap between lines
    
    # Calculate total processing time
    total_time = sum(line.time_spent_days for line in line_details)
    
    # Determine current status
    current_status = "In Progress" if any(line.status == "In Progress" for line in line_details) else "Completed"
    
    response = WorkorderResponse(
        workorder_number=workorder_number,
        total_processing_time_days=round(total_time, 1),
        production_lines=line_details,
        current_status=current_status,
        created_date=(datetime.now() - timedelta(days=random.randint(30, 60))).strftime("%Y-%m-%d")
    )
    
    return response

@app.get("/workorder/{workorder_number}/configuration")
def get_workorder_configuration(workorder_number: str):
    """
    Get configured time and settings for each production line in a workorder
    """
    # Define available production lines (same as get_workorder_details)
    production_lines = ["1200REI", "1200GR35", "MH", "QC", "Assembly", "Packaging", "Shipping"]
    
    # Use the same seed as get_workorder_details to ensure same number of lines
    random.seed(hash(workorder_number) % 1000)
    
    # Select the same number of lines as get_workorder_details
    num_lines = random.randint(3, 5)
    selected_lines = random.sample(production_lines, num_lines)
    
    # Line type mappings
    line_types = {
        "1200REI": "Manufacturing",
        "1200GR35": "Manufacturing", 
        "MH": "Material Handling",
        "QC": "Quality Control",
        "Assembly": "Assembly",
        "Packaging": "Packaging",
        "Shipping": "Logistics"
    }
    
    # Generate line configurations with different timing than actual processing time
    line_configs = []
    total_configured_time = 0
    
    for i, line_name in enumerate(selected_lines):
        # Configured time is different from actual processing time
        # Usually configured time is the standard/planned time for the line
        configured_time = round(random.uniform(1.0, 4.0), 1)
        
        # Capacity per day (units that can be processed)
        capacity_per_day = random.randint(50, 200)
        
        # Priority level (1-5, where 1 is highest priority)
        priority = random.randint(1, 5)
        
        line_config = ProductionLineConfiguration(
            line_name=line_name,
            configured_time_days=configured_time,
            line_type=line_types.get(line_name, "General"),
            capacity_per_day=capacity_per_day,
            priority=priority
        )
        line_configs.append(line_config)
        total_configured_time += configured_time
    
    # Determine workorder type and priority level
    workorder_types = ["Standard", "Express", "Priority", "Custom"]
    workorder_type = random.choice(workorder_types)
    
    priority_levels = ["Low", "Medium", "High", "Critical"]
    priority_level = random.choice(priority_levels)
    
    response = WorkorderConfigurationResponse(
        workorder_number=workorder_number,
        total_configured_time_days=round(total_configured_time, 1),
        production_line_configs=line_configs,
        workorder_type=workorder_type,
        priority_level=priority_level
    )
    
    return response

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)