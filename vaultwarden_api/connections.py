from .vaultwarden import VaultwardenAPI
from os import environ

try:
    VAULTWARDEN_URL = environ["VAULTWARDEN_URL"]
    VAULTWARDEN_TOKEN = environ["VAULTWARDEN_TOKEN"]
except KeyError:
    raise RuntimeError("VAULTWARDEN_URL and VAULTWARDEN_TOKEN must be set in the environment")

vw_api = VaultwardenAPI(VAULTWARDEN_URL, VAULTWARDEN_TOKEN)
