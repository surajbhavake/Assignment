from django.test import TestCase

# Create your tests here.

from decimal import Decimal

from django.test import TestCase

from .models import Product, ShippingBox, Order, OrderItem
from .services import can_pack, recommend_box


class PackingAlgorithmTests(TestCase):

    def test_product_fits_in_box(self):
        self.assertTrue(
            can_pack([(20, 15, 10)], (25, 20, 15))
        )

    def test_product_fits_after_rotation(self):
        self.assertTrue(
            can_pack([(20, 10, 15)], (15, 20, 10))
        )

    def test_product_too_large(self):
        self.assertFalse(
            can_pack([(40, 30, 20)], (25, 20, 15))
        )

    def test_multiple_products_fit_without_overlap(self):
        self.assertTrue(
            can_pack(
                [(10, 10, 10), (10, 10, 10)],
                (20, 10, 10),
            )
        )

    def test_volume_alone_does_not_guarantee_fit(self):
        # Each item fits individually, but both cannot
        # fit side by side in this box.
        self.assertFalse(
            can_pack(
                [(6, 6, 6), (6, 6, 6)],
                (10, 10, 10),
            )
        )


class BoxRecommendationTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Keyboard",
            length=Decimal("20"),
            width=Decimal("15"),
            height=Decimal("5"),
            weight=Decimal("1.0"),
        )

        self.order = Order.objects.create(
            order_number="ORD-1001"
        )

        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
        )

        ShippingBox.objects.create(
            name="Small",
            length=Decimal("25"),
            width=Decimal("20"),
            height=Decimal("10"),
            max_weight=Decimal("2"),
            cost=Decimal("20"),
        )

        ShippingBox.objects.create(
            name="Medium",
            length=Decimal("35"),
            width=Decimal("25"),
            height=Decimal("15"),
            max_weight=Decimal("5"),
            cost=Decimal("30"),
        )

    def test_selects_cheapest_suitable_box(self):
        result = recommend_box(self.order)

        self.assertTrue(result["success"])
        self.assertEqual(result["box"].name, "Small")
        self.assertEqual(result["box_cost"], Decimal("20"))

    def test_excludes_box_with_insufficient_capacity(self):
        box = ShippingBox.objects.get(name="Small")
        box.max_weight = Decimal("0.5")
        box.save()

        result = recommend_box(self.order)

        self.assertTrue(result["success"])
        self.assertEqual(result["box"].name, "Medium")

    def test_inactive_box_is_not_recommended(self):
        ShippingBox.objects.filter(name="Small").update(
            is_active=False
        )

        result = recommend_box(self.order)

        self.assertTrue(result["success"])
        self.assertEqual(result["box"].name, "Medium")

    def test_no_box_fits_returns_failure(self):
        ShippingBox.objects.all().update(is_active=False)

        result = recommend_box(self.order)

        self.assertFalse(result["success"])
        self.assertIn("No available box", result["message"])



from rest_framework.test import APITestCase
from rest_framework import status


class RecommendationAPITests(APITestCase):

    def test_unknown_order_returns_404(self):
        response = self.client.get(
            "/api/orders/999999/recommend-box/"
        )

        self.assertEqual(response.status_code, 404)