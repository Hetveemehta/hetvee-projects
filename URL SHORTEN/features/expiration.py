from datetime import datetime, timedelta

class ExpirationManager:
    def __init__(self, db_reference):
        # We hold a reference to the main database
        self.db = db_reference

    def check_expiration(self, record: dict):
        """Checks if a record has expired."""
        if record["is_permanent"] or record.get("is_expired"):
            return record.get("is_expired", False)

        expires_at_str = record["expires_at"]
        if expires_at_str:
            expires_at = datetime.strptime(expires_at_str, "%Y-%m-%d %H:%M:%S")
            is_expired = datetime.now() > expires_at
            if is_expired:
                record["is_expired"] = True
            return is_expired
        return False

    def auto_delete_expired(self, analytics_db):
        """Deletes expired records from memory."""
        expired_codes = []
        # Identify expired
        for code, record in list(self.db.items()): 
            if self.check_expiration(record):
                expired_codes.append(code)
        
        # Delete them
        for code in expired_codes:
            del self.db[code]
            if code in analytics_db:
                del analytics_db[code]
        return len(expired_codes)

    def get_dashboard_warnings(self):
        """Provides a dashboard view of links that are expiring soon (within 7 days)."""
        warnings = []
        now = datetime.now()
        seven_days_later = now + timedelta(days=7)
        
        for code, record in self.db.items():
            if not record["is_permanent"] and not self.check_expiration(record):
                try:
                    expires_at = datetime.strptime(record["expires_at"], "%Y-%m-%d %H:%M:%S")
                    
                    if now < expires_at < seven_days_later:
                        time_left = expires_at - now
                        warnings.append({
                            "short_link": record["short_link"],
                            "original_url": record["original_url"],
                            "expires_in_seconds": int(time_left.total_seconds()),
                            "expires_in_days": time_left.days,
                            "expires_at": record["expires_at"]
                        })
                except Exception:
                    continue
        return warnings