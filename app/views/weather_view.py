from datetime import date, datetime, timedelta

import folium
import plotly.graph_objs as go
import requests
from dateutil.relativedelta import relativedelta
from flask import Blueprint, render_template, request, session
from folium.features import DivIcon
from plotly.offline import plot

from app.services.favorite_service import FavoriteService
from app.services.log_service import LogService
from app.services.weather_service import WeatherService
from app.utils.convert import weather_icon
from app.utils.decorators import token_required

weather_bp = Blueprint('weather', __name__)


@weather_bp.route('/search', methods=['GET', 'POST'])
@token_required
def search():
    keyword = request.args.get('keyword')

    if keyword:
        user = session['user']

        results = WeatherService.search(keyword)

        for result in results:
            is_favorited = FavoriteService.get_by_place(user['id'], result['id'])
            result['is_favorited'] = True if is_favorited else False

        log = {
            'message': f'Đã tìm kiếm khu vực <b class="text-blue-500">{keyword}</b>',
            'user': user['id']
        }

        LogService.add(log)

        return render_template('weather_search.html', keyword=keyword, results=results)

    return render_template('weather_search.html')


@weather_bp.route('/info', methods=['GET'])
@token_required
def info():
    location = session['location']
    user = session['user']

    today = date.today()
    minDay = today - relativedelta(months=2)
    maxDay = today + timedelta(days=14)

    name = request.args.get('name', location['district'])
    admin1 = request.args.get('admin1')
    country = request.args.get('country')
    latitude = request.args.get('latitude', location['latitude'])
    longitude = request.args.get('longitude', location['longitude'])
    time = request.args.get('time', today)
    option = request.args.get('option', 'temperature_2m')

    info = {
        'name': name,
        'latitude': latitude,
        'longitude': longitude,
        'time': time,
        'minDay': minDay,
        'maxDay': maxDay,
        'option': option
    }

    area = name

    if admin1:
        info['admin1'] = admin1
        area += f', {admin1}'

    if country:
        info['country'] = country
        area += f', {country}'

    hours = [f'{hour}:00' for hour in range(24)]
    now = f'{datetime.now().hour}:00'

    weather_info = WeatherService.info(latitude, longitude, time, option)
    unit = weather_info['unit']
    data = weather_info['data']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=hours,
        y=data,
        mode='lines',
        line=dict(color='#155DFC', shape='spline'),
        fill='tozeroy',
        hovertemplate=f'%{{y}} {unit} lúc %{{x}}<extra></extra>'
    ))

    fig.add_shape(
        type='line',
        x0=now,
        x1=now,
        y0=0,
        y1=1,
        xref='x',
        yref='paper',
        line=dict(color='#FB2C36', dash='dash')
    )

    fig.update_xaxes(
        ticklabelstep=2,
        ticklabelposition='inside'
    )

    fig.update_layout(
        xaxis=dict(
            fixedrange=(True),
            tickfont=dict(color='#FB2C36', size=14),
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            fixedrange=(True),
            tickfont=dict(color='#FB2C36', size=14),
            showgrid=False,
            zeroline=False
        ),
        dragmode=False,
        hovermode='closest',
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)'
    )

    config = {
        'displayModeBar': False,
        'scrollZoom': False,
        'doubleClick': False
    }

    chart = plot(fig, output_type='div', include_plotlyjs=True, config=config)

    if option == 'temperature_2m':
        option_name = 'nhiệt độ'
    elif option == 'relative_humidity_2m':
        option_name = 'độ ẩm'
    elif option == 'cloud_cover':
        option_name = 'mây che phủ'
    elif option == 'wind_speed_10m':
        option_name = 'tốc độ gió'
    elif option == 'wind_direction_10m':
        option_name = 'hướng gió'
    elif option == 'precipitation_probability':
        option_name = 'khả năng mưa'
    elif option == 'precipitation':
        option_name = 'lượng mưa'
    elif option == 'uv_index':
        option_name = 'UV'

    converted_time = datetime.strptime(str(time), '%Y-%m-%d').strftime('%d/%m/%Y')

    log = {
        'message': f'Đã xem <b class="text-blue-500">{option_name}</b> vào <b class="text-blue-500">{converted_time}</b> tại khu vực <b class="text-blue-500">{area}</b>',
        'user': user['id']
    }

    LogService.add(log)

    return render_template('weather_info.html', info=info, chart=chart)


def classify_alert(data):
    """Trả về thông báo cảnh báo cho từng chỉ số"""
    alerts = []

    # AQI
    if data["aqi"] is not None:
        if data["aqi"] <= 50:
            alerts.append("🌿 Không khí tốt.")
        elif data["aqi"] <= 100:
            alerts.append("😐 Chất lượng không khí trung bình.")
        else:
            alerts.append("⚠️ Không khí ô nhiễm, nên hạn chế ra ngoài.")

    # UV Index
    if data["uv_index"] is not None:
        if data["uv_index"] >= 8:
            alerts.append("🌞 Cảnh báo tia UV rất cao! Bôi kem chống nắng.")
        elif data["uv_index"] >= 6:
            alerts.append("☀️ Tia UV cao, nên tránh nắng giữa trưa.")

    # Độ ẩm
    if data["humidity"] is not None:
        if data["humidity"] < 40:
            alerts.append("💧 Không khí khô, nên uống thêm nước.")
        elif data["humidity"] > 75:
            alerts.append("💦 Độ ẩm cao, dễ gây khó chịu hoặc nấm mốc.")

    # Xác suất mưa
    if data["precipitation_chance"] > 70:
        alerts.append("🌧️ Khả năng mưa cao, nhớ mang theo ô.")

    # Nhiệt độ trung bình
    if data["temperature_mean"] > 35:
        alerts.append("🔥 Nắng nóng, tránh hoạt động ngoài trời.")
    elif data["temperature_mean"] < 20:
        alerts.append("🧥 Trời lạnh, nên mặc ấm.")

    return alerts


def get_forecast(days_ahead_list, LAT, LON):
    TIMEZONE = 'Asia/Bangkok'

    WEATHER_URL = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={LAT}&longitude={LON}"
        f"&daily=temperature_2m_max,temperature_2m_min,uv_index_max,"
        f"rain_sum,precipitation_probability_max,weather_code,wind_speed_10m_max"
        f"&hourly=relative_humidity_2m,precipitation,cloud_cover_mid,temperature_2m"
        f"&timezone={TIMEZONE}&forecast_days=14"
    )

    AQI_URL = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality?"
        f"latitude={LAT}&longitude={LON}"
        f"&hourly=pm10,pm2_5,us_aqi,us_aqi_pm2_5,us_aqi_pm10"
        f"&timezone={TIMEZONE}&forecast_days=7"
    )

    w_data = requests.get(WEATHER_URL, timeout=10).json()
    aqi_data = requests.get(AQI_URL, timeout=10).json()
    today = date.today()
    result = []

    # --- Gom AQI trung bình từng ngày ---
    aqi_daily_dict = {}
    if "hourly" in aqi_data and "us_aqi" in aqi_data["hourly"]:
        for ts, val in zip(aqi_data["hourly"]["time"], aqi_data["hourly"]["us_aqi"]):
            if val is None:
                continue
            day = ts.split("T")[0]
            aqi_daily_dict.setdefault(day, []).append(val)
        for day in list(aqi_daily_dict.keys()):
            vals = aqi_daily_dict[day]
            aqi_daily_dict[day] = round(sum(vals) / len(vals))

    # --- AQI trung bình 7 ngày đầu (dự đoán 8–14) ---
    if aqi_daily_dict:
        aqi_avg7 = round(sum(aqi_daily_dict.values()) / len(aqi_daily_dict))
    else:
        aqi_avg7 = None

    for d in days_ahead_list:
        target = today + timedelta(days=d)
        date_str = target.isoformat()

        if date_str not in w_data["daily"]["time"]:
            continue
        idx = w_data["daily"]["time"].index(date_str)

        rh_values = [
            v for i, v in enumerate(w_data["hourly"]["relative_humidity_2m"])
            if w_data["hourly"]["time"][i].startswith(date_str) and v is not None
        ]
        humidity = round(sum(rh_values) / len(rh_values)) if rh_values else None

        cloud_values = [
            v for i, v in enumerate(w_data["hourly"]["cloud_cover_mid"])
            if w_data["hourly"]["time"][i].startswith(date_str) and v is not None
        ]
        cloud_cover = round(sum(cloud_values) / len(cloud_values)) if cloud_values else None

        raw_rain = w_data["daily"]["rain_sum"][idx]
        prob = w_data["daily"]["precipitation_probability_max"][idx]
        if raw_rain == 0 and prob > 30:
            if prob < 50:
                rain_est = 0.5
            elif prob < 70:
                rain_est = 2
            elif prob < 90:
                rain_est = 5
            else:
                rain_est = 10
        else:
            rain_est = raw_rain

        if date_str in aqi_daily_dict:
            aqi_val = aqi_daily_dict[date_str]
        else:
            aqi_val = aqi_avg7

        temp_max = w_data["daily"]["temperature_2m_max"][idx]
        temp_min = w_data["daily"]["temperature_2m_min"][idx]
        data = {
            "date": date_str,
            "temperature_max": round(temp_max),
            "temperature_min": round(temp_min),
            "temperature_mean": round((temp_max + temp_min) / 2),
            "humidity": humidity,
            "cloud_cover": cloud_cover,
            "precipitation": round(rain_est, 2),
            "precipitation_chance": round(prob),
            "wind_speed": round(w_data["daily"]["wind_speed_10m_max"][idx]),
            "uv_index": round(w_data["daily"]["uv_index_max"][idx]),
            "aqi": aqi_val,
            "weathercode": int(w_data["daily"]["weather_code"][idx])
        }

        # 🔔 Thêm cảnh báo
        data["alerts"] = classify_alert(data)
        result.append(data)

    return result


@weather_bp.route("/forecast14", methods=['GET'])
@token_required
def forecast14():
    location = session['location']

    name = request.args.get('name', location['district'])
    admin1 = request.args.get('admin1')
    country = request.args.get('country')
    latitude = request.args.get('latitude', location['latitude'])
    longitude = request.args.get('longitude', location['longitude'])

    area = name

    if admin1:
        area += f', {admin1}'

    if country:
        area += f', {country}'

    data = get_forecast(list(range(0, 15)), latitude, longitude)

    for d in data:
        d['date'] = datetime.strptime(str(d['date']), '%Y-%m-%d').strftime('%d/%m/%Y')

    return render_template("forecast14.html", forecasts=data, area=area)


@weather_bp.route('/map')
@token_required
def map():
    user = session['user']
    favorites = FavoriteService.get_all(user['id'])
    data = WeatherService.map(favorites)

    map = folium.Map()

    locations = []

    for d in data:
        latitude = d['latitude']
        longitude = d['longitude']
        area = d['area']
        weather_code = weather_icon(d['weather_code'])
        temperature_2m = d['temperature_2m']

        locations.append([latitude, longitude])

        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(area, max_width=9999),
            icon=DivIcon(
                icon_size=(80, 60),
                icon_anchor=(40, 30),
                html=f'''
                    <div style="text-align: center; background-color: rgba(255, 255, 255, 0.8); border-radius: 16px">
                        <p style="font-size: 36px">{weather_code}</p>
                        <p style="font-size: 18px; font-weight: bold">{temperature_2m} °C</p>
                    </div>
                '''
            )
        ).add_to(map)

    map.fit_bounds(locations)

    return render_template('weather_map.html', map=map._repr_html_())
