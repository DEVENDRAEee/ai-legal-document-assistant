from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import json


class SearchAPIView(LoginRequiredMixin, View):
    """API endpoint for semantic search."""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            query = data.get('query', '')
            
            if not query:
                return JsonResponse({'error': 'Query is required'}, status=400)
            
            from .services import LegalSearchService
            search_service = LegalSearchService()
            
            # Search both Constitution and IPC
            constitution_results = search_service.search_constitution(query)
            ipc_results = search_service.search_ipc(query)
            
            return JsonResponse({
                'constitution': constitution_results,
                'ipc': ipc_results
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)




