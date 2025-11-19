"""Data Transfer Object for execution summary."""
from dataclasses import dataclass, field
from datetime import date
from typing import List, Dict


@dataclass
class URLExecutionResult:
    """Result of processing a single URL."""
    url_id: int
    url: str
    success: bool
    error_message: str = ""


@dataclass
class ExecutionSummary:
    """Summary of the data collection job execution."""
    execution_date: date
    total_urls: int
    successful: int = 0
    failed: int = 0
    skipped: int = 0
    results: List[URLExecutionResult] = field(default_factory=list)

    def add_success(self, url_id: int, url: str) -> None:
        """
        Record a successful URL processing.

        Args:
            url_id: URL identifier
            url: URL string
        """
        self.successful += 1
        self.results.append(
            URLExecutionResult(url_id=url_id, url=url, success=True)
        )

    def add_failure(self, url_id: int, url: str, error_message: str) -> None:
        """
        Record a failed URL processing.

        Args:
            url_id: URL identifier
            url: URL string
            error_message: Error description
        """
        self.failed += 1
        self.results.append(
            URLExecutionResult(
                url_id=url_id,
                url=url,
                success=False,
                error_message=error_message
            )
        )

    def add_skipped(self, url_id: int, url: str) -> None:
        """
        Record a skipped URL (already has data).

        Args:
            url_id: URL identifier
            url: URL string
        """
        self.skipped += 1

    def get_failed_urls(self) -> List[URLExecutionResult]:
        """Get list of failed URL results."""
        return [r for r in self.results if not r.success]

    def get_successful_urls(self) -> List[URLExecutionResult]:
        """Get list of successful URL results."""
        return [r for r in self.results if r.success]

    def to_dict(self) -> Dict:
        """Convert summary to dictionary."""
        return {
            'execution_date': str(self.execution_date),
            'total_urls': self.total_urls,
            'successful': self.successful,
            'failed': self.failed,
            'skipped': self.skipped,
            'success_rate': f"{(self.successful / self.total_urls * 100):.1f}%" if self.total_urls > 0 else "0%",
        }
