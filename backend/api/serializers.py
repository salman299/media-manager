from rest_framework import serializers

from api.utils import get_media_url


class SearchQuerySerializer(serializers.Serializer):
    """Serializer for search query parameters."""

    query = serializers.CharField(required=False, allow_blank=True)
    db = serializers.CharField(required=False, allow_blank=True)
    page = serializers.IntegerField(default=1, min_value=1)
    page_size = serializers.IntegerField(default=20, min_value=1, max_value=100)
    sort_by = serializers.CharField(required=False, allow_blank=True)
    sort_order = serializers.ChoiceField(
        choices=["asc", "desc"], default="desc", required=False
    )
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    photographer = serializers.CharField(required=False, allow_blank=True)


class MediaSourceSerializer(serializers.Serializer):
    """Serializer for media source data from Elasticsearch."""

    bildnummer = serializers.CharField()
    datum = serializers.DateTimeField()
    suchtext = serializers.CharField()
    fotografen = serializers.CharField()
    breite = serializers.IntegerField()
    hoehe = serializers.IntegerField()
    db = serializers.CharField()
    thumbnail_url = serializers.SerializerMethodField(read_only=True)

    def get_thumbnail_url(self, obj):
        """Generate thumbnail URL from the bildnummer field."""
        bildnummer = obj.get("bildnummer", "")
        db = obj.get("db", "st")
        return get_media_url(db, bildnummer)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            "image_number": data["bildnummer"],
            "date": data["datum"],
            "search_text": data["suchtext"],
            "photographers": data["fotografen"],
            "height": data["hoehe"],
            "width": data["breite"],
            "database": data["db"],
            "thumbnail_url": data["thumbnail_url"],
        }


class ElasticsearchHitSerializer(serializers.Serializer):
    """Serializer for individual Elasticsearch hit."""

    _id = serializers.CharField()
    _score = serializers.FloatField(required=False, allow_null=True)
    _source = MediaSourceSerializer()
    sort = serializers.ListField(required=False, allow_null=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            "id": data["_id"],
            "source": data["_source"],
        }


class ElasticsearchResponseSerializer(serializers.Serializer):
    """Serializer for Elasticsearch search results."""

    total = serializers.IntegerField()
    results = ElasticsearchHitSerializer(many=True)
    aggregations = serializers.DictField(required=False)
