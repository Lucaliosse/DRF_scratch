import logging
from django.db import connection, reset_queries
from django.conf import settings

logger = logging.getLogger(__name__)


class QueryCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG:
            reset_queries()

        response = self.get_response(request)

        if settings.DEBUG:
            num_queries = len(connection.queries)
            logger.info(
                f"{request.method} {request.path} - Status: {response.status_code} - "
                f"Queries: {num_queries}"
            )

        return response
