

# Models 
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

 # Views   
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def my_view(request):
    item_list = Item.objects.all()  # Queryset of items
    paginator = Paginator(item_list, 10)

    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'my_template.html', {'page_obj': page_obj})


from django.views.generic import ListView
from .models import Item

class ItemListView(ListView):
    model = Item
    template_name = 'item_list.html'  # Main template
    context_object_name = 'items'  # The variable to use in templates
    paginate_by = 10  # Number of items per page

    def get(self, request, *args, **kwargs):
        # Check if this is an AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.template_name = 'partial_item_list.html'  # Load the partial template for AJAX

        return super().get(request, *args, **kwargs)