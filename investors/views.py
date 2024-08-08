from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import HttpRequest
from entrepreneurs.models import Company
from django.contrib import messages
from django.db.models import F


def suggestions(request: HttpRequest):
    """show and filter suggestions of companies to invest"""
    areas = Company.AreaChoices
    if request.method == "GET":   
        return render(request, 'suggestions.html', {'areas': areas})
    
    elif request.method == "POST":
        type_ = request.POST.get('tipo')
        area = request.POST.getlist('area')
        value = request.POST.get('valor')

        qs = Company.objects
        qs_dict = {
            'C': qs.filter(
                time_of_existence=Company.TimeOfExistenceChoices.GREATEST_5Y,
                stage=Company.StageChoices.SCALABLE
            ),
            'D': qs.exclude(
                stage=Company.StageChoices.SCALABLE, 
                time_of_existence=Company.TimeOfExistenceChoices.GREATEST_5Y
            ),
        }
        if type_ not in qs_dict.keys():
            messages.error(request, 'Tipo de perfil selecionado é inválido.')
            return redirect('suggestions')
        
        qs = qs_dict[type_]
        qs = qs.filter(area__in=area)
        
        selected_companies = qs.annotate(
            val=100 * F('value') / F('percent_equity'),
            pct=Decimal(value) * 100 / F('val')
        ).filter(pct__gte=1)
        
        return render(request, 'suggestions.html', {'companies': selected_companies, 'areas': areas})
