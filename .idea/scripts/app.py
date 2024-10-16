from flask import Flask, request, jsonify
from weather import get_weather
from ai_background import get_ai_response

app = Flask(__name__)

@app.route('/api/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    weather_info = get_weather(city)

    if weather_info:
        return jsonify(weather_info)
    else:
        return jsonify({"error": "Could not fetch weather data"}), 500

@app.route('/api/ai', methods=['GET'])
def ai():
    query = request.args.get('query')
    ai_response = get_ai_response(query)

    if ai_response:
        return jsonify({"response": ai_response})
    else:
        return jsonify({"error": "Could not fetch AI response"}), 500

if __name__ == '__main__':
    app.run(debug=True)