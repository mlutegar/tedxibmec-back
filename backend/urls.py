from django.urls import path
from .views import (
    PontuacaoCreateUpdateAPIView,
    SpeakerRankingAPIView,
    OverallRankingAPIView, EspectadorCreateAPIView, VerificaNomeAPIView
)

urlpatterns = [
    path('scores/', PontuacaoCreateUpdateAPIView.as_view(), name='submit-score'),
    path('rankings/speaker/<int:speaker_id>/', SpeakerRankingAPIView.as_view(), name='speaker-ranking'),
    path('rankings/overall/', OverallRankingAPIView.as_view(), name='overall-ranking'),
    path('espectador/', EspectadorCreateAPIView.as_view(), name='espectador-create'),
    path('verifica-nome/', VerificaNomeAPIView.as_view(), name='verifica-nome'),
]
