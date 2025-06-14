import pytest
from api.serializers import SearchQuerySerializer, MediaSourceSerializer


class TestSerializers:
    """Test cases for serializers."""

    def test_search_query_serializer(self):
        """Test SearchQuerySerializer validation."""
        # Test valid data
        valid_data = {
            'query': 'test',
            'page': 1,
            'page_size': 20,
            'sort_by': 'date',
            'sort_order': 'desc'
        }
        serializer = SearchQuerySerializer(data=valid_data)
        assert serializer.is_valid()
        
        # Test invalid data
        invalid_data = {
            'page': 0,  # Invalid page number
            'page_size': 200  # Invalid page size
        }
        serializer = SearchQuerySerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert 'page' in serializer.errors
        assert 'page_size' in serializer.errors

    def test_media_source_serializer(self):
        """Test MediaSourceSerializer."""
        data = {
            'bildnummer': '12345',
            'datum': '2024-01-01T00:00:00',
            'suchtext': 'Test image',
            'fotografen': 'John Doe',
            'breite': 800,
            'hoehe': 600,
            'db': 'st'
        }
        
        # Test validation
        serializer = MediaSourceSerializer(data=data)
        assert serializer.is_valid()
        
        # Test to_representation with a dictionary input
        representation = serializer.to_representation(data)
        assert 'image_number' in representation
        assert 'date' in representation
        assert 'search_text' in representation
        assert 'photographers' in representation
        assert 'height' in representation
        assert 'width' in representation
        assert 'database' in representation
        assert 'thumbnail_url' in representation 