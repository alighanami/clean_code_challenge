from typing import Optional
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from interns_challenges_number1.d_1 import get_status_list_from_query
from interns_challenges_number1.d_2 import payout_collection
from interns_challenges_number1.tools import create_paginate_response
from interns_challenges_number1.payout_filters import build_payout_match
from interns_challenges_number1.sorting import build_sorting


class PayoutListAPIView(APIView):
    """
    GET /api/payout/
    Adapter Layer:
    - collects inputs
    - calls pure logic
    - returns response
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        # ----------------------------
        # Query Params
        # ----------------------------
        statuses: Optional[str] = request.query_params.get("statuses")
        start_date: Optional[str] = request.query_params.get("start_date")
        end_date: Optional[str] = request.query_params.get("end_date")
        payment_start_date: Optional[str] = request.query_params.get("payment_start_date")
        payment_end_date: Optional[str] = request.query_params.get("payment_end_date")
        user_type: Optional[str] = request.query_params.get("user_type")

        page: Optional[str] = request.query_params.get("page")

        sort_by: Optional[str] = request.query_params.get("sort_by")
        direction: str = request.query_params.get("direction", "desc")

        # ----------------------------
        # Status parsing
        # ----------------------------
        status_list = None
        if statuses:
            status_list = get_status_list_from_query(statuses)

        # ----------------------------
        # Pure Filter Logic
        # ----------------------------
        match = build_payout_match(
            start_date=start_date,
            end_date=end_date,
            payment_start_date=payment_start_date,
            payment_end_date=payment_end_date,
            user_type=user_type,
            statuses=status_list,
        )

        # ----------------------------
        # Pure Sorting Logic
        # ----------------------------
        sorting = build_sorting(sort_by, direction)

        # ----------------------------
        # Pagination / Response
        # ----------------------------
        data = create_paginate_response(
            page=page,
            collection=payout_collection,
            match=match,
            # sorting deliberately not applied here (Stage 7)
        )

        return Response(data, status=status.HTTP_200_OK)