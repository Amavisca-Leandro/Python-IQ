"""
Dashboard Page Object for main application navigation.

This module provides the DashboardPage class for handling dashboard interactions
including navigation, menu items, user info, and common dashboard validations.
"""

import logging
from typing import Optional, List

from playwright.sync_api import Page

from core.ui.base_page import BasePage


logger = logging.getLogger(__name__)


class DashboardPage(BasePage):
    """
    Page Object for the Dashboard page.
    
    This class encapsulates all interactions with the dashboard including:
    - Navigation menu
    - User profile dropdown
    - Notifications
    - Search functionality
    - Quick actions
    - Dashboard widgets
    
    Example:
        >>> dashboard = DashboardPage(page)
        >>> dashboard.wait_for_page_load()
        >>> dashboard.navigate_to_profile()
        >>> assert dashboard.get_username() == "Test User"
    """
    
    # ============================================================================
    # LOCATORS
    # ============================================================================
    
    # Page identifiers
    DASHBOARD_CONTAINER = "#dashboard"
    PAGE_TITLE = "h1.dashboard-title"
    
    # Navigation menu
    NAV_MENU = "#nav-menu"
    HOME_LINK = "a[href='/dashboard']"
    PROFILE_LINK = "a[href='/profile']"
    SETTINGS_LINK = "a[href='/settings']"
    USERS_LINK = "a[href='/users']"
    REPORTS_LINK = "a[href='/reports']"
    
    # User dropdown
    USER_DROPDOWN = "#user-dropdown"
    USER_DROPDOWN_TOGGLE = "#user-dropdown-toggle"
    USERNAME_DISPLAY = "#username-display"
    LOGOUT_BUTTON = "#logout-button"
    MY_PROFILE_LINK = "#my-profile-link"
    
    # Search
    SEARCH_INPUT = "#search-input"
    SEARCH_BUTTON = "#search-button"
    SEARCH_RESULTS = ".search-results"
    
    # Notifications
    NOTIFICATION_BELL = "#notification-bell"
    NOTIFICATION_BADGE = ".notification-badge"
    NOTIFICATION_DROPDOWN = "#notification-dropdown"
    NOTIFICATION_ITEM = ".notification-item"
    
    # Quick actions
    QUICK_ACTIONS = "#quick-actions"
    CREATE_NEW_BUTTON = "#create-new"
    UPLOAD_BUTTON = "#upload"
    
    # Dashboard widgets
    WIDGET_CONTAINER = ".widget"
    STATS_WIDGET = "#stats-widget"
    RECENT_ACTIVITY_WIDGET = "#recent-activity"
    
    # Loading indicators
    LOADING_SPINNER = ".loading-spinner"
    SKELETON_LOADER = ".skeleton-loader"
    
    def __init__(self, page: Page, base_url: str = ""):
        """
        Initialize DashboardPage.
        
        Args:
            page: Playwright Page instance
            base_url: Base URL for the application
        """
        super().__init__(page, base_url)
        logger.info("DashboardPage initialized")
    
    # ============================================================================
    # NAVIGATION METHODS
    # ============================================================================
    
    def navigate_to(self, wait_until: str = "networkidle") -> None:
        """
        Navigate to the dashboard page.
        
        Args:
            wait_until: When to consider navigation complete
        """
        super().navigate_to("/dashboard", wait_until=wait_until)
        self.wait_for_page_load()
    
    def wait_for_page_load(self, timeout: Optional[int] = None) -> None:
        """
        Wait for dashboard page to fully load.
        
        Args:
            timeout: Custom timeout in milliseconds
        """
        logger.info("Waiting for dashboard page to load")
        self.wait_for_selector(self.DASHBOARD_CONTAINER, timeout=timeout)
        
        # Wait for loading indicators to disappear
        if self.is_visible(self.LOADING_SPINNER, timeout=1000):
            self.wait_for_selector(self.LOADING_SPINNER, state="hidden", timeout=timeout)
        
        logger.info("Dashboard page loaded")
    
    def navigate_to_profile(self) -> None:
        """
        Navigate to user profile page via menu.
        """
        logger.info("Navigating to profile page")
        self.click(self.PROFILE_LINK)
    
    def navigate_to_settings(self) -> None:
        """
        Navigate to settings page via menu.
        """
        logger.info("Navigating to settings page")
        self.click(self.SETTINGS_LINK)
    
    def navigate_to_users(self) -> None:
        """
        Navigate to users page via menu.
        """
        logger.info("Navigating to users page")
        self.click(self.USERS_LINK)
    
    def navigate_to_reports(self) -> None:
        """
        Navigate to reports page via menu.
        """
        logger.info("Navigating to reports page")
        self.click(self.REPORTS_LINK)
    
    def navigate_to_home(self) -> None:
        """
        Navigate to home/dashboard via menu.
        """
        logger.info("Navigating to home page")
        self.click(self.HOME_LINK)
    
    # ============================================================================
    # USER DROPDOWN METHODS
    # ============================================================================
    
    def open_user_dropdown(self) -> None:
        """
        Open the user dropdown menu.
        """
        logger.info("Opening user dropdown")
        self.click(self.USER_DROPDOWN_TOGGLE)
        self.wait_for_selector(self.USER_DROPDOWN, state="visible")
    
    def close_user_dropdown(self) -> None:
        """
        Close the user dropdown menu.
        """
        logger.info("Closing user dropdown")
        # Click outside or press Escape
        self.press_key("Escape")
    
    def get_username(self) -> str:
        """
        Get the displayed username.
        
        Returns:
            str: Username text
        """
        logger.debug("Getting username")
        return self.get_text(self.USERNAME_DISPLAY)
    
    def logout(self) -> None:
        """
        Logout from the application.
        """
        logger.info("Logging out")
        self.open_user_dropdown()
        self.click(self.LOGOUT_BUTTON)
    
    def go_to_my_profile(self) -> None:
        """
        Navigate to user profile via dropdown.
        """
        logger.info("Going to my profile via dropdown")
        self.open_user_dropdown()
        self.click(self.MY_PROFILE_LINK)
    
    # ============================================================================
    # SEARCH METHODS
    # ============================================================================
    
    def search(self, query: str, submit: bool = True) -> None:
        """
        Perform a search.
        
        Args:
            query: Search query
            submit: Click search button after typing
        """
        logger.info(f"Searching for: {query}")
        self.fill(self.SEARCH_INPUT, query)
        
        if submit:
            self.click(self.SEARCH_BUTTON)
            self.wait_for_search_results()
    
    def wait_for_search_results(self, timeout: Optional[int] = None) -> None:
        """
        Wait for search results to appear.
        
        Args:
            timeout: Custom timeout in milliseconds
        """
        logger.debug("Waiting for search results")
        self.wait_for_selector(self.SEARCH_RESULTS, timeout=timeout)
    
    def get_search_results_count(self) -> int:
        """
        Get the number of search results.
        
        Returns:
            int: Number of search results
        """
        return self.get_elements_count(f"{self.SEARCH_RESULTS} .result-item")
    
    # ============================================================================
    # NOTIFICATION METHODS
    # ============================================================================
    
    def open_notifications(self) -> None:
        """
        Open the notifications dropdown.
        """
        logger.info("Opening notifications")
        self.click(self.NOTIFICATION_BELL)
        self.wait_for_selector(self.NOTIFICATION_DROPDOWN, state="visible")
    
    def get_notification_count(self) -> int:
        """
        Get the number of unread notifications.
        
        Returns:
            int: Number of unread notifications
        """
        if not self.is_visible(self.NOTIFICATION_BADGE):
            return 0
        
        badge_text = self.get_text(self.NOTIFICATION_BADGE)
        try:
            return int(badge_text)
        except ValueError:
            logger.warning(f"Could not parse notification count: {badge_text}")
            return 0
    
    def has_notifications(self) -> bool:
        """
        Check if there are unread notifications.
        
        Returns:
            bool: True if there are unread notifications
        """
        return self.is_visible(self.NOTIFICATION_BADGE)
    
    def get_notifications(self) -> List[str]:
        """
        Get all notification texts.
        
        Returns:
            List[str]: List of notification texts
        """
        self.open_notifications()
        
        notification_count = self.get_elements_count(self.NOTIFICATION_ITEM)
        notifications = []
        
        for i in range(notification_count):
            notification_text = self.get_text(f"{self.NOTIFICATION_ITEM}:nth-child({i+1})")
            notifications.append(notification_text)
        
        return notifications
    
    # ============================================================================
    # QUICK ACTIONS METHODS
    # ============================================================================
    
    def click_create_new(self) -> None:
        """
        Click the "Create New" button.
        """
        logger.info("Clicking create new button")
        self.click(self.CREATE_NEW_BUTTON)
    
    def click_upload(self) -> None:
        """
        Click the "Upload" button.
        """
        logger.info("Clicking upload button")
        self.click(self.UPLOAD_BUTTON)
    
    # ============================================================================
    # WIDGET METHODS
    # ============================================================================
    
    def get_widget_count(self) -> int:
        """
        Get the number of widgets on the dashboard.
        
        Returns:
            int: Number of widgets
        """
        return self.get_elements_count(self.WIDGET_CONTAINER)
    
    def is_stats_widget_visible(self) -> bool:
        """
        Check if stats widget is visible.
        
        Returns:
            bool: True if stats widget is visible
        """
        return self.is_visible(self.STATS_WIDGET)
    
    def is_recent_activity_visible(self) -> bool:
        """
        Check if recent activity widget is visible.
        
        Returns:
            bool: True if recent activity widget is visible
        """
        return self.is_visible(self.RECENT_ACTIVITY_WIDGET)
    
    def get_widget_title(self, widget_selector: str) -> str:
        """
        Get the title of a specific widget.
        
        Args:
            widget_selector: CSS selector for the widget
        
        Returns:
            str: Widget title
        """
        return self.get_text(f"{widget_selector} .widget-title")
    
    # ============================================================================
    # VALIDATION METHODS
    # ============================================================================
    
    def is_dashboard_loaded(self) -> bool:
        """
        Check if dashboard is fully loaded.
        
        Returns:
            bool: True if dashboard is loaded
        """
        return (
            self.is_visible(self.DASHBOARD_CONTAINER) and
            not self.is_visible(self.LOADING_SPINNER, timeout=1000)
        )
    
    def get_page_title_text(self) -> str:
        """
        Get the dashboard page title.
        
        Returns:
            str: Page title text
        """
        return self.get_text(self.PAGE_TITLE)
    
    def is_navigation_menu_visible(self) -> bool:
        """
        Check if navigation menu is visible.
        
        Returns:
            bool: True if navigation menu is visible
        """
        return self.is_visible(self.NAV_MENU)
    
    def is_user_dropdown_visible(self) -> bool:
        """
        Check if user dropdown toggle is visible.
        
        Returns:
            bool: True if user dropdown is visible
        """
        return self.is_visible(self.USER_DROPDOWN_TOGGLE)
    
    def verify_dashboard_elements(self) -> bool:
        """
        Verify all essential dashboard elements are present.
        
        Returns:
            bool: True if all essential elements are present
        """
        logger.info("Verifying dashboard elements")
        
        checks = {
            "Dashboard container": self.is_visible(self.DASHBOARD_CONTAINER),
            "Navigation menu": self.is_visible(self.NAV_MENU),
            "User dropdown": self.is_visible(self.USER_DROPDOWN_TOGGLE),
            "Search input": self.is_visible(self.SEARCH_INPUT),
        }
        
        for element, is_present in checks.items():
            if not is_present:
                logger.warning(f"Dashboard element missing: {element}")
                return False
        
        logger.info("All dashboard elements present")
        return True
