from django.urls import path
from .views import nepali_tts

urlpatterns = [
    path("nepali-tts/", nepali_tts, name="nepali_tts"),
]


from django.urls import path
from .views import nepali_tts, demo

urlpatterns = [
    path("", demo, name="tts_demo"),                 # GET demo page
    path("nepali-tts/", nepali_tts, name="nepali_tts"),  # POST returns MP3
]


from django.urls import path
from .views import demo, nepali_tts, tts_health

urlpatterns = [
    path("", demo, name="tts_demo"),
    path("health/", tts_health, name="tts_health"),
    path("nepali-tts/", nepali_tts, name="nepali_tts"),
]

