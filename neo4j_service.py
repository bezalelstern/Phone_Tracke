from datetime import datetime, timedelta
import io

class PhonRepository:
    def __init__(self, driver):
        self.driver = driver

    def create_phon_call(self, transaction_data):
        with self.driver.session() as session:
            query = """
            MERGE (device1:Device {id: $from_device_id, brand: $from_device_brand, model: $from_device_model, name: $from_device_name})
            MERGE (device2:Device {id: $to_device_id, brand: $to_device_brand, model: $to_device_model, name: $to_device_name})
            MERGE (device1)-[r:CONNECTED {
                method: $method,
                bluetooth_version: $bluetooth_version,
                signal_strength_dbm: $signal_strength_dbm,
                distance_meters: $distance_meters,
                duration_seconds: $duration_seconds,
                timestamp: $timestamp
            }]->(device2)
            RETURN id(r) AS phon_call_id
            """

            device1, device2 = transaction_data['devices']
            interaction = transaction_data['interaction']

            params = {
                "from_device_id": device1['id'],
                "from_device_brand": device1['brand'],
                "from_device_model": device1['model'],
                "from_device_name": device1['name'],

                "to_device_id": device2['id'],
                "to_device_brand": device2['brand'],
                "to_device_model": device2['model'],
                "to_device_name": device2['name'],

                "method": interaction['method'],
                "bluetooth_version": interaction['bluetooth_version'],
                "signal_strength_dbm": interaction['signal_strength_dbm'],
                "distance_meters": interaction['distance_meters'],
                "duration_seconds": interaction['duration_seconds'],
                "timestamp": interaction['timestamp'],
            }

            result = session.run(query, params)
            return result.single()['phon_call_id']


    def get_bluetooth_paths(self, max_depth= 50):
        query = """
        MATCH path = (device1:Device)-[r:CONNECTED*2 ..%d]->(device2:Device)
        WHERE ALL(rel IN relationships(path) WHERE rel.method = 'Bluetooth')
        RETURN 
            device1.id AS from_device,
            device1.name AS from_name,
            device2.id AS to_device,
            device2.name AS to_name,
            relationships(path) AS calls,
            length(path) AS cycle_length
        ORDER BY cycle_length DESC
        """ % max_depth

        with self.driver.session() as session:
            results = session.run(query)
            return [
                {"from_device": record["from_device"],
                 "from_name" : record["from_name"],
                 "to_device": record["to_device"],
                 "to_name" : record["to_name"],
                 "cycle_length": record["cycle_length"],
                "calls": [dict(call) for call in record["calls"] ]
                 }
                for record in results
            ]

    def get_signal_strength(self):
        query = """
                MATCH (device1:Device)-[r:CONNECTED]->(device2:Device)
                WHERE r.signal_strength_dbm > -60
                RETURN device1.id AS from_device, device1.name AS from_name, 
                       device2.id AS to_device, device2.name AS to_name, 
                       r.signal_strength_dbm AS signal_strength
                ORDER BY signal_strength DESC
                """
        with self.driver.session() as session:
            results = session.run(query)

            return [dict(record) for record in results]

    def get_connected_device(self, id):
        query = """
        MATCH (device:Device)-[:CONNECTED]->(connected:Device)
        WHERE device.id = $id
        RETURN COUNT(connected) AS connected_count
        """
        with self.driver.session() as session:
            results = session.run(query, id = id)
            record = results.single()
            return record["connected_count"]
