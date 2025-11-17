# app-specs.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Core Web Vitals Dashboard built with Python and MySQL.

The project use Docker and the first time we install it in a server or computer the database won't exist, therefore, the Docker installation will provide a MySQL server.
The file @database/cwv_database.sql provides the queries to create the database and its tables.
We'll have a MAKEFILE with the usual options needed: install, up, down, pull, etc.
The project will use uv for python dependencies.
The project will have a README.md file with all the explanation to install the app in local for developers.

The project is divided in two parts: Data Collection and Dashboard

### Data Collection

We'll have a part to make jobs that in the future could be executed, for example, from a jenkins server.
The only job that we have now is in charge of collecting the data through the PageSpeed Insights API.
So that, the job will take the urls from the 'urls' table. 
For each one, we'll call the PageSpeed Insights API passing also the url and the device.
We'll insert the core web vitals data in the table 'url_core_web_vitals'
If for some reason the script fails, some urls will last without data. So that, if we execute the script again, we'll just use those urls without data in 'url_core_web_vitals' to avoid losing execution time.

### Dashboard

The Dashboard will work separetly of the jobs.
We'll use Streamlit, the python library to build Dashboards.
The Dashboard will have a lateral menu. For now, it will have an option called Overview which is the default dashboard view and therefore will be selected.
The Dashboard have to be made with responsive design.
The design have to be modern and spectacular.
Make a Dark mode button at the end of the lateral menu where the highlight color (for example for headers) will be #a7f9ab

The Overview will have a complete horizontal form in the top to update what we want to see in the Dashboard.
We can Choose:
* Start Date and End Date. Two dates that will conform the chosen time period. By default, the End Date is the last execution Date and the Start Date the first execution date (`url_core_web_vitals.execution_date`)
* Page Type. We can filter by the url.page_type field
* Country. We can filter by the countries at url.country_id
* Core Web Vital. We can filter by one of the many core web vital that we have at the table url_core_web_vitals.

All the fields will affect to the rest of the Dashboard Overview where we'll have:

1.1. Performance

We'll have the data for two brands, CUPRA and SEAT.
For each of both the last Performance Score for the Mobile and Desktop Devices average will be shown.
For each Performance Score we will have the data: Initial period, selected period, difference and goal.
The goal is represented by a constant called PERFORMANCE_GOAL_VALUE. Initially has the number 70.
We'll play with the design as traffic lights: green positive, red negative and amber. 
These numbers are the main numbers and have to have presence.

Under this initial part, we'll see a chart with the evolution of the selected core web vital (performance score by default) for CUPRA Mobile, CUPRA Desktop, SEAT Mobile and SEAT Desktop average.
Remember to adapt the values depending on what the user selects in the top form: Page Type, Country or Core Web Vital KPI

Remember that all the data here should be an average because what we show is not about a unique URL, is about groups of urls. This should be took into account when designing how we request the data to the database.

## Architecture

This project follows Clean Architecture with strict separation of concerns and dependency inversion:

### Key Architectural Principles

1. **Dependency Inversion**: All layers depend on abstractions (interfaces), not concretions
2. **Separation of Concerns**: Each component has ONE responsibility
   - Auth providers: Handle authentication/credentials
   - HTTP clients: Handle HTTP transport
   - Mappers: Convert API responses to domain models
   - Repositories: Handle data persistence
   - Use cases: Orchestrate business workflows
   - Services: Contain domain business logic

3. **Dependency Injection**: All dependencies are injected via constructors using `dependency-injector` library

4. **Clean Interfaces**: Facade pattern provides simple, domain-focused APIs:

## Layer Details

### Domain Layer

Pure business logic with NO external dependencies

### Application Layer

Use cases that orchestrate business workflows:

- Each use case depends on INTERFACES (not implementations)
- Receives injected dependencies via constructor

### Infrastructure Layer

Implementations of domain interfaces

**API Client Structure** (for each external API):
```
auth/*_auth_provider.py      → Handles authentication
http/*_http_client.py        → Handles HTTP calls
mappers/*_mapper.py          → Maps API responses to domain models
*_client_facade.py           → Combines above 3 components
```

### Jobs Layer (`src/jobs/`)

Thin orchestration layer - each job:
1. Checks prerequisites (e.g., credentials file exists)
2. Resolves use case from DI container (or accepts injected)
3. Executes use case
4. Prints summary

Jobs are 20-30 lines max, all logic is in use cases.

## Dependency Injection

**Container**
- Uses `dependency-injector` library
- Wires ALL dependencies automatically
- Loads configuration from environment variables
- Single source of truth for object creation

## Configuration

Environment variables in `.env` (copy from `.env.example`):

**Database**:
- `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`

**API Authentication**:
- `PAGESPEED_INSIGHTS_API_KEY`

## Database Schema

Tables in `database/cwv_database.sql`:

## Testing Strategy

Tests use dependency injection for easy mocking

## Key Implementation Patterns

### 1. Value Objects for Domain Concepts
```python
from src.domain.value_objects import DomainURL, DateRange

# Automatic protocol handling
domain_url = DomainURL.from_domain_name("example.com")  # → https://example.com
encoded = domain_url.url_encoded()  # → URL-encoded for API

# Validated date ranges
date_range = DateRange(start_date, end_date)  # Validates start < end
start, end = date_range.to_iso_strings()  # Convert to ISO format
```

### 2. Repository Pattern
```python
# Application layer depends on interface
class CollectGSCDataUseCase:
    def __init__(self, gsc_repository: GSCClicksRepository):  # ABC interface
        self._repository = gsc_repository

# Infrastructure provides implementation
class MySQLGSCClicksRepository(GSCClicksRepository):  # Concrete class
    def add(self, clicks: GSCClicks) -> None:
        # SQL implementation
```

### 3. Facade Pattern for Clean APIs
```python
# Instead of exposing HTTP/auth details:
auth = GSCAuthProvider(credentials_file)
http = GSCHttpClient(auth)
mapper = GSCResponseMapper()
response = http.query_search_analytics(...)
data = mapper.map_response(response)

# Use facade with domain-focused interface:
facade = GSCClientFacade(auth, http, mapper)
data = facade.fetch_performance(domain_url, date_range)  # Clean!
```

### 4. Use Cases for Business Workflows

## Common Mistakes to Avoid

❌ **Don't** instantiate dependencies inside classes:
```python
class UseCase:
    def __init__(self):
        self._client = GSCClient()  # BAD - tight coupling
```

✅ **Do** inject dependencies via constructor:
```python
class UseCase:
    def __init__(self, client: GSCClientFacade):  # GOOD - injected
        self._client = client
```

❌ **Don't** mix concerns (e.g., HTTP + mapping in one class)

✅ **Do** separate authentication, transport, and mapping

❌ **Don't** return raw API responses (`Dict[str, Any]`)

✅ **Do** return domain models (`List[GSCClicks]`)

❌ **Don't** put business logic in jobs or infrastructure

✅ **Do** put business logic in domain services and use cases

## Development Workflow

1. **Make changes to domain layer first** (models, services, value objects)
2. **Update repository interfaces** if data access changes
3. **Implement infrastructure changes** (repositories, clients, mappers)
4. **Update use cases** with new business workflows
5. **Update jobs** if needed (usually no changes needed)
6. **Rebuild container** to reflect new dependencies
7. **Write tests** at use case level with mocked dependencies

## References

- Clean Architecture: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- Dependency Injection in Python: https://python-dependency-injector.ets-labs.org/
- Repository Pattern: https://martinfowler.com/eaaCatalog/repository.html
- Value Objects: https://martinfowler.com/bliki/ValueObject.html
