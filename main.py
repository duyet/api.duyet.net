from flask import Flask, Response, render_template, request, jsonify, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time
import os
import logging
import requests
from flask_compress import Compress

from api.gender import name_to_gender
from api.similar_skill import similar_skill
from api.clean_skill import clean_skill as clean_skill_func
from api.clean_datetime import clean_datetime
from api.profile_faker import profile_faker

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config["DEBUG"] = os.environ.get("FLASK_DEBUG", "False").lower() == "true"

# Enable compression
Compress(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
)


# Security headers
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self' 'unsafe-inline' 'unsafe-eval' https:; img-src 'self' data: https:;"
    )

    # Add CORS headers
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"

    return response


@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded errors."""
    return make_response(
        jsonify(
            error="Rate limit exceeded",
            message=str(e.description),
            suggestion="Please wait before making more requests",
        ),
        429,
    )


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "templates"))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route("/")
@limiter.exempt
def index():
    content = get_file("index.html")
    return Response(content, mimetype="text/html")


@app.route("/ping")
@limiter.exempt
def ping():
    """Simple ping endpoint for uptime monitoring."""
    return "PONG"


@app.route("/health")
@limiter.exempt
def healthcheck():
    """Healthcheck endpoint for load balancers."""
    return jsonify({"status": "healthy", "service": "api.duyet.net", "version": "2.0.0"})


@app.route("/api/v1/gender")
@limiter.limit("5000 per day")
@limiter.limit("500 per hour")
def gender_api():
    """Predict gender from first name.

    Query params:
            name or first_name: The first name to analyze

    Returns:
            JSON with name, gender (male/female), and processing time
    """
    s_time = time.time()
    name = request.args.get("name") or request.args.get("first_name", "")

    if not name or not name.strip():
        return (
            jsonify(
                error="Missing parameter",
                message="Please provide 'name' or 'first_name' parameter",
                example="/api/v1/gender?name=John",
            ),
            400,
        )

    try:
        gender = name_to_gender(name.strip())
        e_time = time.time() - s_time
        return jsonify(name=name, gender=gender, time=e_time)
    except Exception as e:
        logger.error(f"Gender API error: {str(e)}")
        return jsonify(error="Internal error", message="Failed to process request"), 500


@app.route("/gender")
@limiter.exempt
def gender_view():
    return render_template("gender.html")


@app.route("/api/v1/similar_skill")
@limiter.limit("5000 per day")
@limiter.limit("500 per hour")
def similar_skill_api():
    """Find similar skills (stub - not yet implemented).

    Query params:
            skill or skills: The skill name

    Returns:
            JSON with similar skills and processing time
    """
    s_time = time.time()
    skill = request.args.get("skill") or request.args.get("skills", "")

    if not skill:
        return jsonify(error="Missing parameter", message="Please provide 'skill' parameter"), 400

    try:
        result = similar_skill(skill)
        logger.info(f"Similar skill query: {skill}")
        e_time = time.time() - s_time
        return jsonify(input_skill=skill, similar_skills=result, time=e_time)
    except Exception as e:
        logger.error(f"Similar skill API error: {str(e)}")
        return jsonify(error="Internal error"), 500


@app.route("/similar_skill")
@limiter.exempt
def similar_skill_view():
    return render_template("similar_skill.html")


@app.route("/api/v1/clean_skill")
@limiter.limit("5000 per day")
@limiter.limit("500 per hour")
def clean_skill_api():
    """Clean and normalize skill/technology names.

    Query params:
            skill or skills: The raw skill name to clean

    Returns:
            JSON with raw input, cleaned output, and processing time
    """
    s_time = time.time()
    skill = request.args.get("skill") or request.args.get("skills", "")

    if not skill:
        return (
            jsonify(
                error="Missing parameter",
                message="Please provide 'skill' parameter",
                example="/api/v1/clean_skill?skill=JavaScript",
            ),
            400,
        )

    try:
        result = clean_skill_func(skill)
        logger.info(f"Clean skill: {skill} -> {result}")
        e_time = time.time() - s_time
        return jsonify(raw=skill, cleaned=result, time=e_time)
    except Exception as e:
        logger.error(f"Clean skill API error: {str(e)}")
        return jsonify(error="Internal error"), 500


@app.route("/api/v1/clean_datetime")
@limiter.limit("5000 per day")
@limiter.limit("500 per hour")
def clean_datetime_api():
    """Parse and normalize datetime strings.

    Query params:
            datetime or d: The raw datetime string to parse

    Returns:
            JSON with raw input, ISO format output, and processing time
    """
    s_time = time.time()
    datetime_str = request.args.get("datetime") or request.args.get("d", "")

    if not datetime_str:
        return (
            jsonify(
                error="Missing parameter",
                message="Please provide 'datetime' or 'd' parameter",
                example="/api/v1/clean_datetime?datetime=Jan 2020",
            ),
            400,
        )

    try:
        result = clean_datetime(datetime_str)
        if result:
            result = result.isoformat()
        else:
            result = ""
        e_time = time.time() - s_time
        return jsonify(raw=datetime_str, cleaned=result, time=e_time)
    except Exception as e:
        logger.error(f"Clean datetime API error: {str(e)}")
        return jsonify(error="Internal error"), 500


@app.route("/api/v1/profile_faker")
@limiter.limit("5000 per day")
@limiter.limit("500 per hour")
def profile_faker_api():
    """Generate fake user profile data.

    Returns:
            JSON with fake profile data (name, address, email, etc.)
    """
    try:
        return jsonify(profile_faker())
    except Exception as e:
        logger.error(f"Profile faker API error: {str(e)}")
        return jsonify(error="Internal error"), 500


@app.route("/api/v1/senti")
@limiter.limit("5000 per day")
@limiter.limit("500 per hour")
def senti_api():
    """Analyze text sentiment (positive/negative/neutral).

    Query params:
            text or t: The text to analyze

    Returns:
            JSON with sentiment probabilities and label
    """
    text = request.args.get("text") or request.args.get("t", "")

    if not text or not text.strip():
        return (
            jsonify(
                error="Missing parameter",
                message="Please provide 'text' parameter",
                example="/api/v1/senti?text=I love this!",
            ),
            400,
        )

    try:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        form_data = {"text": text.strip()}

        # Use HTTPS instead of HTTP for security
        response = requests.post(
            "https://text-processing.com/api/sentiment/",
            data=form_data,
            headers=headers,
            timeout=10,
        )

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            logger.error(f"Sentiment API returned status {response.status_code}")
            return jsonify(error="External API error", message="Failed to analyze sentiment"), 502

    except requests.Timeout:
        logger.error("Sentiment API timeout")
        return jsonify(error="Timeout", message="Request timed out"), 504
    except Exception as e:
        logger.error(f"Sentiment API error: {str(e)}")
        return jsonify(error="Internal error", message="Failed to process request"), 500


@app.route("/senti")
@limiter.exempt
def senti_view():
    return render_template("senti.html")


###############################################
# Demo UI
###############################################


@app.route("/clean_skill")
@limiter.exempt
def clean_skill_view():
    return render_template("clean_skill.html")


@app.route("/clean_datetime")
@limiter.exempt
def clean_datetime_view():
    return render_template("clean_datetime.html")


@app.route("/profile_faker")
@limiter.exempt
def profile_faker_view():
    return render_template("profile_faker.html")


@app.errorhandler(404)
@limiter.exempt
def page_not_found(e):
    """Return a custom 404 error."""
    return (
        jsonify(
            error="Not found",
            message="The requested endpoint does not exist",
            suggestion="Check the API documentation at /",
        ),
        404,
    )


@app.route("/nn")
@limiter.exempt
def neural_network():
    return render_template("nn/index.html")
