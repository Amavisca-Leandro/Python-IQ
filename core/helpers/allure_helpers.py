"""Allure reporting helpers and utilities."""

import json
import logging
import functools
from typing import Any, Callable, Optional, Dict
from pathlib import Path

import allure
import requests
from allure_commons.types import AttachmentType

logger = logging.getLogger(__name__)


def allure_step(step_title: str) -> Callable:
    """Decorator to create Allure steps with custom titles."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            formatted_title = step_title
            try:
                formatted_title = step_title.format(**kwargs)
            except (KeyError, IndexError):
                try:
                    formatted_title = step_title.format(*args)
                except (KeyError, IndexError):
                    pass
            
            with allure.step(formatted_title):
                logger.info(f"Executing step: {formatted_title}")
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    logger.error(f"Step failed: {formatted_title} - {str(e)}")
                    raise
        return wrapper
    return decorator


def attach_request_response(
    response: requests.Response,
    request_name: str = "HTTP Request",
    response_name: str = "HTTP Response"
) -> None:
    """Attach HTTP request and response details to Allure report."""
    request_data = {
        "method": response.request.method,
        "url": response.request.url,
        "headers": dict(response.request.headers),
        "body": _get_request_body(response.request)
    }
    
    allure.attach(
        json.dumps(request_data, indent=2, ensure_ascii=False),
        name=request_name,
        attachment_type=AttachmentType.JSON
    )
    
    response_data = {
        "status_code": response.status_code,
        "reason": response.reason,
        "headers": dict(response.headers),
        "body": _get_response_body(response),
        "elapsed_ms": response.elapsed.total_seconds() * 1000
    }
    
    allure.attach(
        json.dumps(response_data, indent=2, ensure_ascii=False),
        name=response_name,
        attachment_type=AttachmentType.JSON
    )
    logger.debug(f"Attached request/response for {response.request.method} {response.request.url}")


def _get_request_body(request: requests.PreparedRequest) -> Any:
    """Extract request body."""
    if not request.body:
        return None
    try:
        if isinstance(request.body, bytes):
            return json.loads(request.body.decode('utf-8'))
        elif isinstance(request.body, str):
            return json.loads(request.body)
        else:
            return str(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return str(request.body)


def _get_response_body(response: requests.Response) -> Any:
    """Extract response body."""
    try:
        return response.json()
    except (json.JSONDecodeError, ValueError):
        return response.text if response.text else None


def attach_screenshot(screenshot_bytes: bytes, name: str = "Screenshot") -> None:
    """Attach a screenshot to the Allure report."""
    allure.attach(screenshot_bytes, name=name, attachment_type=AttachmentType.PNG)
    logger.debug(f"Attached screenshot: {name}")


def attach_json(data: Dict[str, Any], name: str = "JSON Data") -> None:
    """Attach JSON data to the Allure report."""
    allure.attach(
        json.dumps(data, indent=2, ensure_ascii=False),
        name=name,
        attachment_type=AttachmentType.JSON
    )
    logger.debug(f"Attached JSON: {name}")


def set_environment_info(env_data: Dict[str, str]) -> None:
    """Set environment information for the Allure report."""
    allure_results_dir = Path("reports/allure-results")
    allure_results_dir.mkdir(parents=True, exist_ok=True)
    env_file = allure_results_dir / "environment.properties"
    with open(env_file, 'w', encoding='utf-8') as f:
        for key, value in env_data.items():
            f.write(f"{key}={value}\n")
    logger.info(f"Environment information saved to {env_file}")


def add_jira_link(issue_key: str) -> None:
    """Add a link to a Jira issue."""
    allure.dynamic.link(issue_key, link_type='issue', name=f"Jira: {issue_key}")


def add_test_case_link(test_case_id: str) -> None:
    """Add a link to a test case."""
    allure.dynamic.link(test_case_id, link_type='tms', name=f"Test Case: {test_case_id}")
