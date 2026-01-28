# Dashboard Architecture

## Overview

The dashboard follows **Clean Architecture** principles with a clear separation between business logic, presentation logic, and UI rendering. This architecture enables support for multiple frontends (Streamlit, HTML templates, React, REST APIs) without rewriting business logic.

## Architecture Layers

```
┌─────────────────────────────────────┐
│   UI Layer (Streamlit/HTML/React)  │  ← Framework-specific rendering
│   - Streamlit components           │
│   - HTML templates                 │
│   - React components               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Adapters (Bridge Pattern)         │  ← Framework-specific implementations
│   - StreamlitStateAdapter           │
│   - StreamlitChartAdapter           │
│   - (Future: FlaskStateAdapter)     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Presentation Layer (NEW)          │  ← Framework-agnostic presentation
│   - View Models                     │
│   - Presenters                      │
│   - Chart Builder                   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Application Layer                 │  ← Business workflows
│   - Use Cases                       │
│   - Pure DTOs                       │
│   - Validators                      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Domain Layer                      │  ← Core business logic
│   - Entities                        │
│   - Repository Interfaces           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Infrastructure Layer              │  ← External integrations
│   - MySQL Repositories              │
│   - API Clients                     │
│   - DI Container                    │
└─────────────────────────────────────┘
```

## Key Components

### 1. Presentation Layer (`src/presentation/`)

**Purpose**: Framework-agnostic presentation logic.

#### View Models (`presentation/models/`)

Immutable dataclasses containing pre-formatted, presentation-ready data:

- `PerformanceViewModel` - Performance metrics with pre-calculated deltas, growth rates
- `CompetitorViewModel` - Rankings with medals and highlighting
- `FilterOptionsViewModel` - Filter options with "All" prefixes
- `ChartViewModel` - Framework-agnostic chart configuration

**Key characteristics**:
- All values are pre-formatted strings (e.g., "+5.20%", "N/A")
- Colors are semantic names ("green", "red", "neutral")
- No framework-specific code
- Immutable (frozen dataclasses)

#### Presenters (`presentation/presenters/`)

Transform DTOs into view models. Contains ALL presentation logic:

```python
# Example: PerformancePresenter
class PerformancePresenter:
    TARGET_MOBILE = 65
    TARGET_DESKTOP = 80

    def present(self, performance_metrics, mobile_ts, desktop_ts):
        # Calculate delta
        delta = end_score - start_score

        # Calculate growth rate
        growth_rate = (delta / start_score) * 100

        # Determine color
        color = "green" if delta > 0 else "red" if delta < 0 else "neutral"

        # Format values
        formatted_delta = f"+{delta:.2f}" if delta > 0 else f"{delta:.2f}"

        return DeviceMetricsViewModel(...)
```

**Responsibilities**:
- Delta calculations
- Growth rate calculations
- Color determination
- Value formatting
- Target value application

#### Chart Builder (`presentation/charts/`)

Creates framework-agnostic chart configurations:

```python
chart_builder = ChartBuilder(red_threshold=40, green_threshold=60)
chart_vm = chart_builder.build_performance_evolution_chart(
    mobile_data, desktop_data
)
# Returns ChartViewModel that can be rendered by any charting library
```

### 2. Adapters Layer (`src/dashboard/adapters/`)

**Purpose**: Bridge between presentation layer and specific UI frameworks.

#### StreamlitStateAdapter

Wraps `st.session_state` with framework-agnostic interface:

```python
state = StreamlitStateAdapter()
state.set_filter_criteria(criteria)
criteria = state.get_filter_criteria()
```

#### StreamlitChartAdapter

Converts `ChartViewModel` to Plotly figures:

```python
adapter = StreamlitChartAdapter()
fig = adapter.render_chart(chart_vm)  # Returns Plotly Figure
st.plotly_chart(fig)
```

### 3. Application Layer (`src/application/`)

#### DTOs (Data Transfer Objects)

Pure data containers with NO presentation logic:

```python
@dataclass(frozen=True)
class DeviceMetrics:
    """Pure data container - no presentation logic."""
    device: str
    start_score: Optional[float]
    end_score: Optional[float]
    # No delta, growth_rate, or target properties!
```

#### Validators (`application/validation/`)

Business validation extracted from DTOs and components:

```python
validator = FilterValidator()
try:
    validator.validate_date_range(start_date, end_date)
except FilterValidationError as e:
    st.error(str(e))
```

### 4. UI Components (`src/dashboard/components/`)

**Pure renderers** that consume view models:

```python
def render_device_metrics(device_vm: DeviceMetricsViewModel):
    """Pure rendering - all data pre-formatted."""
    st.metric(device_vm.target_card.label, device_vm.target_card.value)
    st.metric(device_vm.end_date_card.label, device_vm.end_date_card.value,
              delta=device_vm.end_date_card.delta)
    # No calculations, no formatting - just rendering!
```

## Data Flow

### Current Flow (with Presentation Layer)

```
1. User interacts with UI
   ↓
2. UI calls use case (business logic)
   ↓
3. Use case returns DTO (pure business data)
   ↓
4. Presenter transforms DTO → View Model
   - Calculates delta, growth rate
   - Determines colors
   - Formats values
   ↓
5. Component renders View Model
   - Pure rendering, no logic
```

### Example: Performance Metrics

```python
# 1. Fetch business data
performance_metrics = get_performance_data_use_case.execute(criteria)
# Returns: DeviceMetrics(device="mobile", start_score=60.0, end_score=65.0)

# 2. Transform to presentation
performance_presenter = PerformancePresenter()
performance_vm = performance_presenter.present(performance_metrics, ...)
# Returns: DeviceMetricsViewModel(
#     device_label="Mobile",
#     end_date_card=MetricCardViewModel(
#         label="End Date",
#         value="65.00",
#         delta="+5.00",
#         delta_color="green"
#     ),
#     growth_rate_display="+8.33%",
#     growth_rate_color="green",
#     ...
# )

# 3. Render
render_device_metrics(performance_vm)
```

## Benefits

### 1. Multiple Frontend Support

80%+ code reuse when adding new frontends:

**Adding a REST API:**
```python
@app.get("/api/performance")
def get_performance():
    # Reuse use case
    metrics = get_performance_data_use_case.execute(criteria)

    # Reuse presenter
    vm = performance_presenter.present(metrics, ...)

    # Serialize view model to JSON
    return jsonable_encoder(vm)
```

**Adding HTML Templates:**
```python
@app.route("/dashboard")
def dashboard():
    # Reuse use case
    metrics = get_performance_data_use_case.execute(criteria)

    # Reuse presenter
    vm = performance_presenter.present(metrics, ...)

    # Pass to Jinja template
    return render_template("dashboard.html", performance=vm)
```

### 2. Better Testability

Presentation logic isolated and independently testable:

```python
def test_presenter_calculates_delta():
    presenter = PerformancePresenter()
    metrics = DeviceMetrics(device="mobile", start_score=50.0, end_score=60.0)

    vm = presenter._present_device_metrics(metrics, "Mobile", 65)

    assert vm.end_date_card.delta == "+10.00"
    assert vm.end_date_card.delta_color == "green"
    assert vm.growth_rate_display == "+20.00%"
```

### 3. Cleaner Code

Components become pure renderers:

**Before:**
```python
# Component had calculation logic
delta = device_metrics.end_score - device_metrics.start_score
growth_rate = (delta / device_metrics.start_score) * 100
color = "green" if growth_rate > 0 else "red"
st.metric(label, value, delta, color)
```

**After:**
```python
# Component just renders pre-formatted data
st.metric(
    device_vm.end_date_card.label,
    device_vm.end_date_card.value,
    device_vm.end_date_card.delta
)
```

### 4. Single Source of Truth

All presentation calculations in one place (presenters), not scattered across:
- DTO properties
- Component inline logic
- Helper functions

## Design Patterns Used

1. **Presentation Adapter Pattern**: Adapters bridge presentation layer and UI frameworks
2. **Model-View-Presenter (MVP)**: Presenters mediate between DTOs and View Models
3. **Data Transfer Object (DTO)**: Pure data containers for layer communication
4. **Repository Pattern**: Abstract data access (existing)
5. **Dependency Injection**: Wire dependencies through container (existing)

## Migration Path

To add a new frontend (e.g., React):

1. **Reuse existing layers** (no changes):
   - Use Cases
   - DTOs
   - Presenters
   - Domain
   - Infrastructure

2. **Create new adapters**:
   - `ReactStateAdapter` (use Redux/Context)
   - `ReactChartAdapter` (use Recharts/Victory)

3. **Create React components**:
   - Consume same view models
   - No business logic duplication

4. **Expose REST API** (optional):
   - Serialize view models to JSON
   - React fetches from API

## File Structure

```
src/
├── presentation/              # NEW: Framework-agnostic presentation
│   ├── models/               # View models
│   ├── presenters/           # DTO → View Model transformers
│   ├── charts/               # Chart builders
│   └── state/                # State abstractions
│
├── dashboard/                # Streamlit-specific UI
│   ├── adapters/             # NEW: Streamlit adapters
│   ├── components/           # REFACTORED: Pure renderers
│   └── main.py              # REFACTORED: Uses presenters
│
├── application/              # Business workflows
│   ├── dto/                 # REFACTORED: Pure DTOs
│   ├── use_cases/           # Use cases (unchanged)
│   └── validation/          # NEW: Business validators
│
├── domain/                   # Core business (unchanged)
├── infrastructure/           # External integrations
│   └── di/container.py      # UPDATED: Register presenters
```

## Testing Strategy

### Unit Tests

1. **Presenters** (100% coverage):
   - Test delta calculations
   - Test growth rate calculations
   - Test color determination
   - Test formatting
   - Test edge cases (None, zero division)

2. **Validators** (100% coverage):
   - Test validation rules
   - Test error messages

3. **View Models**:
   - Basic instantiation tests

4. **Adapters**:
   - Test framework wrapping
   - Test chart conversion

### Integration Tests

- End-to-end dashboard flow
- Verify presenters work with real DTOs
- Verify adapters work with real charts

## Future Enhancements

Once decoupled, easily implement:

1. **REST API Frontend**
2. **HTML Templates (Flask/Django)**
3. **React/Vue Frontend**
4. **PDF Report Generator**
5. **CLI Dashboard**

All without changing use cases or domain layer!
