from django.shortcuts import render
from .models import TeamMember

def team_list_view(request):
    firm_leadership = TeamMember.objects.filter(is_active=True, department='Management').order_by('order_weight')
    associates = TeamMember.objects.filter(is_active=True).exclude(department='Management').order_by('order_weight')
    context = {
        'firm_leadership': firm_leadership,
        'associates': associates,
    }
    return render(request, 'team/team_list.html', context)

def team_detail_view(request, pk):
    team_member = TeamMember.objects.get(pk=pk)
    return render(request, 'team/team_detail.html', {'team_member': team_member})
