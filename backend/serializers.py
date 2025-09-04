import unicodedata
from rest_framework import serializers, permissions
from .models import Pontuacao, Palestrante, Espectador


class PontuacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pontuacao
        fields = ('espectador', 'palestrante', 'score')


class PalestranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Palestrante
        fields = ('id', 'nome')


class EspectadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espectador
        fields = ('id', 'nome', 'avatar')


class VerificarNomeSerializer(serializers.Serializer):
    permission_classes = [permissions.AllowAny]

    nome = serializers.CharField(
        max_length=150,
        required=True,
        help_text="Nome do espectador a ser verificado"
    )

    def validate_nome(self, value):
        def remover_acentos(s: str) -> str:
            return ''.join(
                c for c in unicodedata.normalize('NFD', s)
                if unicodedata.category(c) != 'Mn'
            )

        # 1) limpa espaços e normaliza
        cleaned = value.strip()
        norm_value = remover_acentos(cleaned).lower()

        # 2) verifica todos os nomes já cadastrados,
        #    removendo acentos e comparando em minúsculo
        existentes = Espectador.objects.values_list('nome', flat=True)
        for nome_existente in existentes:
            if remover_acentos(nome_existente).lower() == norm_value:
                raise serializers.ValidationError("Nome já está cadastrado.")

        return cleaned