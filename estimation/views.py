from django.http import JsonResponse
from django.shortcuts import render
from .forms import EstimationForm

def estimation_view(request):
    form = EstimationForm()
    estimated_cost = None
    service_name = None

    if request.method == 'POST':
        form = EstimationForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            area = form.cleaned_data['area']
            estimated_cost = service.cost_per_sqm * area
            service_name = service.name

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'estimated_cost': float(estimated_cost),
                    'service_name': service_name
                })
        elif request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)

    return render(request, 'estimation/estimator.html', {
        'form': form,
        'estimated_cost': estimated_cost,
        'service_name': service_name
    })
