"""
Presentation layer for the dashboard application.

This layer contains framework-agnostic presentation logic including:
- View Models: Presentation-ready data structures
- Presenters: Transform DTOs into View Models
- Chart Builders: Framework-agnostic chart configuration
- State Abstractions: State management interfaces

This layer sits between the Application layer (use cases, DTOs) and the
UI layer (Streamlit components, HTML templates, etc.).
"""
