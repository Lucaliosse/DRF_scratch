import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from training.models import Category, Product


@pytest.fixture
def api_client():
    """Fixture to provide an API client for testing."""
    return APIClient()


@pytest.fixture
def category_active(db):
    """Fixture to create an active category."""
    return Category.objects.create(
        name="Electronics", description="Electronic products", active=True
    )


@pytest.fixture
def category_inactive(db):
    """Fixture to create an inactive category."""
    return Category.objects.create(
        name="Inactive Category", description="This category is inactive", active=False
    )


@pytest.fixture
def product_active(db, category_active):
    """Fixture to create an active product."""
    return Product.objects.create(
        name="Laptop",
        description="High-performance laptop",
        active=True,
        category=category_active,
    )


@pytest.fixture
def product_inactive(db, category_active):
    """Fixture to create an inactive product."""
    return Product.objects.create(
        name="Inactive Product",
        description="This product is inactive",
        active=False,
        category=category_active,
    )


@pytest.mark.django_db
class TestCategoryViewset:
    """Test cases for CategoryViewset."""

    def test_list_categories_returns_only_active(
        self, api_client, category_active, category_inactive
    ):
        """Test that listing categories returns all categories."""
        url = reverse("category-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        names = {cat["name"] for cat in response.data}
        assert names == {category_active.name, category_inactive.name}

    def test_list_categories_empty_when_no_active(self, api_client, category_inactive):
        """Test that listing returns the inactive category."""
        url = reverse("category-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == category_inactive.name

    def test_create_category(self, api_client):
        """Test creating a new category."""
        url = reverse("category-list")
        data = {"name": "Books", "description": "Book products", "active": True}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.count() == 1
        assert Category.objects.first().name == "Books"

    def test_retrieve_category(self, api_client, category_active):
        """Test retrieving a single category."""
        url = reverse("category-detail", kwargs={"pk": category_active.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == category_active.name
        assert response.data["id"] == category_active.id

    def test_update_category(self, api_client, category_active):
        """Test updating a category."""
        url = reverse("category-detail", kwargs={"pk": category_active.pk})
        data = {
            "name": "Updated Electronics",
            "description": "Updated description",
            "active": True,
        }
        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        category_active.refresh_from_db()
        assert category_active.name == "Updated Electronics"

    def test_partial_update_category(self, api_client, category_active):
        """Test partially updating a category."""
        url = reverse("category-detail", kwargs={"pk": category_active.pk})
        data = {"name": "Partially Updated"}
        response = api_client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        category_active.refresh_from_db()
        assert category_active.name == "Partially Updated"

    def test_delete_category(self, api_client, category_active):
        """Test deleting a category."""
        url = reverse("category-detail", kwargs={"pk": category_active.pk})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Category.objects.count() == 0

    def test_disable_category(self, api_client, category_active, product_active):
        """Test disabling a category disables the category and all its products."""
        url = reverse("category-disable", kwargs={"pk": category_active.pk})
        response = api_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"]

        category_active.refresh_from_db()
        product_active.refresh_from_db()

        assert category_active.active is False
        assert product_active.active is False


@pytest.mark.django_db
class TestProductViewset:
    """Test cases for ProductViewset."""

    def test_list_products_returns_only_active(
        self, api_client, product_active, product_inactive
    ):
        """Test that listing products returns only active products."""
        url = reverse("product-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == product_active.name
        assert response.data[0]["active"] is True

    def test_list_products_empty_when_no_active(self, api_client, product_inactive):
        """Test that listing returns empty when there are no active products."""
        url = reverse("product-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_create_product(self, api_client, category_active):
        """Test creating a new product."""
        url = reverse("product-list")
        data = {
            "name": "Smartphone",
            "description": "Latest smartphone",
            "active": True,
            "category": category_active.id,
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.count() == 1
        assert Product.objects.first().name == "Smartphone"

    def test_retrieve_product(self, api_client, product_active):
        """Test retrieving a single product."""
        url = reverse("product-detail", kwargs={"pk": product_active.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == product_active.name
        assert response.data["id"] == product_active.id

    def test_update_product(self, api_client, product_active, category_active):
        """Test updating a product."""
        url = reverse("product-detail", kwargs={"pk": product_active.pk})
        data = {
            "name": "Updated Laptop",
            "description": "Updated description",
            "active": True,
            "category": category_active.id,
        }
        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        product_active.refresh_from_db()
        assert product_active.name == "Updated Laptop"

    def test_partial_update_product(self, api_client, product_active):
        """Test partially updating a product."""
        url = reverse("product-detail", kwargs={"pk": product_active.pk})
        data = {"name": "Partially Updated"}
        response = api_client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        product_active.refresh_from_db()
        assert product_active.name == "Partially Updated"

    def test_delete_product(self, api_client, product_active):
        """Test deleting a product."""
        url = reverse("product-detail", kwargs={"pk": product_active.pk})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Product.objects.count() == 0

    def test_filter_products_by_category_id(
        self, api_client, category_active, product_active
    ):
        """Test filtering products by category_id query parameter."""
        # Create another category and product
        other_category = Category.objects.create(
            name="Clothing", description="Clothing products", active=True
        )
        other_product = Product.objects.create(
            name="Shirt",
            description="Cotton shirt",
            active=True,
            category=other_category,
        )

        # Filter by first category
        url = reverse("product-list")
        response = api_client.get(url, {"category_id": category_active.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == product_active.name
        assert response.data[0]["category"] == category_active.id

    def test_filter_products_by_nonexistent_category(self, api_client, product_active):
        """Test filtering products by a category_id that doesn't exist."""
        url = reverse("product-list")
        response = api_client.get(url, {"category_id": 99999})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_filter_products_with_multiple_categories(self, api_client):
        """Test filtering products when multiple categories exist."""
        # Create two categories
        cat1 = Category.objects.create(name="Category 1", active=True)
        cat2 = Category.objects.create(name="Category 2", active=True)

        # Create products in each category
        Product.objects.create(name="Product 1", active=True, category=cat1)
        Product.objects.create(name="Product 2", active=True, category=cat1)
        Product.objects.create(name="Product 3", active=True, category=cat2)

        # Filter by category 1
        url = reverse("product-list")
        response = api_client.get(url, {"category_id": cat1.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        # Filter by category 2
        response = api_client.get(url, {"category_id": cat2.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
