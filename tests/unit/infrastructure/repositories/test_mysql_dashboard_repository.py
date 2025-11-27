import re
import pytest
from datetime import date
from src.infrastructure.repositories.mysql_dashboard_repository import MySQLDashboardRepository

class DummyDB:
    pass

class DummyBrandRepo:
    pass

@pytest.fixture
def repo():
    return MySQLDashboardRepository(DummyDB(), DummyBrandRepo())

def normalize_sql(sql):
    """Remove extra whitespace and line breaks for easier comparison."""
    return re.sub(r"\s+", " ", sql).strip()

@pytest.mark.parametrize(
    "brands,countries,page_types",
    [
        (None, None, None),
        (None, None, ["type1", "type2"]),
        (None, ["ES"], None),
        (["BrandA"], None, None),
        (["BrandA", "BrandB"], ["ES", "FR"], None),
        (["BrandA"], ["ES"], ["type1"]),
        (["BrandA", "BrandB"], None, ["type1", "type2"]),
        (["BrandA"], ["ES"], ["type1", "type2"]),
    ]
)
def test_build_brand_time_series_query_and_params(repo, brands, countries, page_types):
    start_date = date(2023, 1, 1)
    end_date = date(2023, 1, 31)
    device = "desktop"

    query, params = repo._build_brand_time_series_query_and_params(
        start_date, end_date, device, brands, countries, page_types
    )

    # Check that the query contains required SQL parts
    sql = normalize_sql(query)
    assert "SELECT cwv.execution_date, u.brand, AVG(cwv.performance_score) as avg_performance_score" in sql
    assert "FROM url_core_web_vitals cwv INNER JOIN urls u ON cwv.url_id = u.url_id" in sql
    assert "WHERE cwv.execution_date BETWEEN %s AND %s AND u.device = %s AND cwv.performance_score IS NOT NULL" in sql
    if brands:
        assert "AND u.brand IN" in sql
    assert "GROUP BY cwv.execution_date, u.brand" in sql
    assert "ORDER BY cwv.execution_date ASC, u.brand ASC" in sql

    # Check that the number of %s matches the number of params
    num_placeholders = sql.count("%s")
    assert num_placeholders == len(params)

    # Check that params are in the expected order
    expected_params = [start_date, end_date, device]
    if brands:
        expected_params += brands
    if countries:
        expected_params += countries
    if page_types:
        expected_params += page_types
    assert params == expected_params