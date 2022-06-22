# from django.db.models import Min,Max
# from products.models import Products,Variation


# def get_filters(request):
#     pass
    # cats=Products.objects.distinct().values('category__title','category__id')
	# # colors=Variation.objects.distinct().values('variation_category__color')
	# # sizes=Variation.objects.distinct().values('size__title','size__id')
	# # minMaxPrice=Products.objects.aggregate(Min('price'),Max('price'))
	# data={
	# 	'cats':cats,
	# 	# 'colors':colors,
	# 	# 'sizes':sizes,
	# 	# 'minMaxPrice':minMaxPrice,
	# }
	# return data