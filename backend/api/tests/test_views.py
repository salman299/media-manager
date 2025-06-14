import pytest
from unittest.mock import Mock, patch
from django.urls import reverse
from rest_framework import status


class TestMediaAPIView:
    """Test cases for MediaAPIView."""

    @patch('api.views.ElasticsearchService')
    def test_search_endpoint(self, mock_es_service, api_client, sample_search_response):
        """Test the search endpoint."""
        # Create a mock instance of ElasticsearchService
        mock_service_instance = Mock()
        mock_service_instance.search.return_value = sample_search_response
        mock_es_service.return_value = mock_service_instance
        
        url = reverse('media-list')
        response = api_client.get(url, {
            'query': 'test',
            'page': 1,
            'page_size': 20
        })
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['total'] == 2
        assert len(data['results']) == 2
        assert 'aggregations' in data

    def test_search_endpoint_invalid_params(self, api_client):
        """Test the search endpoint with invalid parameters."""
        url = reverse('media-list')
        response = api_client.get(url, {
            'page': 0,  # Invalid page number
            'page_size': 200  # Invalid page size
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST 