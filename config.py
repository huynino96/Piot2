import os


config = {
        "local_database": os.path.join(os.path.abspath(os.path.dirname(__file__)), "a2.db"),
        "host": "127.0.0.1",
        "user": "car",
        "password": "123456",
        "database": "car",
        "client_secrets": os.path.join(os.path.abspath(os.path.dirname(__file__)), "client_secrets.json"),
        "udp_client_port": 5555,
        "udp_server_port": 9999,
        "dataset": os.path.join(os.path.abspath(os.path.dirname(__file__)), "Dataset"),
        "speech_credentials": os.path.join(os.path.abspath(os.path.dirname(__file__)), "service_account_key.json")
}