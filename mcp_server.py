import requests
from fastmcp import FastMCP

# Create the MCP server instance with stateless HTTP
mcp = FastMCP("Simulation Tools", stateless_http=True)

@mcp.tool
def simulate(
    n_servers: int = 1,
    arrival_rate: float = 5.0,
    service_time: float = 3.0,
    sim_time: int = 50,
    random_seed: int = 42
):
    """
    Simulates a multi-server queuing system (e.g., supermarket, call center).

    This tool wraps a REST API that models customers arriving, waiting, and being served.
    You can control:
    - `n_servers`: Number of parallel service stations
    - `arrival_rate`: Customer arrival rate per time unit
    - `service_time`: Average service time per customer
    - `sim_time`: Total simulation time
    - `random_seed`: (Optional) fixed seed for reproducibility

    Returns:
    - total_customers: Total customers served
    - avg_wait_time: Average time spent waiting before service
    - avg_system_time: Average total time in system (wait + service)
    """
    try:
        response = requests.post(
            "http://localhost:8000/simulate",
            json={
                "n_servers": n_servers,
                "arrival_rate": arrival_rate,
                "service_time": service_time,
                "sim_time": sim_time,
                "random_seed": random_seed,
                "verbose": False
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to call simulation API: {str(e)}"}

@mcp.tool
def get_workorder_details(workorder_number: str):
    """
    Retrieves detailed information about a specific workorder's journey through production lines.

    This tool provides comprehensive tracking information for manufacturing workorders, including:
    - Which production lines the workorder has passed through
    - Actual time spent at each production line (in days)
    - Start and end dates for each production line
    - Current status of each line (Completed/In Progress)
    - Overall workorder status and total processing time

    Production lines include manufacturing lines (1200REI, 1200GR35), material handling (MH),
    quality control (QC), assembly, packaging, and shipping operations.

    Args:
        workorder_number (str): The unique identifier of the workorder to retrieve details for.
                               Can be any string format (e.g., "WO-2024-001", "PROD-123", etc.)

    Returns:
        dict: A comprehensive workorder details object containing:
            - workorder_number: The requested workorder identifier
            - total_processing_time_days: Sum of all time spent across production lines
            - production_lines: Array of line details with timing and status information
            - current_status: Overall workorder status (In Progress/Completed)
            - created_date: When the workorder was created

    Example:
        >>> get_workorder_details("WO-2024-001")
        {
            "workorder_number": "WO-2024-001",
            "total_processing_time_days": 8.2,
            "production_lines": [...],
            "current_status": "In Progress",
            "created_date": "2024-01-10"
        }

    Note:
        - The same workorder number will always return consistent data
        - Production line selection is randomized but deterministic per workorder
        - Time values represent actual processing time, not planned/configured time
    """
    try:
        response = requests.get(
            f"http://localhost:8000/workorder/{workorder_number}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to retrieve workorder details: {str(e)}"}

@mcp.tool
def get_workorder_configuration(workorder_number: str):
    """
    Retrieves the configured/planned settings and timing for each production line in a workorder.

    This tool provides the planned configuration information for manufacturing workorders, including:
    - Standard/configured time allocated for each production line (in days)
    - Line type classifications (Manufacturing, Quality Control, Assembly, etc.)
    - Daily capacity specifications for each line
    - Priority levels for production line processing
    - Overall workorder type and priority classification

    This is different from actual processing time - it represents the planned/standard time
    that should be allocated for each production line based on engineering specifications.

    Args:
        workorder_number (str): The unique identifier of the workorder to retrieve configuration for.
                               Must be the same as used in get_workorder_details for consistency.

    Returns:
        dict: A comprehensive workorder configuration object containing:
            - workorder_number: The requested workorder identifier
            - total_configured_time_days: Sum of all configured times across production lines
            - production_line_configs: Array of line configuration details
            - workorder_type: Classification (Standard, Express, Priority, Custom)
            - priority_level: Overall priority (Low, Medium, High, Critical)

    Example:
        >>> get_workorder_configuration("WO-2024-001")
        {
            "workorder_number": "WO-2024-001",
            "total_configured_time_days": 12.5,
            "production_line_configs": [...],
            "workorder_type": "Priority",
            "priority_level": "High"
        }

    Note:
        - Returns the same number of production lines as get_workorder_details for consistency
        - Configured time values are different from actual processing time
        - Line names and count are guaranteed to match get_workorder_details for the same workorder
        - Useful for comparing planned vs. actual performance and capacity planning
    """
    try:
        response = requests.get(
            f"http://localhost:8000/workorder/{workorder_number}/configuration",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to retrieve workorder configuration: {str(e)}"}


    # Run the MCP server with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8001)