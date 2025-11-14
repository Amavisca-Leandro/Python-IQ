"""
UI automation components for Playwright-based frontend testing.

This module provides Page Object Model (POM) components for frontend automation:
- BasePage: Base class with common functionality
- Specific page objects for different pages (LoginPage, DashboardPage, etc.)
"""

from core.ui.base_page import BasePage
from core.ui.pages.login_page import LoginPage
from core.ui.pages.dashboard_page import DashboardPage
from core.ui.pages.user_profile_page import UserProfilePage

__all__ = [
    "BasePage",
    "LoginPage",
    "DashboardPage",
    "UserProfilePage",
]
