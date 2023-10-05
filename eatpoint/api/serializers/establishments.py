from drf_spectacular.utils import (
    extend_schema_field,
)
from rest_framework import serializers

from establishments.models import (
    Establishment,
    WorkEstablishment,
    Kitchen,
    Work,
    TableEstablishment,
)


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"


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
    start = serializers.TimeField(
        source="order_dt.start",
        format="%I:%M",
    )
    end = serializers.TimeField(
        source="order_dt.end",
        format="%I:%M",
    )

    class Meta:
        model = WorkEstablishment
        fields = [
            "name",
            "start",
            "end",
        ]


class TableEstablishmentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="table.id")
    name = serializers.ReadOnlyField(source="table.name")
    description = serializers.ReadOnlyField(source="table.description")
    slug = serializers.ReadOnlyField(source="table.slug")

    class Meta:
        model = TableEstablishment
        fields = [
            "id",
            "name",
            "description",
            "slug",
            "seats",
            "status",
        ]


class EstablishmentSerializer(serializers.ModelSerializer):
    worked = serializers.SerializerMethodField("get_work")
    kitchen = KitchenSerializer(read_only=True, many=True)
    tables = serializers.SerializerMethodField("get_table")

    class Meta:
        fields = "__all__"
        model = Establishment

    @extend_schema_field(WorkSerializer(many=True))
    def get_work(self, obj):
        order_dt = WorkEstablishment.objects.filter(establishment=obj)
        return WorkEstablishmentSerializer(order_dt, many=True).data

    @extend_schema_field(TableEstablishmentSerializer(many=True))
    def get_table(self, obj):
        table = TableEstablishment.objects.filter(establishment=obj)
        return TableEstablishmentSerializer(table, many=True).data
