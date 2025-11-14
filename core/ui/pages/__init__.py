"""
Specific Page Objects for the application.

This module contains page-specific implementations:
- LoginPage: Login page interactions
- DashboardPage: Dashboard navigation and validations
- UserProfilePage: User profile management
"""

from core.ui.pages.login_page import LoginPage
from core.ui.pages.dashboard_page import DashboardPage
from core.ui.pages.user_profile_page import UserProfilePage

__all__ = [
    "LoginPage",
    "DashboardPage",
    "UserProfilePage",
]
