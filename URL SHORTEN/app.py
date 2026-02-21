# app.py
from flask import Flask, request, jsonify, render_template, redirect
from service import URLShortenerService

# --- FLASK APPLICATION SETUP ---

app = Flask(__name__)
shortener = URLShortenerService()

# --- API ROUTES ---

@app.route('/api/shorten', methods=['POST'])
def shorten_link():
    data = request.get_json()
    original_url = data.get('original_url')
    days_valid = data.get('days_valid')
    hours_valid = data.get('hours_valid')
    seconds_valid = data.get('seconds_valid')
    custom_code = data.get('custom_code')
    custom_domain = data.get('custom_domain')
    
    if not original_url:
        return jsonify({"error": "Original URL is required"}), 400

    result = shortener.shorten_url(original_url, days_valid, hours_valid, seconds_valid, custom_code, custom_domain)
    
    if "error" in result:
        return jsonify(result), 409
    
    return jsonify(result)

@app.route('/api/analytics/<short_code>', methods=['GET'])
def get_link_analytics(short_code):
    analytics = shortener.get_analytics(short_code)
    if "error" in analytics:
        return jsonify(analytics), 404
    
    return jsonify(analytics)

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    deleted_count = shortener.auto_delete_expired()
    warnings = shortener.get_dashboard_warnings()
    
    link_list = [{
        "short_code": code,
        "short_link": record['short_link'],
        "clicks": record['click_count'],
        "expires_at": record['expires_at']
    } for code, record in shortener.db.items()]
    
    return jsonify({
        "warnings": warnings,
        "link_list": link_list,
        "deleted_expired": deleted_count
    })

@app.route('/api/bulk-shorten', methods=['POST'])
def bulk_shorten_api():
    data = request.get_json()
    csv_data = data.get('csv_data')
    custom_domain = data.get('custom_domain')
    
    if not csv_data:
        return jsonify({"error": "CSV data is required"}), 400

    results = shortener.bulk_shorten_csv(csv_data, custom_domain)
    return jsonify({"results": results})

@app.route('/<short_code>')
def redirect_to_original(short_code):
    user_agent = request.headers.get('User-Agent', 'Unknown')
    ip_address = request.remote_addr if request.remote_addr else '0.0.0.0'
    
    target_url = shortener.redirect_url(short_code, user_agent, ip_address)
    
    if target_url.startswith("Error:"):
        return f"<h1>404 Not Found</h1><p>{target_url}</p>", 404
    
    return redirect(target_url, code=302)

# --- MAIN ROUTE TO SERVE THE UI ---

@app.route('/')
def serve_ui():
    if len(shortener.db) == 0:
        shortener.shorten_url(
            "https://www.google.com/search?q=simple+flask+app",
            days_valid=365, hours_valid=0, seconds_valid=0,
            custom_code="flask-start", custom_domain=None
        )

        shortener.shorten_url(
            "https://example.com/expiring-soon-link",
            days_valid=0, hours_valid=1, seconds_valid=30,
            custom_code="expiring", custom_domain=None
        )

        shortener.shorten_url(
            "https://branded-link.com",
            days_valid=0, hours_valid=0, seconds_valid=0,
            custom_code="branded", custom_domain="https://my.link.co"
        )

        # Removed _log_access calls (method does not exist)

    return render_template('index.html', shortener=shortener)

# --- RUN THE APP ---

if __name__ == '__main__':
    print("---------------------------------------------------------------------")
    print("Flask App is running. Open http://127.0.0.1:5000/ in your browser.")
    print("Press Ctrl+C to stop.")
    print("---------------------------------------------------------------------")
    app.run(debug=True)