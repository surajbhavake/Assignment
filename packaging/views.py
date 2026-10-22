from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from .services import recommend_box


@api_view(["GET"])
def recommend_box_view(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    result = recommend_box(order)

    if not result["success"]:
        return Response(
            result,
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    box = result["box"]

    return Response({
        "order_id": order.id,
        "order_number": order.order_number,
        "recommended_box": {
            "id": box.id,
            "name": box.name,
            "dimensions_cm": {
                "length": box.length,
                "width": box.width,
                "height": box.height,
            },
            "maximum_weight_kg": box.max_weight,
            "cost": box.cost,
        },
        "total_weight_kg": result["total_weight"],
    })


from django.shortcuts import render


def dashboard_view(request):
    return render(request, "packaging/dashboard.html")

