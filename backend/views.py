from django.db.models import Sum, Window, F
from django.db.models.functions import RowNumber
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Pontuacao, Palestrante, Espectador
from .serializers import PontuacaoSerializer, EspectadorSerializer, VerificarNomeSerializer


class PontuacaoCreateUpdateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=PontuacaoSerializer)
    def post(self, request):
        espectador_id = request.data.get('espectador')
        palestrante_id = request.data.get('palestrante')
        score_val = request.data.get('score')

        if not espectador_id:
            return Response(
                {'detail': 'O campo "espectador" é obrigatório.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if palestrante_id is None or score_val is None:
            return Response(
                {'detail': 'Você precisa enviar "palestrante" e "score".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2) Busca o palestrante
        try:
            palestrante = Palestrante.objects.get(pk=palestrante_id)
        except Palestrante.DoesNotExist:
            return Response(
                {'detail': 'Palestrante não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            espectador = Espectador.objects.get(pk=espectador_id)
        except Espectador.DoesNotExist:
            return Response(
                {'detail': 'Espectador não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3) update_or_create pela dupla (espectador, palestrante)
        pontuacao, created = Pontuacao.objects.update_or_create(
            espectador=espectador,
            palestrante=palestrante,
            defaults={'score': score_val}
        )

        # 4) Serializa e retorna 201 se criou, 200 se atualizou
        serializer = PontuacaoSerializer(pontuacao)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class EspectadorCreateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=EspectadorSerializer)
    def post(self, request):
        nome = request.data.get('nome')
        avatar = request.data.get('avatar')

        if not nome:
            return Response(
                {'detail': 'O campo "nome" é obrigatório.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not avatar:
            return Response(
                {'detail': 'O campo "avatar" é obrigatório.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2) Cria o espectador
        espectador = Espectador.objects.create(nome=nome, avatar=avatar)

        # 3) Serializa e retorna 201
        serializer = EspectadorSerializer(espectador)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class SpeakerRankingAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, speaker_id):
        # ranking de um palestrante específico
        qs = Pontuacao.objects.filter(palestrante_id=speaker_id) \
            .annotate(rank=Window(
                expression=RowNumber(),
                order_by=F('score').desc()
            ))
        data = [
            {
                'espectador': p.espectador.nome,
                'score': p.score,
                'rank': p.rank,
                'avatar': p.espectador.avatar,
            } for p in qs
        ]
        return Response(data)


class OverallRankingAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # ranking geral (soma de todas as pontuações do espectador)
        agg = Pontuacao.objects.values('espectador') \
            .annotate(total_score=Sum('score')) \
            .order_by('-total_score')

        data = [
            {
                'espectador': Espectador.objects.get(id=a['espectador']).nome,
                'score': a['total_score'],
                'rank': idx + 1,
                'avatar': Espectador.objects.get(id=a['espectador']).avatar  # Aqui estamos pegando o avatar
            } for idx, a in enumerate(agg)
        ]
        return Response(data)


class VerificaNomeAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=VerificarNomeSerializer)
    def post(self, request):
        serializer = VerificarNomeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {'detail': 'Nome disponível.'},
            status=status.HTTP_200_OK
        )