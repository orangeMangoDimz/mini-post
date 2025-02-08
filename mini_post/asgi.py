import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from posts import urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_post.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
      "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(urls.websocket_urlpatterns))
        ),
    # Just HTTP for now. (We can add other protocols later.)
})

