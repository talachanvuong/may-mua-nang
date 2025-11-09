from datetime import date, datetime, timedelta

import plotly.graph_objs as go
from dateutil.relativedelta import relativedelta
from flask import Blueprint, render_template, request, session
from plotly.offline import plot

from app.services.favorite_service import FavoriteService
from app.services.log_service import LogService
from app.services.weather_service import WeatherService
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
    minDay = today - relativedelta(months=3)
    maxDay = today + timedelta(days=16)

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
