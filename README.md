# DRF API

Project initialized with:
`python -m venv ./.venv`
`source .venv/bin/activate`
`pip install Django==6.1`
`django-admin startproject training`


Linux command to activate venv:
`source .venv/bin/activate`
Equivalent command on Windows:
`.venv\Scripts\Activate`

To apply the migrations:
`python manage.py migrate`

To run the server:
`python manage.py runserver`

Web access:
Swagger UI: http://127.0.0.1:8000/api/schema/swagger-ui/
ReDoc: http://127.0.0.1:8000/api/schema/redoc/

To run unit tests:
`pytest`
To run one specific unit test:
`pytest test_views.py::TestProductViewset::test_filter_products_by_category_id`

Formatting: black. Use an extension ("Black Formatter" on VScode) or manually format with:
`pip install black`
`black .`

Features:
- Query counting middleware, to track the number of database queries for each API calls in the API logs in DEBUG.


