from rest_framework import serializers

from establishments.models import Establishment


class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Establishment
