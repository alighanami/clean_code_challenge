from rest_framework.views import APIView
from rest_framework.response import Response
from interns_challenges_number1.payout_filters import build_payout_match
from interns_challenges_number1.pagination import paginate
from interns_challenges_number1.sorting import build_sorting
from payouts.repositories.mongo.payout_repository import list_payouts


class PayoutListApi(APIView):
    def get(self, request):
        match = build_payout_match(
            statuses=request.query_params.getlist("status"),
            start_date=request.query_params.get("start_date"),
            end_date=request.query_params.get("end_date"),
        )

        pagination = paginate(
            page=request.query_params.get("page", 1),
            page_size=request.query_params.get("page_size", 10),
        )

        sorting = build_sorting(
            sort_by=request.query_params.get("sort_by"),
            direction=request.query_params.get("direction"),
        )

        data = list_payouts(
            match=match,
            pagination=pagination,
            sorting=sorting,
        )

        return Response(data)