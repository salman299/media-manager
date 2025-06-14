# Media Manager Backend

A Django-based backend service for managing and retrieving media content from Elasticsearch.

## Architecture Overview

### Tech Stack
- Django 5.0.2 with Django REST Framework 3.14.0
- Elasticsearch 8.11.1 integration for media content retrieval
- CORS support with django-cors-headers
- Comprehensive test suite with pytest and pytest-cov
- Production-ready with Gunicorn and Whitenoise
- Environment configuration with python-dotenv

## Features
- Elasticsearch integration for media content retrieval
- Advanced search and filtering capabilities
- Image processing with Pillow
- Real-time search suggestions
- Error handling and loading states
- Comprehensive logging and monitoring
- Production-ready deployment configuration

## Setup Instructions

### Prerequisites
- Python 3.9+ (managed via pyenv)
- Docker and Docker Compose (optional)
- Elasticsearch credentials (provided in the challenge)

### Environment Setup

#### Python Setup with pyenv
1. Install pyenv (if not already installed):
```bash
# macOS
brew install pyenv

# Linux
curl https://pyenv.run | bash
```

2. Add pyenv to your shell configuration:
```bash
# Add to ~/.zshrc or ~/.bashrc
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

3. Install and set up Python:
```bash
pyenv install 3.9.18  # or your preferred 3.9+ version
pyenv global 3.9.18
```

### Backend Setup
1. Create and activate a virtual environment using pyenv:
```bash
cd backend
pyenv virtualenv 3.9.18 media-manager-env
pyenv local media-manager-env
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env  # Create your .env file from example
# Edit .env with your Elasticsearch credentials and other settings
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

### Production Setup
The backend is configured for production deployment with:
- Gunicorn as the WSGI server
- Whitenoise for static file serving
- Environment-based configuration
- Production-grade security settings

To run in production mode:
```bash
python manage.py collectstatic
gunicorn media_manager.wsgi:application
```

## Development Considerations

### Data Normalization
- Implemented data validation and normalization in the Django serializers
- Custom Elasticsearch query builder for consistent search results
- Field mapping and transformation utilities

### Scalability
- Elasticsearch for efficient search and retrieval
- Pagination for large result sets

### Monitoring and Logging
- Django logging configuration in `backend/logs/`
- Performance monitoring
- API usage metrics
- Test coverage reports

### Testing
- Backend: pytest with pytest-django and pytest-cov for coverage
- Integration tests for API endpoints

## License
MIT

## Author
Ali Salman
