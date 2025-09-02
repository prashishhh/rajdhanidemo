from django.urls import path
from .views import nepali_tts, demo

urlpatterns = [
    path("", demo, name="tts_demo"),                 # GET demo page
    path("nepali-tts/", nepali_tts, name="nepali_tts"),  # POST returns MP3
]
