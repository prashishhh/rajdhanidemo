from django.urls import path
from .views import demo, nepali_tts, tts_health

urlpatterns = [
    path("", demo, name="tts_demo"),
    path("health/", tts_health, name="tts_health"),
    path("nepali-tts/", nepali_tts, name="nepali_tts"),
]
