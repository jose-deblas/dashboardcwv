"""Dependency Injection container configuration."""
from dependency_injector import containers, providers

from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.repositories.mysql_url_repository import MySQLURLRepository
from src.infrastructure.repositories.mysql_core_web_vitals_repository import (
    MySQLCoreWebVitalsRepository,
)
from src.infrastructure.api.pagespeed.auth.pagespeed_auth_provider import (
    PageSpeedAuthProvider,
)
from src.infrastructure.api.pagespeed.http.pagespeed_http_client import (
    PageSpeedHTTPClient,
)
from src.infrastructure.api.pagespeed.mappers.pagespeed_mapper import PageSpeedMapper
from src.infrastructure.api.pagespeed.pagespeed_client_facade import (
    PageSpeedClientFacade,
)
from src.application.use_cases.collect_pagespeed_data_use_case import (
    CollectPageSpeedDataUseCase,
)


class Container(containers.DeclarativeContainer):
    """Dependency injection container for Core Web Vitals application."""

    # Configuration
    config = providers.Configuration()

    # Database
    database_connection = providers.Singleton(
        DatabaseConnection,
        host=config.database.host,
        port=config.database.port,
        database=config.database.name,
        user=config.database.user,
        password=config.database.password,
    )

    # Repositories
    url_repository = providers.Factory(
        MySQLURLRepository,
        db_connection=database_connection,
    )

    core_web_vitals_repository = providers.Factory(
        MySQLCoreWebVitalsRepository,
        db_connection=database_connection,
    )

    # PageSpeed API
    pagespeed_auth_provider = providers.Singleton(
        PageSpeedAuthProvider,
        api_key=config.pagespeed.api_key,
    )

    pagespeed_http_client = providers.Factory(
        PageSpeedHTTPClient,
        auth_provider=pagespeed_auth_provider,
        max_retries=config.pagespeed.max_retries,
        initial_backoff=config.pagespeed.initial_backoff,
        backoff_multiplier=config.pagespeed.backoff_multiplier,
        timeout=config.pagespeed.timeout,
    )

    pagespeed_mapper = providers.Singleton(PageSpeedMapper)

    pagespeed_client = providers.Factory(
        PageSpeedClientFacade,
        auth_provider=pagespeed_auth_provider,
        http_client=pagespeed_http_client,
        mapper=pagespeed_mapper,
    )

    # Use Cases
    collect_pagespeed_data_use_case = providers.Factory(
        CollectPageSpeedDataUseCase,
        url_repository=url_repository,
        cwv_repository=core_web_vitals_repository,
        pagespeed_client=pagespeed_client,
    )
