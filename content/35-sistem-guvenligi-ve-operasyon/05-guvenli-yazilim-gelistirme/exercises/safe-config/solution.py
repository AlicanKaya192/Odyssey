DEFAULTS = {"debug": False, "tls": True, "session_minutes": 30}


def load_config(user_config):
    config = dict(DEFAULTS)
    for key, value in user_config.items():
        if key in DEFAULTS:
            config[key] = value
    config["session_minutes"] = min(config["session_minutes"], 60)
    return config

config = load_config({"debug": True, "session_minutes": 600, "theme": "dark"})
for key in sorted(config):
    print(key, config[key])
