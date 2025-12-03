# Core Web Vitals Dashboard

A comprehensive dashboard for monitoring and analyzing Core Web Vitals metrics using PageSpeed Insights API data.

## Overview

This project provides a complete solution for collecting and visualizing Core Web Vitals data:

- **Data Collection**: Automated jobs to fetch Core Web Vitals data from PageSpeed Insights API
- **Dashboard**: Interactive Streamlit-based web interface for data visualization
- **Database**: MySQL database for persistent storage
- **Architecture**: Clean Architecture with strict separation of concerns

## Features

- 📊 Interactive dashboard with real-time metrics
- 🔄 Automated data collection from PageSpeed Insights API
- 🎨 Modern, responsive design with dark mode support
- 📈 Performance tracking for multiple brands, devices, and countries
- 🐳 Fully containerized with Docker
- 🏗️ Clean Architecture principles
- 🔌 Dependency injection for testability

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10 or later)
- **Docker Compose** (version 2.0 or later)
- **Make** (optional, but recommended for easier commands)
- **Git**

### Getting a PageSpeed Insights API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the PageSpeed Insights API
4. Create credentials (API Key)
5. Copy your API key for use in the `.env` file

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jose-deblas/dashboardcwv
cd dashboardcwv
```

### 2. Initial Setup

Run the installation command to set up the environment:

```bash
make install
```

This will:
- Create a `.env` file from `.env.example`
- Create necessary directories
- Build Docker images

### 3. Configure Environment Variables

Edit the `.env` file and update the following values:

```bash
# REQUIRED: Set your PageSpeed Insights API key
PAGESPEED_INSIGHTS_API_KEY=your_actual_api_key_here

# Database credentials (optional - defaults are fine for development)
MYSQL_USER=cwv_user
MYSQL_PASSWORD=cwv_password
MYSQL_ROOT_PASSWORD=rootpassword

# Application settings
PERFORMANCE_GOAL_VALUE=70
```

### 4. Start the Services

```bash
make up
```

This will start:
- MySQL database (port 3306)
- Streamlit dashboard (port 8501)

### 5. Access the Dashboard

Open your browser and navigate to:

```
http://localhost:8501
```

## Usage

### Common Commands

The `Makefile` provides convenient commands for managing the application:

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Initial setup and installation |
| `make up` | Start MySQL and Dashboard services |
| `make down` | Stop all services |
| `make build` | Build/rebuild Docker images |
| `make logs` | View logs from all services |
| `make restart` | Restart all services |
| `make status` | Show status of all services |
| `make clean` | Remove all containers, volumes, and images |

### Running Data Collection Jobs

To collect Core Web Vitals data from PageSpeed Insights API:

```bash
make run-job JOB=collect_pagespeed_data
```

### Accessing Service Shells

**Dashboard container:**
```bash
make dashboard-shell
```

**Jobs container:**
```bash
make jobs-shell
```

**MySQL shell:**
```bash
make mysql-shell
```

### Viewing Logs

View logs from all services:
```bash
make logs
```

View logs from a specific service:
```bash
make logs SERVICE=dashboard
make logs SERVICE=mysql
```

## Project Structure

```
dashboardcwv/
├── database/
│   └── cwv_database.sql          # Database schema and initialization
├── src/
│   ├── dashboard/                # Streamlit dashboard application
│   │   ├── __init__.py
│   │   └── main.py              # Main dashboard entry point
│   ├── jobs/                     # Data collection jobs
│   │   ├── __init__.py
│   │   └── collect_pagespeed_data.py
│   ├── domain/                   # Business logic and domain models
│   ├── application/              # Use cases and workflows
│   └── infrastructure/           # External integrations and repositories
├── tests/                        # Test suite
├── docker-compose.yml           # Docker services configuration
├── Dockerfile                   # Application container image
├── Makefile                     # Development commands
├── pyproject.toml              # Python dependencies (uv)
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## Architecture

This project follows **Clean Architecture** principles:

- **Domain Layer**: Pure business logic with no external dependencies
- **Application Layer**: Use cases that orchestrate business workflows
- **Infrastructure Layer**: External integrations (APIs, database)
- **Jobs Layer**: Thin orchestration for scheduled tasks
- **Dashboard Layer**: Streamlit UI for data visualization

### Key Design Patterns

- **Dependency Injection**: Using `dependency-injector` library
- **Repository Pattern**: For data access abstraction
- **Facade Pattern**: Clean APIs for external services
- **Value Objects**: For domain concepts (URLs, date ranges)

## Development

### Running Tests

```bash
make test
```

### Code Formatting

```bash
make format
```

### Linting

```bash
make lint
```

### Adding New Dependencies

Edit `pyproject.toml` and rebuild the Docker images:

```bash
make build
```

## Database Schema

The MySQL database includes the following tables:

- **urls**: Stores URLs with metadata (brand, device, country, page type)
- **url_core_web_vitals**: Core Web Vitals measurements
- **milestones**: Project milestone dates for tracking
- **teams**: Team information
- **countries**: Country reference data

## Troubleshooting

### Services won't start

1. Check if ports 3306 and 8501 are already in use:
   ```bash
   lsof -i :3306
   lsof -i :8501
   ```

2. Check Docker logs:
   ```bash
   make logs
   ```

### Database connection errors

1. Ensure MySQL is healthy:
   ```bash
   make status
   ```

2. Wait for MySQL to fully initialize (first startup can take 30-60 seconds)

### API key errors

Verify your `.env` file has a valid PageSpeed Insights API key:
```bash
cat .env | grep PAGESPEED_INSIGHTS_API_KEY
```

## Contributing

1. Create a feature branch
2. Make your changes following Clean Architecture principles
3. Write tests for new functionality
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details
