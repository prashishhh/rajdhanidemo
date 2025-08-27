# tts/views.py
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from gtts import gTTS
from io import BytesIO
from django.conf import settings

def demo(request):
    # Your demo page (the one with the textarea + Listen button)
    return render(request, "tts_demo.html")

def tts_health(request):
    # Optional: quick check (kept for convenience)
    return JsonResponse({"engine": "gTTS", "lang": "ne"})

@csrf_exempt              # OK for prototype; add CSRF later for production
@require_POST
def nepali_tts(request):
    text = (request.POST.get("text") or "").strip()
    if not text:
        return JsonResponse({"error": "No text provided"}, status=400)

    # gTTS supports Nepali via lang="ne"
    # If the article is extremely long, trim for prototype (adjust as you like)
    MAX_CHARS = 8000
    text = text[:MAX_CHARS]

    try:
        mp3_buf = BytesIO()
        gTTS(text=text, lang="ne", slow=False).write_to_fp(mp3_buf)
        mp3_buf.seek(0)
        resp = HttpResponse(mp3_buf.read(), content_type="audio/mpeg")
        resp["Content-Disposition"] = 'inline; filename="news-nepali-tts.mp3"'
        return resp
    except Exception as e:
        return JsonResponse({"error": "gTTS error", "details": repr(e)}, status=500)
