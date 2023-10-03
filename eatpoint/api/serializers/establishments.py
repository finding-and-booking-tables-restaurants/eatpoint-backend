from rest_framework import serializers

from establishments.models import Establishment, WorkEstablishment, Kitchen


class KitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = [
            "id",
            "name",
            "description",
            "slug",
        ]


class WorkEstablishmentSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(
        source="order_dt.name",
    )
    start = serializers.ReadOnlyField(
        source="order_dt.start",
    )
    end = serializers.ReadOnlyField(
        source="order_dt.end",
    )
    lunch_start = serializers.ReadOnlyField(
        source="order_dt.lunch_start",
    )
    lunch_end = serializers.ReadOnlyField(
        source="order_dt.lunch_end",
    )

    class Meta:
        model = WorkEstablishment
        fields = [
            "name",
            "start",
            "end",
            "lunch_start",
            "lunch_end",
        ]


class EstablishmentSerializer(serializers.ModelSerializer):
    worked = serializers.SerializerMethodField("get_work")
    kitchen = KitchenSerializer(read_only=True, many=True)

    class Meta:
        fields = "__all__"
        model = Establishment

    def get_work(self, obj):
        order_dt = WorkEstablishment.objects.filter(establishment=obj)
        return WorkEstablishmentSerializer(order_dt, many=True).data
