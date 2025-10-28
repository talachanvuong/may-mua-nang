from flask import Blueprint, render_template, request
from app.utils.decorators import token_required
from app.services.weather_service import WeatherService
weather_bp = Blueprint("weather", __name__)

@weather_bp.route("/search", methods=["GET"])
@token_required
def search():
    location  = request.args.get("location","").strip()
    
    result = []
    if location :
        result = WeatherService.search(location)
        if result: return render_template('weather.html', location=location, results = result)
        else : return render_template('weather.html', not_found=True, location=location)
    return render_template('weather.html', location = location )


@weather_bp.route("current", methods =["GET"])
@token_required
def current():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    name = request.args.get("name","Location Undefine!")
    
    weather = None
    if lat and lon:
        weather = WeatherService.get_weather_info(lat, lon)
    return render_template("weather.html", weather = weather, location_name = name)


