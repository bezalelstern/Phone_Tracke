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
    try:
        repo = PhonRepository(current_app.driver)
        paths = repo.get_bluetooth_paths()

        return jsonify({"paths": paths}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@phone_bp.route('/signal_strength', methods=['GET'])
def get_signal_strength():
    try:
        repo = PhonRepository(current_app.driver)
        paths = repo.get_signal_strength()

        return jsonify({"paths": paths}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

