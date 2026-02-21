from datetime import datetime

class AnalyticsManager:
    def __init__(self, db_reference, analytics_db_reference):
        self.db = db_reference
        self.analytics = analytics_db_reference

    def log_access(self, short_code):
        """Tracks the access details."""
        if short_code not in self.analytics:
            self.analytics[short_code] = []
            
        access_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        self.analytics[short_code].append(access_data)
        # Safely increment click count in main DB
        if short_code in self.db:
            self.db[short_code]["click_count"] += 1

    def get_summary(self, short_code, expiration_manager):
        """Retrieves summary, checking expiration via the passed manager."""
        record = self.db.get(short_code)
        if not record:
            return {"error": "Short link not found."}
        
        # Use the expiration manager to check validity before showing stats
        if expiration_manager.check_expiration(record):
            return {"error": "This link has expired."}

        click_data = self.analytics.get(short_code, [])
        
        summary = {
            "total_clicks": len(click_data),
            "last_5_clicks": click_data[-5:]
        }
        
        return {
            "url_info": record,
            "analytics_summary": summary
        }