DEFAULTS = {"debug": False, "tls": True, "session_minutes": 30}


def load_config(user_config):
    config = dict(DEFAULTS)
    config.update(user_config)
    return config

config = load_config({"debug": True, "session_minutes": 600, "theme": "dark"})
for key in sorted(config):
    print(key, config[key])
