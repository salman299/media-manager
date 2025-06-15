from django.shortcuts import render
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import SearchQuerySerializer, ElasticsearchResponseSerializer, GlobalAggregationsSerializer
from .services import ElasticsearchService

logger = logging.getLogger(__name__)


class MediaAPIView(APIView):
    """
    ViewSet for handling media search operations.
    Provides endpoints for searching media items in Elasticsearch.
    """

    permission_classes = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.es_service = ElasticsearchService()

    def get(self, request):
        """
        Search for media items in Elasticsearch.

        Args:
            request: The HTTP request containing search parameters

        Returns:
            Response: The search results
        """
        serializer = SearchQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            results = self.es_service.search(serializer.validated_data)
            results_dict = {
                "total": results.get("hits", {}).get("total", {}).get("value", 0),
                "aggregations": results.get("aggregations", {}),
                "results": results.get("hits", {}).get("hits", []),
            }
            # Pass the raw response directly to the serializer
            response_serializer = ElasticsearchResponseSerializer(data=results_dict)
            if not response_serializer.is_valid():
                logger.error(
                    f"Serializer validation error: {response_serializer.errors}"
                )
                return Response(
                    {"error": "Error processing search results"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            return Response(response_serializer.data)
        except Exception as e:
            logger.error(f"Error in media search: {str(e)}")
            return Response(
                {"error": "An error occurred while searching media items"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AggregationAPIView(APIView):
    """
    API view for fetching global aggregations.
    """
    permission_classes = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.es_service = ElasticsearchService()

    def get(self, request):
        """
        Retrieve global aggregations for filter options.
        """
        try:
            aggregations_data = self.es_service.get_global_aggregations()
            serializer = GlobalAggregationsSerializer(data=aggregations_data.get("all_docs", {}))
            if not serializer.is_valid():
                logger.error(f"Aggregation serializer validation error: {serializer.errors}")
                return Response(
                    {"error": "Error processing aggregations"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching aggregations: {str(e)}")
            return Response(
                {"error": "An error occurred while fetching aggregations"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
