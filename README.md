
# PackWise — Shipping Box Recommendation System

A Django-based shipping box recommendation system for ecommerce platforms. PackWise evaluates product dimensions, order weight, box dimensions, weight capacity, and packaging cost to recommend a suitable shipping box for each order.

## Features

- **Product Management:** Store product dimensions and unit weights.
- **Shipping Box Management:** Maintain box dimensions, maximum weight capacities, costs, and availability.
- **Order Management:** Create orders and associate products with quantities.
- **Smart Box Recommendation:** Evaluate available boxes and recommend the lowest-cost suitable option.
- **3D Packing Heuristic:** Consider rectangular product rotations and non-overlapping placements.
- **REST API:** Retrieve box recommendations for existing orders.
- **Warehouse Dashboard:** View recommendations through an HTML, CSS, and JavaScript interface.
- **Django Admin:** Manage products, boxes, orders, and order items.
- **Automated Tests:** Test packing behavior, box selection, and API error handling.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework and ORM |
| Django REST Framework | Recommendation API |
| SQLite | Development database |
| HTML5 | Frontend structure |
| CSS3 | Responsive dashboard styling |
| Vanilla JavaScript | API integration and dynamic UI |
| Django Test Framework | Automated testing |

## Project Structure

```text
shipping_system/
├── manage.py
├── README.md
├── shipping_system/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── packaging/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── services.py
    ├── views.py
    ├── urls.py
    ├── tests.py
    ├── migrations/
    ├── templates/
    │   └── packaging/
    │       └── dashboard.html
    └── static/
        └── packaging/
            ├── css/
            │   └── style.css
            └── js/
                └── dashboard.js
```

## Prerequisites

- Python 3.10 or newer
- pip
- Git (optional)

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd shipping_system
```

If you have not uploaded the project to GitHub, navigate directly to your project directory instead.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Linux or macOS:

```bash
source venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install django djangorestframework
```

Save the dependencies for future installations:

```bash
pip freeze > requirements.txt
```

### 4. Configure Django

Ensure `rest_framework` and `packaging` are included in `INSTALLED_APPS` in `shipping_system/settings.py`.

Ensure the project-level URL configuration includes the packaging app:

```python
path("", include("packaging.urls")),
```

The default SQLite database can be used for local development.

### 5. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create an administrator

```bash
python manage.py createsuperuser
```

Follow the prompts to configure your admin credentials.

### 7. Start the development server

```bash
python manage.py runserver
```

## Access the Application

| Resource | URL |
|---|---|
| Warehouse Dashboard | http://127.0.0.1:8000/ |
| Django Admin | http://127.0.0.1:8000/admin/ |
| Box Recommendation API | http://127.0.0.1:8000/api/orders/1/recommend-box/ |

Replace `1` with an existing order's database ID.

## How It Works

1. Create products with their length, width, height, and unit weight.
2. Define shipping boxes with internal dimensions, maximum weight capacity, cost, and active status.
3. Create an order and add its products with their respective quantities.
4. Enter the order ID in the warehouse dashboard.
5. The backend calculates the total product weight.
6. Boxes that cannot support the total weight are excluded.
7. The packing heuristic evaluates possible product orientations and placements.
8. The system returns the lowest-cost box found that passes the packing check.
9. If no box is found, the API returns an explanatory error response.

## API Documentation

### Recommend a Shipping Box

**Endpoint**

```http
GET /api/orders/<order_id>/recommend-box/
```

**Example request**

```bash
curl http://127.0.0.1:8000/api/orders/1/recommend-box/
```

**Example successful response**

```json
{
  "order_id": 1,
  "order_number": "ORD-1001",
  "recommended_box": {
    "id": 1,
    "name": "Small",
    "dimensions_cm": {
      "length": "25.00",
      "width": "20.00",
      "height": "10.00"
    },
    "maximum_weight_kg": "2.000",
    "cost": "20.00"
  },
  "total_weight_kg": "1.000"
}
```

The response above is illustrative; actual values depend on the records in your database.

### Error Responses

| HTTP status | Meaning |
|---|---|
| 404 Not Found | The requested order does not exist. |
| 422 Unprocessable Entity | No box was found by the recommendation algorithm. |

## Data Model

### Product

Stores the product name, dimensions, and unit weight.

### ShippingBox

Stores the box name, internal dimensions, maximum weight capacity, cost, and whether it is active.

### Order

Represents an ecommerce order with a unique order number and creation timestamp.

### OrderItem

Associates products with orders and records the quantity of each product.

## Packing Logic

The recommendation service:

- Calculates total product weight, including quantities.
- Filters out inactive boxes and boxes with insufficient weight capacity.
- Considers 90-degree rotations of rectangular products.
- Attempts to position products without overlapping.
- Evaluates boxes in ascending order of cost.
- Returns the first box for which the heuristic finds a valid arrangement.

**Important limitation:** This implementation uses a greedy 3D packing heuristic. It does not guarantee finding every possible valid arrangement. A failed packing attempt does not prove that a box is physically unsuitable. For production use, consider a stronger packing solver and account for protective packaging, dimensional tolerances, fragile products, and handling restrictions.

## Running Tests

Run the application tests with:

```bash
python manage.py test packaging
```

The test suite should cover:

- Product fit and rotation.
- Oversized products.
- Multiple-product placement.
- Lowest-cost box selection.
- Weight-capacity restrictions.
- Missing-order API responses.

Add further tests for edge cases as the packing algorithm evolves.

## Future Improvements

- Display all pending orders in the dashboard.
- Select orders from a table instead of manually entering IDs.
- Save the recommended box and packaging decision against the order.
- Add order statuses such as Pending, Recommended, and Packed.
- Improve 3D packing optimization.
- Add authentication and role-based permissions for warehouse staff.
- Add API validation and more detailed error handling.
- Add PostgreSQL for production deployment.
- Add audit logs and recommendation history.
- Deploy the application using Docker and a production-ready web server.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Run the test suite.
5. Submit a pull request.

## License

Specify a license before distributing this project publicly.
