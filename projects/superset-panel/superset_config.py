import os

SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY", "change-me")

# Permite iframe embed no portfólio
TALISMAN_ENABLED = False
WTF_CSRF_ENABLED = False

FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DASHBOARD_RBAC": False,
}

# Aceita requisições de qualquer origem (necessário para embed)
CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["*"],
    "resources": ["*"],
    "origins": ["*"],
}
ENABLE_CORS = True

# Role público pode ver dashboards compartilhados
PUBLIC_ROLE_LIKE = "Gamma"

# Desabilita redirect HTTPS (Cloudflare Tunnel já faz isso)
PREFERRED_URL_SCHEME = "https"
