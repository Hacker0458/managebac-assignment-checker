#!/usr/bin/env python3
"""
ManageBac Assignment Checker

Automated tool to log into ManageBac and check for unsubmitted assignments.
"""

import os
import sys
import asyncio
from datetime import datetime
from typing import List, Dict, Any

from playwright.async_api import async_playwright, Page, Browser
from dotenv import load_dotenv


class ManageBacChecker:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        self.email = os.getenv('MANAGEBAC_EMAIL')
        self.password = os.getenv('MANAGEBAC_PASSWORD')
        self.url = os.getenv('MANAGEBAC_URL', 'https://shtcs.managebac.cn')
        self.headless = os.getenv('HEADLESS', 'true').lower() == 'true'
        self.timeout = int(os.getenv('TIMEOUT', '30000'))
        
        # Validate required environment variables
        if not self.email or not self.password:
            print("Error: MANAGEBAC_EMAIL and MANAGEBAC_PASSWORD must be set in .env file")
            sys.exit(1)
    
    async def login(self, page: Page) -> bool:
        """
        Log into ManageBac with provided credentials.
        
        Args:
            page: The Playwright page instance
            
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            print(f"Navigating to {self.url}...")
            await page.goto(self.url, wait_until="domcontentloaded")
            
            # Wait for login form to load
            print("Waiting for login form...")
            await page.wait_for_selector('input[type="email"], input[name="email"]', timeout=self.timeout)
            
            # Fill in email
            email_selector = 'input[type="email"], input[name="email"]'
            await page.fill(email_selector, self.email)
            print(f"Filled email: {self.email}")
            
            # Fill in password
            password_selector = 'input[type="password"], input[name="password"]'
            await page.fill(password_selector, self.password)
            print("Filled password")
            
            # Click login button
            login_button_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Login")',
                'button:has-text("Sign in")',
                '.btn-primary'
            ]
            
            login_clicked = False
            for selector in login_button_selectors:
                try:
                    await page.click(selector, timeout=2000)
                    print(f"Clicked login button with selector: {selector}")
                    login_clicked = True
                    break
                except:
                    continue
            
            if not login_clicked:
                print("Warning: Could not find login button, trying form submission...")
                await page.press(password_selector, 'Enter')
            
            # Wait for navigation or error message
            print("Waiting for login to complete...")
            
            try:
                # Wait for either successful navigation or error message
                await page.wait_for_load_state("domcontentloaded", timeout=self.timeout)
                
                # Check if we're still on login page (login failed)
                current_url = page.url
                if 'login' in current_url.lower() or 'signin' in current_url.lower():
                    # Look for error messages
                    error_elements = await page.query_selector_all('.error, .alert-danger, [class*="error"]')
                    if error_elements:
                        error_text = await error_elements[0].text_content()
                        print(f"Login failed: {error_text}")
                        return False
                    else:
                        print("Login may have failed (still on login page)")
                        return False
                
                print(f"Login successful! Current URL: {current_url}")
                return True
                
            except Exception as e:
                print(f"Error during login: {e}")
                return False
                
        except Exception as e:
            print(f"Error during login process: {e}")
            return False
    
    async def get_unsubmitted_assignments(self, page: Page) -> List[Dict[str, Any]]:
        """
        Extract unsubmitted assignments from ManageBac.
        
        Args:
            page: The Playwright page instance
            
        Returns:
            List of dictionaries containing assignment information
        """
        assignments = []
        
        try:
            print("Looking for assignments...")
            
            # Common selectors for ManageBac assignments
            assignment_selectors = [
                '.assignment',
                '[data-assignment]',
                '.task-item',
                '.homework-item',
                '.assignment-item'
            ]
            
            # Try to find assignments container
            for selector in assignment_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        print(f"Found {len(elements)} elements with selector: {selector}")
                        
                        for element in elements:
                            try:
                                # Extract assignment details
                                title_element = await element.query_selector('.title, .assignment-title, h3, h4')
                                due_date_element = await element.query_selector('.due-date, .date, [class*="date"]')
                                status_element = await element.query_selector('.status, .assignment-status')
                                
                                title = await title_element.text_content() if title_element else "Unknown Assignment"
                                due_date = await due_date_element.text_content() if due_date_element else "No due date"
                                status = await status_element.text_content() if status_element else "Unknown status"
                                
                                # Check if assignment is unsubmitted
                                if any(keyword in status.lower() for keyword in ['not submitted', 'unsubmitted', 'pending', 'overdue']):
                                    assignments.append({
                                        'title': title.strip(),
                                        'due_date': due_date.strip(),
                                        'status': status.strip(),
                                        'found_at': datetime.now().isoformat()
                                    })
                                    
                            except Exception as e:
                                print(f"Error extracting assignment details: {e}")
                                continue
                        
                        break  # Found assignments, stop looking
                        
                except:
                    continue
            
            # If no specific assignment elements found, try to find any relevant text
            if not assignments:
                print("No specific assignment elements found, searching page content...")
                
                # Look for common assignment-related text patterns
                page_content = await page.content()
                if any(keyword in page_content.lower() for keyword in ['assignment', 'homework', 'task', 'due', 'submit']):
                    print("Found assignment-related content on page")
                    
                    # Try to extract any visible text that might be assignments
                    text_elements = await page.query_selector_all('*:visible')
                    for element in text_elements[:50]:  # Limit to first 50 elements
                        try:
                            text = await element.text_content()
                            if text and any(keyword in text.lower() for keyword in ['assignment', 'homework', 'due', 'submit']):
                                if len(text.strip()) > 10 and len(text.strip()) < 200:  # Reasonable length
                                    assignments.append({
                                        'title': text.strip(),
                                        'due_date': 'Unknown',
                                        'status': 'Found on page',
                                        'found_at': datetime.now().isoformat()
                                    })
                        except:
                            continue
            
            return assignments
            
        except Exception as e:
            print(f"Error getting assignments: {e}")
            return assignments
    
    async def run(self):
        """
        Main method to run the ManageBac checker.
        """
        print("=== ManageBac Assignment Checker ===")
        print(f"Target URL: {self.url}")
        print(f"Email: {self.email}")
        print(f"Headless mode: {self.headless}")
        print()
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            
            try:
                # Create new page
                page = await browser.new_page()
                
                # Set viewport size
                await page.set_viewport_size({'width': 1280, 'height': 720})
                
                # Attempt login
                if not await self.login(page):
                    print("Login failed. Please check your credentials.")
                    return
                
                # Wait a moment for page to fully load
                await page.wait_for_timeout(3000)
                
                # Get unsubmitted assignments
                assignments = await self.get_unsubmitted_assignments(page)
                
                # Display results
                print("\n=== Results ===")
                if assignments:
                    print(f"Found {len(assignments)} potential unsubmitted assignments:")
                    print()
                    
                    for i, assignment in enumerate(assignments, 1):
                        print(f"{i}. {assignment['title']}")
                        print(f"   Due Date: {assignment['due_date']}")
                        print(f"   Status: {assignment['status']}")
                        print()
                else:
                    print("No unsubmitted assignments found!")
                    print("This could mean:")
                    print("- All assignments are submitted ✓")
                    print("- The page structure has changed and needs script updates")
                    print("- You need to navigate to the assignments page manually")
                
                print(f"Check completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
            finally:
                await browser.close()


async def main():
    """Main entry point."""
    checker = ManageBacChecker()
    await checker.run()


if __name__ == '__main__':
    asyncio.run(main())