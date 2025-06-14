from django.conf import settings


def get_media_url(db, bildnummer):
    """
    Generate the URL for an image from the Imago database.

    Args:
        db (str): The database identifier for the image
        bildnummer (str): The Bildnummer of the image

    Returns:
        str: The complete URL to access the image in small format
    """
    padded_id = str(bildnummer).zfill(10)
    return f"{settings.IMAGO_BASE_URL}/bild/{db}/{padded_id}/s.jpg"
