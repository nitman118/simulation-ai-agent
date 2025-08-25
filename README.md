# Simulation AI Agents

A comprehensive simulation and manufacturing tracking system with REST APIs and MCP (Model Context Protocol) tools for AI agent integration.

## 🚀 Features

- **Queue Simulation**: Multi-server queuing system simulation with configurable parameters
- **Workorder Tracking**: Real-time tracking of manufacturing workorders through production lines
- **Production Line Management**: Support for various production lines including 1200REI, 1200GR35, MH, QC, Assembly, Packaging, and Shipping
- **MCP Integration**: Model Context Protocol tools for seamless AI agent interaction
- **RESTful APIs**: FastAPI-based endpoints for easy integration

## 🏗️ Project Structure

```
simulation-ai-agents/
├── server.py              # FastAPI server with REST endpoints
├── mcp_server.py          # MCP server with AI agent tools
├── simulation.py          # Core simulation logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── venv/                 # Virtual environment
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd simulation-ai-agents
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Starting the Services

1. **Start the FastAPI server** (Terminal 1)
   ```bash
   python server.py
   ```
   Server runs on: `http://localhost:8000`

2. **Start the MCP server** (Terminal 2)
   ```bash
   python mcp_server.py
   ```
   MCP server runs on: `http://localhost:8001`

### API Endpoints

#### 1. Queue Simulation
```http
POST /simulate
Content-Type: application/json

{
  "n_servers": 1,
  "arrival_rate": 5.0,
  "service_time": 3.0,
  "sim_time": 50,
  "random_seed": 42,
  "verbose": false
}
```

**Response:**
```json
{
  "total_customers": 250,
  "avg_wait_time": 2.1,
  "avg_system_time": 5.2
}
```

#### 2. Workorder Details
```http
GET /workorder/{workorder_number}
```

**Example:**
```http
GET /workorder/WO-2024-001
```

**Response:**
```json
{
  "workorder_number": "WO-2024-001",
  "total_processing_time_days": 8.2,
  "production_lines": [
    {
      "line_name": "1200REI",
      "time_spent_days": 2.1,
      "start_date": "2024-01-15",
      "end_date": "2024-01-17",
      "status": "Completed"
    },
    {
      "line_name": "QC",
      "time_spent_days": 1.5,
      "start_date": "2024-01-18",
      "status": "In Progress"
    }
  ],
  "current_status": "In Progress",
  "created_date": "2024-01-10"
}
```

#### 3. Workorder Configuration
```http
GET /workorder/{workorder_number}/configuration
```

**Example:**
```http
GET /workorder/WO-2024-001/configuration
```

**Response:**
```json
{
  "workorder_number": "WO-2024-001",
  "total_configured_time_days": 12.5,
  "production_line_configs": [
    {
      "line_name": "1200REI",
      "configured_time_days": 3.2,
      "line_type": "Manufacturing",
      "capacity_per_day": 150,
      "priority": 2
    }
  ],
  "workorder_type": "Priority",
  "priority_level": "High"
}
```

## 🤖 MCP Tools

The MCP server provides three tools for AI agent integration:

### 1. `simulate`
Simulates a multi-server queuing system with configurable parameters.

**Parameters:**
- `n_servers`: Number of parallel service stations
- `arrival_rate`: Customer arrival rate per time unit
- `service_time`: Average service time per customer
- `sim_time`: Total simulation time
- `random_seed`: Fixed seed for reproducibility

### 2. `get_workorder_details`
Retrieves detailed tracking information about a workorder's journey through production lines.

**Parameters:**
- `workorder_number`: Unique identifier of the workorder

**Returns:** Comprehensive workorder details including production lines, timing, and status.

### 3. `get_workorder_configuration`
Retrieves planned/configured settings and timing for production lines.

**Parameters:**
- `workorder_number`: Unique identifier of the workorder

**Returns:** Line configurations, capacity specifications, and priority levels.

## 🏭 Production Lines

The system supports the following production lines:

| Line Name | Type | Description |
|-----------|------|-------------|
| 1200REI | Manufacturing | Primary manufacturing line |
| 1200GR35 | Manufacturing | Secondary manufacturing line |
| MH | Material Handling | Material movement and logistics |
| QC | Quality Control | Quality inspection and testing |
| Assembly | Assembly | Product assembly operations |
| Packaging | Packaging | Product packaging and preparation |
| Shipping | Logistics | Final shipping and delivery |

## 🔄 Data Consistency

- **Same workorder number** = **Same number of production lines**
- **Same workorder number** = **Same line names**
- **Different timing values** between actual processing and configured time
- **Deterministic results** for reproducible testing

## 📊 Use Cases

### Manufacturing Operations
- Track workorder progress through production lines
- Monitor actual vs. planned processing times
- Capacity planning and resource allocation

### AI Agent Integration
- MCP tools for automated manufacturing analysis
- Real-time production monitoring
- Predictive maintenance scheduling

### Simulation Studies
- Queue performance analysis
- Service level optimization
- Resource planning and scaling

## 🧪 Testing

### API Testing
```bash
# Test simulation endpoint
curl -X POST "http://localhost:8000/simulate" \
  -H "Content-Type: application/json" \
  -d '{"n_servers": 2, "arrival_rate": 10.0, "service_time": 2.0, "sim_time": 100}'

# Test workorder details
curl "http://localhost:8000/workorder/WO-2024-001"

# Test workorder configuration
curl "http://localhost:8000/workorder/WO-2024-001/configuration"
```

### MCP Tool Testing
Use any MCP-compatible client to test the tools:
- Claude Desktop
- MCP Studio
- Custom MCP clients

## 🔧 Configuration

### Environment Variables
- `PORT`: Server port (default: 8000)
- `MCP_PORT`: MCP server port (default: 8001)
- `HOST`: Server host (default: 0.0.0.0)

### Customization
- Modify production line configurations in `server.py`
- Adjust simulation parameters in `simulation.py`
- Customize MCP tool responses in `mcp_server.py`

## 📝 API Documentation

Once the server is running, visit:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`
- **OpenAPI schema**: `http://localhost:8000/openapi.json`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the MCP tool descriptions
3. Check the console logs for error messages
4. Open an issue in the repository

## 🔮 Future Enhancements

- [ ] Database integration for persistent storage
- [ ] Real-time WebSocket updates
- [ ] Advanced analytics and reporting
- [ ] Machine learning integration for predictive analytics
- [ ] Multi-tenant support
- [ ] Authentication and authorization
- [ ] Performance monitoring and metrics
