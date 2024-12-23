import json
import logging

from flask import Blueprint, current_app, jsonify, request, send_file
from neo4j_service import PhonRepository

phone_bp = Blueprint('phone_bp', __name__)


@phone_bp.route('/phone_tracker', methods=['POST'])
def phone_tracker():
    print(request.json)

    data = request.get_json()

    try:
        repo = PhonRepository(current_app.driver)
        phon_call_id = repo.create_phon_call(data)

        current_app.redis.lpush(
            'recent_transactions',
            json.dumps({**data, 'transaction_id': phon_call_id})
        )
        current_app.redis.ltrim('recent_transactions', 0, 999)

        return jsonify({
            'status': 'success',
            'transaction_id': phon_call_id
        }), 201
    except Exception as e:
        print(f'Error in POST /api/v1/transaction: {str(e)}')
        logging.error(f'Error in POST /api/v1/transaction: {str(e)}')
        return jsonify({'error': str(e)}), 500



@phone_bp.route('/bluetooth_paths', methods=['GET'])
def get_bluetooth_paths():
    max_depth = request.args.get('max_depth', None)

    cache_key = 'bluetooth_paths'
    cached = current_app.redis.get(cache_key)
    if cached:
        return jsonify({"paths": json.loads(cached)}), 200

    try:
        repo = PhonRepository(current_app.driver)
        paths = repo.get_bluetooth_paths(max_depth)

        current_app.redis.setex(
            cache_key,
            600,
            json.dumps(paths)
        )

        return jsonify({"paths": paths}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@phone_bp.route('/signal_strength', methods=['GET'])
def get_signal_strength():

    cache_key = 'signal_strength'
    cached = current_app.redis.get(cache_key)
    if cached:
        return jsonify({"signal_strength": json.loads(cached)}), 200

    try:
        repo = PhonRepository(current_app.driver)
        signal_strength = repo.get_signal_strength()

        current_app.redis.setex(
            cache_key,
            600,
            json.dumps(signal_strength)
        )

        return jsonify({"signal_strength": signal_strength}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@phone_bp.route('/connected_device', methods=['GET'])
def get_connected_device():
    id = request.args.get('id', None)

    if not id:
        return jsonify({"error": "id required"}), 400

    cache_key = f'connected_device_{id}'
    cached = current_app.redis.get(cache_key)
    if cached:
        return jsonify({"device id": id ,"connected_devices": json.loads(cached)}), 200

    try:
        repo = PhonRepository(current_app.driver)
        devices = repo.get_connected_device(id)

        current_app.redis.setex(
            cache_key,
            600,
            json.dumps(devices)
        )

        return jsonify({"device id": id ,"connected_devices": devices}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@phone_bp.route('/is_connected', methods=['GET'])
def check_direct_connection():
    from_device_id = request.args.get('from_device_id')
    to_device_id = request.args.get('to_device_id')

    if not from_device_id or not to_device_id:
        return jsonify({"error": "from_device_id and to_device_id are required"}), 400

    cache_key = f'connected_device_{from_device_id}_{to_device_id}'
    cached = current_app.redis.get(cache_key)

    if cached:
        return jsonify({
            "from_device_id": from_device_id,
            "to_device_id": to_device_id,
            "connected": json.loads(cached)
        }),200

    try:
        repo = PhonRepository(current_app.driver)
        connected = repo.is_connected(from_device_id, to_device_id)

        current_app.redis.setex(
            cache_key,
            600,
            json.dumps(connected)
        )

        return jsonify({
            "from_device_id": from_device_id,
            "to_device_id": to_device_id,
            "connected": connected
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@phone_bp.route('/recent_connection', methods=['GET'])
def get_recent_connection():
    device_id = request.args.get('device_id')
    if not device_id:
        return jsonify({"error": "device_id required"}), 400

    cache_key = f'recent_connection_{device_id}'
    cached = current_app.redis.get(cache_key)

    if cached:
        return jsonify({"device_id": device_id, "recent_connection": json.loads(cached)}), 200

    try:
        repo = PhonRepository(current_app.driver)
        connection = repo.get_recent_connection(device_id)
        if connection:

            current_app.redis.setex(
                cache_key,
                600,
                json.dumps(connection)
            )

            return jsonify({"device_id": device_id, "recent_connection": connection}), 200
        else:
            return "no connection found for dis device", 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



