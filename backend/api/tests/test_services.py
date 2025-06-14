import pytest
from unittest.mock import Mock, patch


class TestElasticsearchService:
    """Test cases for ElasticsearchService."""

    def test_search_with_query(self, es_service, mock_elasticsearch_client, sample_search_response):
        """Test search with query parameters."""
        mock_elasticsearch_client.search.return_value = sample_search_response
        
        query_params = {
            "query": "test",
            "page": 1,
            "page_size": 20,
            "sort_by": "date",
            "sort_order": "desc"
        }
        
        result = es_service.search(query_params)
        
        # Verify the search was called with correct parameters
        mock_elasticsearch_client.search.assert_called_once()
        call_args = mock_elasticsearch_client.search.call_args[1]
        assert call_args["index"] == es_service.index
        
        # Verify the query structure
        query = call_args["body"]["query"]
        assert "bool" in query
        assert "must" in query["bool"]
        assert len(query["bool"]["must"]) > 0
        
        # Verify the result
        assert result == sample_search_response

    def test_search_with_filters(self, es_service, mock_elasticsearch_client, sample_search_response):
        """Test search with filters."""
        mock_elasticsearch_client.search.return_value = sample_search_response
        
        query_params = {
            "db": "st",
            "photographer": "John Doe",
            "page": 1,
            "page_size": 20
        }
        
        result = es_service.search(query_params)
        
        # Verify the search was called with correct parameters
        mock_elasticsearch_client.search.assert_called_once()
        call_args = mock_elasticsearch_client.search.call_args[1]
        
        # Verify the filter structure
        query = call_args["body"]["query"]
        assert "bool" in query
        assert "filter" in query["bool"]
        assert len(query["bool"]["filter"]) == 2
        
        # Verify the result
        assert result == sample_search_response

    def test_get_by_id(self, es_service, mock_elasticsearch_client):
        """Test getting a single media item by ID."""
        mock_response = {
            "_id": "1",
            "_source": {
                "bildnummer": "12345",
                "datum": "2024-01-01T00:00:00",
                "suchtext": "Test image",
                "fotografen": "John Doe",
                "breite": 800,
                "hoehe": 600,
                "db": "st"
            }
        }
        mock_elasticsearch_client.get.return_value = mock_response
        
        result = es_service.get_by_id("1")
        
        mock_elasticsearch_client.get.assert_called_once_with(
            index=es_service.index,
            id="1"
        )
        assert result == mock_response 