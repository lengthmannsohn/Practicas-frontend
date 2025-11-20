from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Professional


def home(request):
    professionals = Professional.objects.filter(is_active=True)
    return render(request, 'core/home.html', {
        'professionals': professionals,
    })


def professional_detail(request, pk):
    professional = get_object_or_404(Professional, pk=pk, is_active=True)
    return render(request, 'core/professional_detail.html', {
        'professional': professional,
    })


def pricing(request):
    return render(request, 'core/pricing.html')


def professionals_api(request):
    qs = Professional.objects.filter(is_active=True)
    # filtros básicos (se pueden ampliar)
    plan = request.GET.get('plan')
    if plan in ['free', 'standard', 'premium']:
        qs = qs.filter(plan=plan)

    data = []
    for p in qs:
        data.append({
            'id': p.id,
            'alias': p.alias,
            'lat': p.lat,
            'lng': p.lng,
            'plan': p.plan,
            'price_from': p.price_from,
            'price_to': p.price_to,
            'bio': p.bio[:120] + ('...' if len(p.bio) > 120 else ''),
        })
    return JsonResponse(data, safe=False)
