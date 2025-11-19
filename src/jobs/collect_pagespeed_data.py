"""
Data Collection Job - PageSpeed Insights API

This job collects Core Web Vitals data from the PageSpeed Insights API
for URLs stored in the database.
"""
import os
import sys
from datetime import date

from src.infrastructure.logging.logger_config import setup_logging, get_logger
from src.infrastructure.di.container import Container


# Setup logging
setup_logging(log_level='INFO', log_to_file=True, log_to_console=True)
logger = get_logger(__name__)


def main() -> None:
    """Main job execution - thin orchestrator."""
    print("=" * 60)
    print("Core Web Vitals - PageSpeed Data Collection Job")
    print("=" * 60)
    print()

    # Validate prerequisites
    if not _validate_prerequisites():
        sys.exit(1)

    # Configure and wire dependencies
    container = _setup_container()

    # Execute use case
    execution_date = date.today()
    logger.info(f"Starting data collection for {execution_date}")

    try:
        use_case = container.collect_pagespeed_data_use_case()
        summary = use_case.execute(execution_date)

        # Print summary
        _print_summary(summary)

        # Exit with appropriate code
        sys.exit(0 if summary.failed == 0 else 1)

    except Exception as e:
        logger.error(f"Job failed with error: {e}", exc_info=True)
        print(f"\n❌ ERROR: {e}")
        print("=" * 60)
        sys.exit(1)


def _validate_prerequisites() -> bool:
    """Validate that all prerequisites are met."""
    api_key = os.getenv("PAGESPEED_INSIGHTS_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("❌ ERROR: PAGESPEED_INSIGHTS_API_KEY not configured")
        print("Please set your API key in the .env file")
        print()
        print("Get your API key from:")
        print("https://developers.google.com/speed/docs/insights/v5/get-started")
        return False

    db_host = os.getenv("MYSQL_HOST", "mysql")
    db_name = os.getenv("MYSQL_DATABASE", "core_web_vitals")

    print(f"Database: {db_name} @ {db_host}")
    print(f"API Key: {'*' * 20}{api_key[-4:]}")
    print()

    return True


def _setup_container() -> Container:
    """Setup and configure the dependency injection container."""
    container = Container()

    # Configure from environment variables
    container.config.database.host.from_env("MYSQL_HOST", default="mysql")
    container.config.database.port.from_env("MYSQL_PORT", default=3306)
    container.config.database.name.from_env("MYSQL_DATABASE", default="core_web_vitals")
    container.config.database.user.from_env("MYSQL_USER", default="cwv_user")
    container.config.database.password.from_env("MYSQL_PASSWORD", default="cwv_password")

    container.config.pagespeed.api_key.from_env("PAGESPEED_INSIGHTS_API_KEY")
    container.config.pagespeed.max_retries.from_value(3)
    container.config.pagespeed.initial_backoff.from_value(1.0)
    container.config.pagespeed.backoff_multiplier.from_value(2.0)
    container.config.pagespeed.timeout.from_value(60)

    return container


def _print_summary(summary) -> None:  # type: ignore
    """Print execution summary."""
    print()
    print("=" * 60)
    print("Execution Summary")
    print("=" * 60)
    print(f"Date: {summary.execution_date}")
    print(f"Total URLs: {summary.total_urls}")
    print(f"✅ Successful: {summary.successful}")
    print(f"❌ Failed: {summary.failed}")
    print(f"⏭️  Skipped: {summary.skipped}")
    print()

    if summary.failed > 0:
        print("Failed URLs:")
        for result in summary.get_failed_urls():
            print(f"  - URL {result.url_id}: {result.url}")
            print(f"    Error: {result.error_message}")
        print()

    success_rate = (summary.successful / summary.total_urls * 100) if summary.total_urls > 0 else 0
    print(f"Success Rate: {success_rate:.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    main()
