from django.views.generic import ListView, DetailView
from .models import Product
from cart.forms import CartAddProductForm

class ProductListView(ListView):
    model = Product
    template_name = 'catalogue/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(is_available=True)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalogue/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context
