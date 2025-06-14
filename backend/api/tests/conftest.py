import pytest
from unittest.mock import Mock, patch
from rest_framework.test import APIClient


@pytest.fixture
def mock_elasticsearch_client():
    """Fixture to mock Elasticsearch client."""
    # Patch the Elasticsearch client in the services module where it's actually used
    with patch("api.services.Elasticsearch") as mock_es:
        mock_client = Mock()
        mock_es.return_value = mock_client
        yield mock_client


@pytest.fixture
def es_service(mock_elasticsearch_client):
    """Fixture to create ElasticsearchService with mocked client."""
    from api.services import ElasticsearchService

    service = ElasticsearchService()
    # Replace the client instance with our mock
    service.client = mock_elasticsearch_client
    return service


@pytest.fixture
def api_client():
    """Fixture to create API client."""
    return APIClient()


@pytest.fixture
def sample_search_response():
    """Fixture to provide sample Elasticsearch search response."""
    return {
        "hits": {
            "total": {"value": 2},
            "hits": [
                {
                    "_id": "1",
                    "_score": 1.0,
                    "_source": {
                        "bildnummer": "12345",
                        "datum": "2024-01-01T00:00:00",
                        "suchtext": "Test image 1",
                        "fotografen": "John Doe",
                        "breite": 800,
                        "hoehe": 600,
                        "db": "st",
                    },
                },
                {
                    "_id": "2",
                    "_score": 0.8,
                    "_source": {
                        "bildnummer": "67890",
                        "datum": "2024-01-02T00:00:00",
                        "suchtext": "Test image 2",
                        "fotografen": "Jane Smith",
                        "breite": 1024,
                        "hoehe": 768,
                        "db": "st",
                    },
                },
            ],
        },
        "aggregations": {
            "db_terms": {"buckets": [{"key": "st", "doc_count": 2}]},
            "photographer_terms": {
                "buckets": [
                    {"key": "John Doe", "doc_count": 1},
                    {"key": "Jane Smith", "doc_count": 1},
                ]
            },
        },
    }
