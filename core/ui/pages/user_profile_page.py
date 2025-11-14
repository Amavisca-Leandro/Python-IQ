"""
User Profile Page Object for profile management.

This module provides the UserProfilePage class for handling user profile
interactions including viewing and editing profile information.
"""

import logging
from typing import Optional, Dict

from playwright.sync_api import Page

from core.ui.base_page import BasePage


logger = logging.getLogger(__name__)


class UserProfilePage(BasePage):
    """
    Page Object for the User Profile page.
    
    This class encapsulates all interactions with the user profile page including:
    - Viewing profile information
    - Editing profile fields
    - Uploading profile picture
    - Changing password
    - Managing preferences
    - Saving and canceling changes
    
    Example:
        >>> profile_page = UserProfilePage(page)
        >>> profile_page.navigate_to()
        >>> profile_page.update_profile_info({
        ...     "full_name": "John Doe",
        ...     "phone": "+5511999999999"
        ... })
        >>> profile_page.save_changes()
    """
    
    # ============================================================================
    # LOCATORS
    # ============================================================================
    
    # Page identifiers
    PROFILE_CONTAINER = "#profile-container"
    PAGE_TITLE = "h1.profile-title"
    
    # Profile information display
    PROFILE_PICTURE = "#profile-picture"
    FULL_NAME_DISPLAY = "#full-name-display"
    EMAIL_DISPLAY = "#email-display"
    PHONE_DISPLAY = "#phone-display"
    BIO_DISPLAY = "#bio-display"
    
    # Edit mode fields
    EDIT_BUTTON = "#edit-profile-button"
    CANCEL_BUTTON = "#cancel-button"
    SAVE_BUTTON = "#save-button"
    
    # Input fields
    FULL_NAME_INPUT = "#full-name"
    EMAIL_INPUT = "#email"
    PHONE_INPUT = "#phone"
    BIO_TEXTAREA = "#bio"
    COMPANY_INPUT = "#company"
    LOCATION_INPUT = "#location"
    WEBSITE_INPUT = "#website"
    
    # Profile picture
    UPLOAD_PICTURE_BUTTON = "#upload-picture"
    PICTURE_INPUT = "input[type='file'][name='profile-picture']"
    REMOVE_PICTURE_BUTTON = "#remove-picture"
    
    # Password change
    CHANGE_PASSWORD_BUTTON = "#change-password-button"
    CURRENT_PASSWORD_INPUT = "#current-password"
    NEW_PASSWORD_INPUT = "#new-password"
    CONFIRM_PASSWORD_INPUT = "#confirm-password"
    UPDATE_PASSWORD_BUTTON = "#update-password-button"
    
    # Preferences
    PREFERENCES_TAB = "#preferences-tab"
    LANGUAGE_SELECT = "#language-select"
    TIMEZONE_SELECT = "#timezone-select"
    EMAIL_NOTIFICATIONS_CHECKBOX = "#email-notifications"
    SMS_NOTIFICATIONS_CHECKBOX = "#sms-notifications"
    
    # Messages
    SUCCESS_MESSAGE = ".success-message"
    ERROR_MESSAGE = ".error-message"
    VALIDATION_ERROR = ".validation-error"
    
    # Loading
    LOADING_SPINNER = ".loading-spinner"
    SAVE_SPINNER = "#save-spinner"
    
    def __init__(self, page: Page, base_url: str = ""):
        """
        Initialize UserProfilePage.
        
        Args:
            page: Playwright Page instance
            base_url: Base URL for the application
        """
        super().__init__(page, base_url)
        logger.info("UserProfilePage initialized")
    
    # ============================================================================
    # NAVIGATION METHODS
    # ============================================================================
    
    def navigate_to(self, user_id: Optional[str] = None, wait_until: str = "networkidle") -> None:
        """
        Navigate to the user profile page.
        
        Args:
            user_id: Optional user ID for viewing specific user profile
            wait_until: When to consider navigation complete
        """
        path = f"/profile/{user_id}" if user_id else "/profile"
        super().navigate_to(path, wait_until=wait_until)
        self.wait_for_page_load()
    
    def wait_for_page_load(self, timeout: Optional[int] = None) -> None:
        """
        Wait for profile page to fully load.
        
        Args:
            timeout: Custom timeout in milliseconds
        """
        logger.info("Waiting for profile page to load")
        self.wait_for_selector(self.PROFILE_CONTAINER, timeout=timeout)
        
        # Wait for loading spinner to disappear
        if self.is_visible(self.LOADING_SPINNER, timeout=1000):
            self.wait_for_selector(self.LOADING_SPINNER, state="hidden", timeout=timeout)
        
        logger.info("Profile page loaded")
    
    # ============================================================================
    # VIEW PROFILE METHODS
    # ============================================================================
    
    def get_full_name(self) -> str:
        """
        Get the displayed full name.
        
        Returns:
            str: Full name
        """
        logger.debug("Getting full name")
        return self.get_text(self.FULL_NAME_DISPLAY)
    
    def get_email(self) -> str:
        """
        Get the displayed email.
        
        Returns:
            str: Email address
        """
        logger.debug("Getting email")
        return self.get_text(self.EMAIL_DISPLAY)
    
    def get_phone(self) -> str:
        """
        Get the displayed phone number.
        
        Returns:
            str: Phone number
        """
        logger.debug("Getting phone")
        return self.get_text(self.PHONE_DISPLAY)
    
    def get_bio(self) -> str:
        """
        Get the displayed bio.
        
        Returns:
            str: Bio text
        """
        logger.debug("Getting bio")
        return self.get_text(self.BIO_DISPLAY)
    
    def get_profile_info(self) -> Dict[str, str]:
        """
        Get all profile information.
        
        Returns:
            Dict[str, str]: Dictionary with profile information
        """
        logger.info("Getting all profile information")
        
        return {
            "full_name": self.get_full_name(),
            "email": self.get_email(),
            "phone": self.get_phone(),
            "bio": self.get_bio(),
        }
    
    # ============================================================================
    # EDIT PROFILE METHODS
    # ============================================================================
    
    def click_edit_profile(self) -> None:
        """
        Click the edit profile button to enter edit mode.
        """
        logger.info("Clicking edit profile button")
        self.click(self.EDIT_BUTTON)
        self.wait_for_edit_mode()
    
    def wait_for_edit_mode(self, timeout: Optional[int] = None) -> None:
        """
        Wait for edit mode to be active.
        
        Args:
            timeout: Custom timeout in milliseconds
        """
        logger.debug("Waiting for edit mode")
        self.wait_for_selector(self.SAVE_BUTTON, timeout=timeout)
    
    def update_full_name(self, full_name: str) -> None:
        """
        Update the full name field.
        
        Args:
            full_name: New full name
        """
        logger.info(f"Updating full name to: {full_name}")
        self.fill(self.FULL_NAME_INPUT, full_name)
    
    def update_email(self, email: str) -> None:
        """
        Update the email field.
        
        Args:
            email: New email address
        """
        logger.info(f"Updating email to: {email}")
        self.fill(self.EMAIL_INPUT, email)
    
    def update_phone(self, phone: str) -> None:
        """
        Update the phone field.
        
        Args:
            phone: New phone number
        """
        logger.info(f"Updating phone to: {phone}")
        self.fill(self.PHONE_INPUT, phone)
    
    def update_bio(self, bio: str) -> None:
        """
        Update the bio field.
        
        Args:
            bio: New bio text
        """
        logger.info("Updating bio")
        self.fill(self.BIO_TEXTAREA, bio)
    
    def update_company(self, company: str) -> None:
        """
        Update the company field.
        
        Args:
            company: Company name
        """
        logger.info(f"Updating company to: {company}")
        self.fill(self.COMPANY_INPUT, company)
    
    def update_location(self, location: str) -> None:
        """
        Update the location field.
        
        Args:
            location: Location
        """
        logger.info(f"Updating location to: {location}")
        self.fill(self.LOCATION_INPUT, location)
    
    def update_website(self, website: str) -> None:
        """
        Update the website field.
        
        Args:
            website: Website URL
        """
        logger.info(f"Updating website to: {website}")
        self.fill(self.WEBSITE_INPUT, website)
    
    def update_profile_info(self, profile_data: Dict[str, str]) -> None:
        """
        Update multiple profile fields at once.
        
        Args:
            profile_data: Dictionary with field names and values
        
        Example:
            >>> profile_page.update_profile_info({
            ...     "full_name": "John Doe",
            ...     "phone": "+5511999999999",
            ...     "bio": "Software Engineer"
            ... })
        """
        logger.info("Updating profile information")
        
        # Enter edit mode if not already in it
        if not self.is_visible(self.SAVE_BUTTON, timeout=1000):
            self.click_edit_profile()
        
        # Update fields based on provided data
        field_mapping = {
            "full_name": self.update_full_name,
            "email": self.update_email,
            "phone": self.update_phone,
            "bio": self.update_bio,
            "company": self.update_company,
            "location": self.update_location,
            "website": self.update_website,
        }
        
        for field, value in profile_data.items():
            if field in field_mapping:
                field_mapping[field](value)
            else:
                logger.warning(f"Unknown field: {field}")
    
    def save_changes(self) -> None:
        """
        Save profile changes.
        """
        logger.info("Saving profile changes")
        self.click(self.SAVE_BUTTON)
        
        # Wait for save to complete
        if self.is_visible(self.SAVE_SPINNER, timeout=1000):
            self.wait_for_selector(self.SAVE_SPINNER, state="hidden")
        
        logger.info("Profile changes saved")
    
    def cancel_changes(self) -> None:
        """
        Cancel profile changes without saving.
        """
        logger.info("Canceling profile changes")
        self.click(self.CANCEL_BUTTON)
    
    # ============================================================================
    # PROFILE PICTURE METHODS
    # ============================================================================
    
    def upload_profile_picture(self, file_path: str) -> None:
        """
        Upload a profile picture.
        
        Args:
            file_path: Path to the image file
        """
        logger.info(f"Uploading profile picture: {file_path}")
        
        # Click upload button to reveal file input
        self.click(self.UPLOAD_PICTURE_BUTTON)
        
        # Set file input
        self.page.set_input_files(self.PICTURE_INPUT, file_path)
        
        logger.info("Profile picture uploaded")
    
    def remove_profile_picture(self) -> None:
        """
        Remove the current profile picture.
        """
        logger.info("Removing profile picture")
        self.click(self.REMOVE_PICTURE_BUTTON)
    
    def has_profile_picture(self) -> bool:
        """
        Check if user has a profile picture.
        
        Returns:
            bool: True if profile picture exists
        """
        return self.is_visible(self.PROFILE_PICTURE)
    
    # ============================================================================
    # PASSWORD CHANGE METHODS
    # ============================================================================
    
    def click_change_password(self) -> None:
        """
        Click the change password button.
        """
        logger.info("Clicking change password button")
        self.click(self.CHANGE_PASSWORD_BUTTON)
    
    def change_password(
        self,
        current_password: str,
        new_password: str,
        confirm_password: Optional[str] = None
    ) -> None:
        """
        Change user password.
        
        Args:
            current_password: Current password
            new_password: New password
            confirm_password: Confirm new password (defaults to new_password)
        """
        logger.info("Changing password")
        
        confirm_password = confirm_password or new_password
        
        self.fill(self.CURRENT_PASSWORD_INPUT, current_password)
        self.fill(self.NEW_PASSWORD_INPUT, new_password)
        self.fill(self.CONFIRM_PASSWORD_INPUT, confirm_password)
        
        self.click(self.UPDATE_PASSWORD_BUTTON)
        
        logger.info("Password change submitted")
    
    # ============================================================================
    # PREFERENCES METHODS
    # ============================================================================
    
    def navigate_to_preferences(self) -> None:
        """
        Navigate to preferences tab.
        """
        logger.info("Navigating to preferences tab")
        self.click(self.PREFERENCES_TAB)
    
    def select_language(self, language: str) -> None:
        """
        Select a language preference.
        
        Args:
            language: Language code or label
        """
        logger.info(f"Selecting language: {language}")
        self.select_option(self.LANGUAGE_SELECT, label=language)
    
    def select_timezone(self, timezone: str) -> None:
        """
        Select a timezone preference.
        
        Args:
            timezone: Timezone value or label
        """
        logger.info(f"Selecting timezone: {timezone}")
        self.select_option(self.TIMEZONE_SELECT, label=timezone)
    
    def enable_email_notifications(self) -> None:
        """
        Enable email notifications.
        """
        logger.info("Enabling email notifications")
        self.check(self.EMAIL_NOTIFICATIONS_CHECKBOX)
    
    def disable_email_notifications(self) -> None:
        """
        Disable email notifications.
        """
        logger.info("Disabling email notifications")
        self.uncheck(self.EMAIL_NOTIFICATIONS_CHECKBOX)
    
    def enable_sms_notifications(self) -> None:
        """
        Enable SMS notifications.
        """
        logger.info("Enabling SMS notifications")
        self.check(self.SMS_NOTIFICATIONS_CHECKBOX)
    
    def disable_sms_notifications(self) -> None:
        """
        Disable SMS notifications.
        """
        logger.info("Disabling SMS notifications")
        self.uncheck(self.SMS_NOTIFICATIONS_CHECKBOX)
    
    # ============================================================================
    # VALIDATION METHODS
    # ============================================================================
    
    def get_success_message(self) -> str:
        """
        Get success message text.
        
        Returns:
            str: Success message
        """
        logger.debug("Getting success message")
        return self.get_text(self.SUCCESS_MESSAGE)
    
    def get_error_message(self) -> str:
        """
        Get error message text.
        
        Returns:
            str: Error message
        """
        logger.debug("Getting error message")
        return self.get_text(self.ERROR_MESSAGE)
    
    def get_validation_error(self) -> str:
        """
        Get validation error text.
        
        Returns:
            str: Validation error
        """
        logger.debug("Getting validation error")
        return self.get_text(self.VALIDATION_ERROR)
    
    def has_success_message(self) -> bool:
        """
        Check if success message is displayed.
        
        Returns:
            bool: True if success message is visible
        """
        return self.is_visible(self.SUCCESS_MESSAGE)
    
    def has_error_message(self) -> bool:
        """
        Check if error message is displayed.
        
        Returns:
            bool: True if error message is visible
        """
        return self.is_visible(self.ERROR_MESSAGE)
    
    def is_in_edit_mode(self) -> bool:
        """
        Check if profile is in edit mode.
        
        Returns:
            bool: True if in edit mode
        """
        return self.is_visible(self.SAVE_BUTTON, timeout=1000)
    
    def get_page_title_text(self) -> str:
        """
        Get the page title text.
        
        Returns:
            str: Page title
        """
        return self.get_text(self.PAGE_TITLE)
