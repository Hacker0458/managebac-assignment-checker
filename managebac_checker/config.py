"""
Configuration management for ManageBac Assignment Checker.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv


class Config:
    """Configuration class for ManageBac Assignment Checker."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        # Load environment variables
        load_dotenv()
        
        # Required credentials
        self.email = os.getenv('MANAGEBAC_EMAIL')
        self.password = os.getenv('MANAGEBAC_PASSWORD')
        self.url = os.getenv('MANAGEBAC_URL', 'https://shtcs.managebac.cn')
        
        # Browser settings
        self.headless = os.getenv('HEADLESS', 'true').lower() == 'true'
        self.timeout = int(os.getenv('TIMEOUT', '30000'))
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'
        
        # Report and notification settings
        self.report_format = os.getenv('REPORT_FORMAT', 'console,json').split(',')
        self.output_dir = Path(os.getenv('OUTPUT_DIR', './reports'))
        self.enable_notifications = os.getenv('ENABLE_NOTIFICATIONS', 'false').lower() == 'true'
        
        # Email notification settings
        self.smtp_server = os.getenv('SMTP_SERVER', '')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_user = os.getenv('EMAIL_USER', '')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        self.notification_email = os.getenv('NOTIFICATION_EMAIL', '')
        
        # Analysis settings
        self.days_ahead = int(os.getenv('DAYS_AHEAD', '7'))
        self.priority_keywords = os.getenv('PRIORITY_KEYWORDS', 'exam,test,project,essay').split(',')
        
        # Detail fetching settings
        self.fetch_details = os.getenv('FETCH_DETAILS', 'false').lower() == 'true'
        self.details_limit = int(os.getenv('DETAILS_LIMIT', '10'))
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Validate required settings
        self._validate()
    
    def _validate(self) -> None:
        """Validate required configuration."""
        if not self.email or not self.password:
            print("Error: MANAGEBAC_EMAIL and MANAGEBAC_PASSWORD must be set in .env file")
            print("Please copy .env.example to .env and fill in your credentials")
            sys.exit(1)
    
    def get_report_formats(self) -> List[str]:
        """Get list of report formats to generate."""
        return [fmt.strip().lower() for fmt in self.report_format if fmt.strip()]
    
    def is_notification_enabled(self) -> bool:
        """Check if email notifications are properly configured."""
        return (self.enable_notifications and 
                self.smtp_server and 
                self.email_user and 
                self.email_password and 
                self.notification_email)
    
    def __repr__(self) -> str:
        """String representation of config (without sensitive data)."""
        return (f"Config(email={self.email}, url={self.url}, "
                f"headless={self.headless}, debug={self.debug})")