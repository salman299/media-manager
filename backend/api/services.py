import logging
from elasticsearch import Elasticsearch
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)


class ElasticsearchService:
    """Service class for handling Elasticsearch operations."""

    def __init__(self):
        """Initialize the Elasticsearch client."""
        self.client = Elasticsearch(
            f"{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}",
            basic_auth=(
                settings.ELASTICSEARCH_USERNAME,
                settings.ELASTICSEARCH_PASSWORD,
            ),
            verify_certs=False,
        )
        self.index = settings.ELASTICSEARCH_INDEX

    def search(self, query_params):
        """
        Search for media items in Elasticsearch.

        Args:
            query_params (dict): Search parameters including query, filters, pagination, etc.

        Returns:
            dict: Raw Elasticsearch response
        """
        try:
            search_query = self._build_search_query(query_params)
            response = self.client.search(index=self.index, body=search_query)
            return response

        except Exception as e:
            logger.error(f"Error searching Elasticsearch: {str(e)}")
            raise

    def _build_search_query(self, params):
        """
        Build the Elasticsearch query based on the provided parameters.

        Args:
            params (dict): Search parameters

        Returns:
            dict: Elasticsearch query
        """
        query = {"bool": {"must": [], "filter": []}}

        # Add text search if query is provided
        if params.get("query"):
            query["bool"]["must"].append(
                {
                    "multi_match": {
                        "query": params["query"],
                        "fields": ["suchtext^3", "fotografen^2"],
                        "type": "best_fields",
                        "operator": "and",
                    }
                }
            )

        # Add database filter if db is provided
        if params.get("db"):
            if len(params["db"]) == 1:
                # Use term query for single value
                query["bool"]["filter"].append({"term": {"db": params["db"][0]}})
            else:
                # Use terms query for multiple values
                query["bool"]["filter"].append({"terms": {"db": params["db"]}})

        # Add date range filter if dates are provided
        if params.get('date_from') or params.get('date_to'):
            date_filter = {'range': {'datum': {}}}
            if params.get('date_from'):
                date_filter['range']['datum']['gte'] = params['date_from'].isoformat()
            if params.get('date_to'):
                date_filter['range']['datum']['lte'] = params['date_to'].isoformat()
            query['bool']['filter'].append(date_filter)

        # Add photographer filter if provided
        if params.get("photographer"):
            if len(params["photographer"]) == 1:
                # Use term query for single value
                query["bool"]["filter"].append({"term": {"fotografen": params["photographer"][0]}})
            else:
                # Use terms query for multiple values
                query["bool"]["filter"].append({"terms": {"fotografen": params["photographer"]}})

        # Build the complete search body
        search_body = {
            "query": query,
            "from": (params.get("page", 1) - 1) * params.get("page_size", 20),
            "size": params.get("page_size", 20),
            "sort": self._build_sort(params),
        }

        # Add aggregations
        search_body["aggs"] = {
            "db_terms": {"terms": {"field": "db", "size": 10}},
            "photographer_terms": {"terms": {"field": "fotografen", "size": 20}},
            # 'date_histogram': {
            #     'date_histogram': {
            #         'field': 'datum',
            #         'calendar_interval': 'month',
            #         'format': 'yyyy-MM'
            #     }
            # }
        }

        return search_body

    def _build_sort(self, params):
        """Build the sort parameters for the search query."""
        sort_by = params.get("sort_by", "datum")
        sort_order = params.get("sort_order", "desc")

        # Map frontend sort fields to Elasticsearch fields
        sort_field_mapping = {
            "date": "datum",
            "photographer": "fotografen",
            "id": "bildnummer",
        }

        es_field = sort_field_mapping.get(sort_by, sort_by)

        return [{es_field: {"order": sort_order}}]

    def get_global_aggregations(self):
        """
        Fetch global aggregations for filter options (db and photographers).

        Returns:
            dict: Raw Elasticsearch aggregations response.
        """
        try:
            aggregation_query = {
                "size": 0,  # No hits needed, only aggregations
                "aggs": {
                    "all_docs": {
                        "global": {},
                        "aggs": {
                            "db_terms": {
                                "terms": {
                                    "field": "db",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "photographer_terms": {
                                "terms": {
                                    "field": "fotografen",
                                    "size": 10000,
                                    "order": {"_count": "desc"}
                                }
                            }
                        }
                    }
                }
            }
            response = self.client.search(index=self.index, body=aggregation_query)
            print(f"Raw Elasticsearch aggregations response: {response.get('aggregations')}") # Debug log
            return response.get("aggregations", {})
        except Exception as e:
            logger.error(f"Error fetching global aggregations: {str(e)}")
            raise

    def get_by_id(self, media_id):
        """
        Retrieve a single media item by ID.

        Args:
            media_id (str): The media item ID

        Returns:
            dict: The media item if found, None otherwise
        """
        try:
            response = self.client.get(index=self.index, id=media_id)
            return response
        except Exception as e:
            logger.error(f"Error retrieving media item {media_id}: {str(e)}")
            return None
