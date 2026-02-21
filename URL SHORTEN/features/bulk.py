class BulkManager:
    def __init__(self):
        pass

    def process_csv(self, csv_data, custom_domain, shorten_function):
        """
        Processes CSV data.
        IMPORTANT: It needs the 'shorten_function' passed to it so it can 
        call the main service to create links.
        """
        results = []
        lines = csv_data.strip().split('\n')
        
        # Skip header if it exists
        if lines and lines[0].lower().startswith("url"):
            lines = lines[1:]

        for i, line in enumerate(lines):
            try:
                parts = [p.strip() for p in line.split(',')]
                original_url = parts[0]
                
                # Parse columns safely
                days_valid = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
                hours_valid = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else None
                seconds_valid = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else None
                custom_code = parts[4] if len(parts) > 4 and parts[4] else None
                domain = parts[5] if len(parts) > 5 and parts[5] else custom_domain

                # Call the main service function
                result = shorten_function(
                    original_url, days_valid, hours_valid, seconds_valid, custom_code, domain
                )
                
                # Check if the result has an error (like code taken)
                if "error" in result:
                     raise Exception(result["error"])

                result_entry = {
                    "url": original_url,
                    "status": "Success",
                    "short_link": result['shortLink']
                }
            except Exception as e:
                result_entry = {
                    "url": parts[0] if 'parts' in locals() and parts else f"Line {i+1}",
                    "status": "Failure",
                    "error": str(e)
                }
            
            results.append(result_entry)
        
        return results