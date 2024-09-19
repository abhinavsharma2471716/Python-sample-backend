from flask import Flask, request, jsonify
from flask_caching import Cache

app = Flask(__name__)

# Configuring Flask-Caching
cache = Cache(config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})
cache.init_app(app)

# Set initial data in cache (optional, just for demonstration)
cache.set("1", {"text": "Default value for user 1"})
cache.set("2", {"text": "Default value for user 2"})

# API to get the current value for a specific user_id
@app.route('/data/<user_id>/text', methods=['GET'])
def get_data(user_id):
    user_data = cache.get(user_id)
    if user_data:
        return user_data['text'], 200  # Return plain text
    return "User not found", 404  # Return plain text error message

# API to update the value of the text field for a specific user_id
@app.route('/data/<user_id>', methods=['PUT'])
def update_data(user_id):
    user_data = cache.get(user_id)
    if not user_data:
        return jsonify({"error": "User not found"}), 404
    
    new_text = request.json.get('text', '')
    user_data['text'] = new_text
    cache.set(user_id, user_data)  # Update cache with new data
    return jsonify(user_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
