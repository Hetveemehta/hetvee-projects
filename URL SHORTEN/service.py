from datetime import datetime, timedelta
from utils import generate_unique_code
from features.expiration import ExpirationManager
from features.analytics import AnalyticsManager
from features.bulk import BulkManager

class URLShortenerService:
    """
    The 'CEO' Class. 
    It holds the data (state) and delegates tasks to the feature managers.
    """
    def __init__(self, code_length=7):
        # The Shared State
        self.db = {}         
        self.analytics_db = {}  
        
        self.code_length = code_length
        self.default_base_url = "http://127.0.0.1:5000/"
        
        # Initialize Feature Managers with access to the DB
        self.expiration_manager = ExpirationManager(self.db)
        self.analytics_manager = AnalyticsManager(self.db, self.analytics_db)
        self.bulk_manager = BulkManager()

    # --- CORE LOGIC ---

    def shorten_url(self, original_url: str, days_valid: int = None, hours_valid: int = None, seconds_valid: int = None, custom_code: str = None, custom_domain: str = None) -> dict:
        if custom_code and custom_code in self.db:
            return {"error": f"Custom code '{custom_code}' is already taken."}
        
        if custom_code:
            short_code = custom_code
        else:
            # Use the Utils helper
            short_code, new_length = generate_unique_code(self.db, self.code_length)
            self.code_length = new_length # Update length if it changed

        # Expiration Math
        total_seconds = 0
        if days_valid: total_seconds += days_valid * 86400
        if hours_valid: total_seconds += hours_valid * 3600
        if seconds_valid: total_seconds += seconds_valid

        expires_at = None
        is_permanent = True
        
        if total_seconds > 0:
            expires_at = (datetime.now() + timedelta(seconds=total_seconds)).strftime("%Y-%m-%d %H:%M:%S")
            is_permanent = False
        
        base = custom_domain if custom_domain else self.default_base_url
        if not base.endswith('/'): base += '/'

        record = {
            "original_url": original_url,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "expires_at": expires_at,
            "is_permanent": is_permanent,
            "click_count": 0,
            "custom_domain": custom_domain,
            "short_link": f"{base}{short_code}"
        }
        
        self.db[short_code] = record
        # Initialize empty analytics list for this code
        self.analytics_db[short_code] = []
        
        return {"shortCode": short_code, "shortLink": record["short_link"]}

    def redirect_url(self, short_code: str, user_agent: str = "Unknown", ip_address: str = "0.0.0.0") -> str:
        record = self.db.get(short_code)
        
        if not record:
            return "Error: Short link not found."

        # Delegate to Expiration Manager
        if self.expiration_manager.check_expiration(record):
            return "Error: This link has expired."

        # Delegate to Analytics Manager
        self.analytics_manager.log_access(short_code)
        
        return record["original_url"]

    # --- DELEGATED FEATURES ---

    def get_analytics(self, short_code: str) -> dict:
        # Pass expiration manager so analytics knows if link is dead
        return self.analytics_manager.get_summary(short_code, self.expiration_manager)

    def auto_delete_expired(self):
        return self.expiration_manager.auto_delete_expired(self.analytics_db)

    def get_dashboard_warnings(self):
        return self.expiration_manager.get_dashboard_warnings()

    def bulk_shorten_csv(self, csv_data: str, custom_domain: str = None) -> list:
        # We pass 'self.shorten_url' as a callback function!
        return self.bulk_manager.process_csv(csv_data, custom_domain, self.shorten_url)