from django.shortcuts import render
from .documents import PostDocument

def search(request):
    query = request.GET.get('q')  # Get the search query from the request
    if query:
        # Perform a full-text search on the title and content fields
        results = PostDocument.search().query("multi_match", query=query, fields=['title', 'content'])
    else:
        results = PostDocument.search().all()  # Return all results if no query
    
    return render(request, 'search.html', {'results': results})