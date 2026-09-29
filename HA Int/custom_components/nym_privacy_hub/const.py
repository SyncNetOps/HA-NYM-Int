"""Constants for the Nym Privacy Hub integration."""

DOMAIN = "nym_privacy_hub"

# Configuration keys
CONF_PROXY_HOST = "proxy_host"
CONF_PROXY_PORT = "proxy_port"
CONF_AI_VOICE_PRIVACY = "ai_voice_privacy"
CONF_GEO_WEATHER_PRIVACY = "geo_weather_privacy"
CONF_COVER_TRAFFIC = "cover_traffic"
CONF_COVER_TRAFFIC_RATE = "cover_traffic_rate"
CONF_CUSTOM_PROVIDER = "custom_provider"
CONF_PASSPHRASE = "passphrase"

# Defaults
DEFAULT_PROXY_HOST = "127.0.0.1"
DEFAULT_PROXY_PORT = 1080
DEFAULT_AI_VOICE_PRIVACY = True
DEFAULT_GEO_WEATHER_PRIVACY = True
DEFAULT_COVER_TRAFFIC = False
DEFAULT_COVER_TRAFFIC_RATE = 10  # packets per min
DEFAULT_SCAN_INTERVAL = 30  # seconds

# Platforms
PLATFORMS = ["sensor", "switch", "button"]
