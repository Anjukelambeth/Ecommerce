
from accounts.models import Account
from category.models import category
import django_filters
from orders.models import Order, OrderProduct

from products.models import Products

class FilterProducts(django_filters.FilterSet):
	class Meta:
		model = Products
		fields = ['product_name', 'category',]

class FilterCategory(django_filters.FilterSet):
	class Meta:
		model = category
		fields = ['category_name',]

class FilterAccount(django_filters.FilterSet):
	class Meta:
		model = Account
		fields = ['first_name', 'user_name', 'email',]

class FilterOrder(django_filters.FilterSet):
	class Meta:
		model = Order
		fields = ['order_number','first_name','last_name','status','is_ordered']