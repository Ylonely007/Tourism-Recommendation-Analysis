"""
ASGI config for 去哪儿旅游数据分析推荐系统 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '去哪儿旅游数据分析推荐系统.settings')

application = get_asgi_application()
