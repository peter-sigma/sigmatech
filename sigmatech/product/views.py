from django.shortcuts import render
from .models import Category, Product
from django.db.models import Q
from django.http import JsonResponse

def catalog_view(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    category_id = request.GET.get('category', '')  # Get the selected category ID

    # Get all categories for the dropdown
    categories = Category.objects.all()

    # Filter products based on query and selected category
    products = Product.objects.all()

    # Apply search query if provided
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)  # Matches products under the searched category
        )

    # Apply category filtering if selected
    selected_category = None
    if category_id:
        try:
            selected_category = Category.objects.get(id=category_id)
            products = products.filter(category=selected_category)
        except Category.DoesNotExist:
            selected_category = None

    return render(request, 'product/catalog.html', {
        'categories': categories,
        'products': products,
        'query': query,  # Pass the query to the template for display
        'selected_category': selected_category,  # Pass selected category to the template
    })


def autocomplete(request):
    query = request.GET.get('term', '')  # Get the term being typed
    if query:
        # Search both category and product names
        categories = Category.objects.filter(name__icontains=query).values_list('name', flat=True)
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).values_list('name', flat=True)

        # Combine results and return suggestions
        suggestions = list(categories) + list(products)
        return JsonResponse(suggestions, safe=False)

    return JsonResponse([], safe=False)  # Return empty list if no query
