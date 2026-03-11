import requests
import logging
from datetime import datetime

logger = logging.getLogger('TokyoTrainAlert')

class TrainStatusChecker:
    # ODPT endpoint for train information (Yamanote Line)
    # We'll use the "odpt:TrainInformation" vocabulary.
    # More details: https://developer.odpt.org/en/docs/api/train_info
    API_URL = "https://api.odpt.org/api/v4/odpt:TrainInformation"
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.line = "odpt:Railway:JR-East.Yamanote"  # ODPT railway ID for Yamanote Line

    def check_delay(self):
        """Return (is_delayed: bool, message: str)"""
        try:
            params = {
                "odpt:railway": self.line,
                "acl:consumerKey": self.api_key
            }
            response = requests.get(self.API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data:
                logger.info("No train information available – assuming no delay.")
                return False, "No delay reported"

            # The API returns an array of information items for the line.
            # We look for the "odpt:trainInformationStatus" field.
            # Usually if there is a delay, it will contain a description.
            for item in data:
                # Check if this item is for our line
                if item.get("odpt:railway") == self.line:
                    status = item.get("odpt:trainInformationStatus", {})
                    # The status might be a multilingual object. We'll extract English or Japanese.
                    # For simplicity, we'll take the first available text.
                    if isinstance(status, dict):
                        # ODPT often returns { "ja": "...", "en": "..." }
                        message = status.get("en") or status.get("ja") or "No details"
                    else:
                        message = str(status)

                    # Determine if this indicates a delay.
                    # Keywords: "delay", "遅れ", "乱れ", "見合わせ" etc.
                    delay_keywords = ["delay", "遅れ", "乱れ", "見合わせ", "停止", "運転見合わせ"]
                    is_delayed = any(keyword in message.lower() for keyword in delay_keywords) if message else False

                    if is_delayed:
                        logger.info(f"Delay detected: {message}")
                        return True, message
                    else:
                        logger.info("No delay detected.")
                        return False, message

            # If no item matched the line (shouldn't happen), assume no delay
            logger.warning("No data for Yamanote Line in response.")
            return False, "No specific info for Yamanote"

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            # In case of error, we assume no delay to avoid false alerts,
            # but we log the error.
            return False, f"API error: {e}"
        except Exception as e:
            logger.exception(f"Unexpected error checking train status: {e}")
            return False, f"Unexpected error: {e}"