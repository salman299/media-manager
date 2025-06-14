import pytest
from api.utils import get_media_url


class TestUtils:
    """Test cases for utility functions."""

    def test_get_media_url(self):
        """Test get_media_url function."""
        url = get_media_url('st', '12345')
        expected_url = 'https://www.imago-images.de/bild/st/0000012345/s.jpg'
        assert url == expected_url
        
        # Test with single digit number
        url = get_media_url('st', '1')
        expected_url = 'https://www.imago-images.de/bild/st/0000000001/s.jpg'
        assert url == expected_url 