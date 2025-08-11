#!/usr/bin/env python3
"""
Flask Web Interface for pw_tester

A production-ready web interface for password complexity analysis.
"""

from flask import Flask, render_template, request, jsonify
import json
from pw_tester import PasswordTester
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key-change-in-production")

# Initialize the password tester
tester = PasswordTester()


@app.route("/")
def index():
    """Main page with password analysis form"""
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze_password():
    """API endpoint for password analysis"""
    try:
        data = request.get_json()

        if not data or "password" not in data:
            return jsonify({"error": "Password is required"}), 400

        password = data["password"]

        if not password:
            return jsonify({"error": "Password cannot be empty"}), 400

        # Analyze the password
        analysis = tester.analyze_password(password)

        # Convert to JSON-serializable format
        result = {
            "password_length": analysis.password_length,
            "character_space": analysis.character_space,
            "entropy_bits": round(analysis.entropy_bits, 2),
            "total_combinations": analysis.total_combinations,
            "complexity_score": analysis.complexity_score,
            "brute_force_times": analysis.brute_force_times,
            "recommendations": analysis.recommendations,
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/demo")
def demo_passwords():
    """API endpoint for demo password examples"""
    demo_passwords = [
        ("123456", "Very weak password"),
        ("password", "Common word"),
        ("Password123", "Basic complexity"),
        ("MyS3cur3P@ssw0rd!", "Strong password"),
        ("correct horse battery staple", "Passphrase"),
    ]

    results = []
    for pwd, description in demo_passwords:
        analysis = tester.analyze_password(pwd)
        result = {
            "password": pwd,
            "description": description,
            "password_length": analysis.password_length,
            "character_space": analysis.character_space,
            "entropy_bits": round(analysis.entropy_bits, 2),
            "total_combinations": analysis.total_combinations,
            "complexity_score": analysis.complexity_score,
            "brute_force_times": analysis.brute_force_times,
            "recommendations": analysis.recommendations,
        }
        results.append(result)

    return jsonify(results)


@app.route("/demo")
def demo_page():
    """Demo page showing example password analyses"""
    return render_template("demo.html")


@app.route("/api/health")
def health_check():
    """Health check endpoint for production monitoring"""
    return jsonify({"status": "healthy", "service": "pw_tester_web"})


@app.errorhandler(404)
def not_found(error):
    """Custom 404 page"""
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    """Custom 500 page"""
    return render_template("500.html"), 500


def main():
    """Main function to run the web application"""
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"

    if debug:
        app.run(host="0.0.0.0", port=port, debug=True)
    else:
        # Production mode - use gunicorn
        print(f"Starting production server on port {port}")
        print("Use: gunicorn -w 4 -b 0.0.0.0:{} web_app:app".format(port))
        app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
