from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import Subscriber

@require_POST
def subscribe_view(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        if email and '@' in email:
            Subscriber.objects.get_or_create(email=email)
            return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})
        return JsonResponse({'success': False, 'message': 'Invalid email provided.'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)
