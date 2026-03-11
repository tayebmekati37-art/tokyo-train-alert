import time
import schedule
from config import Config
from logger import setup_logger
from train_status import TrainStatusChecker
from email_alert import EmailAlert
from database import AlertDatabase

def main():
    # Setup logging
    logger = setup_logger()
    logger.info("Tokyo Train Alert started.")

    # Validate config
    try:
        Config.validate()
    except EnvironmentError as e:
        logger.critical(f"Configuration error: {e}")
        return

    # Initialize components
    checker = TrainStatusChecker(Config.ODPT_API_KEY)
    email_alert = EmailAlert(
        smtp_server=Config.SMTP_SERVER,
        port=Config.SMTP_PORT,
        sender=Config.EMAIL_SENDER,
        password=Config.EMAIL_PASSWORD,
        recipient=Config.EMAIL_RECIPIENT
    )
    db = AlertDatabase() if Config.USE_SQLITE else None

    # To avoid duplicate alerts, we remember the last known delay state.
    last_alert_time = None  # or we can store last status
    # For simplicity, we'll send an alert every time a delay is detected,
    # but you could enhance to only send when state changes or after a cooldown.

    def job():
        nonlocal last_alert_time
        logger.info("Checking train status...")
        is_delayed, message = checker.check_delay()

        if is_delayed:
            # Construct email subject and body
            subject = "⚠️ Yamanote Line Delay Alert"
            body = f"Delay detected on Yamanote Line at {time.ctime()}\n\nDetails: {message}"
            # Send email
            sent = email_alert.send(subject, body)
            if sent:
                logger.info("Alert email sent.")
                if db:
                    db.log_alert("Yamanote Line", "DELAY", message, email_sent=True)
            else:
                logger.error("Failed to send alert email.")
                if db:
                    db.log_alert("Yamanote Line", "DELAY", message, email_sent=False)
        else:
            logger.info("No delay detected.")
            if db:
                db.log_alert("Yamanote Line", "NORMAL", message, email_sent=False)

    # Schedule the job every CHECK_INTERVAL minutes
    schedule.every(Config.CHECK_INTERVAL).minutes.do(job)

    # Run immediately once at start
    job()

    # Keep running
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down by user request.")
    except Exception as e:
        logger.exception("Unexpected error in main loop.")

if __name__ == "__main__":
    main()