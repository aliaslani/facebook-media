from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class DevExtremePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'   # ← allows ?page_size=25 from grid
    max_page_size = 100                   # ← safety cap

    def get_paginated_response(self, data):
        return Response({
            "data": data,
            "totalCount": self.page.paginator.count
        })

    # ── required so DRF schema generation doesn't blow up ───────────────────
    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "data": schema,
                "totalCount": {"type": "integer"},
            }
        }