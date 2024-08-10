from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, Http404
from entrepreneurs.models import Company, Document, Metric
from django.contrib import messages
from django.db.models import F, Q
from django.core.exceptions import ValidationError
from .models import ProposalInvestment
from django.db.models.aggregates import Sum
from utils.supportfuncs import cast


def suggestions(request: HttpRequest):
    """show and filter suggestions of companies to invest"""
    areas = Company.AreaChoices
    if request.method == "GET":   
        return render(request, 'suggestions.html', {'areas': areas})
    
    elif request.method == "POST":
        type_ = request.POST.get('tipo')
        area = request.POST.getlist('area_')
        value = request.POST.get('valor')

        qs = Company.objects
        qs_dict = {
            'C': qs.filter(
                Q(time_of_existence=Company.TimeOfExistenceChoices.GREATEST_5Y)|
                Q(stage=Company.StageChoices.SCALABLE)
            ),
            'I': qs.filter(
                time_of_existence__in=[
                    Company.TimeOfExistenceChoices.GREATEST_6M,
                    Company.TimeOfExistenceChoices.GREATEST_1Y,
                ],
            ).exclude(stage=Company.StageChoices.IDEA),
            'D': qs.exclude(
                Q(time_of_existence=Company.TimeOfExistenceChoices.GREATEST_5Y)|
                Q(stage=Company.StageChoices.SCALABLE)
            ),
        }
        if type_ not in qs_dict.keys():
            messages.error(request, 'Tipo de perfil selecionado é inválido.')
            return redirect('suggestions')
        
        qs = qs_dict[type_]
        print(area)
        qs = qs.filter(area__in=area)
        
        selected_companies = qs.annotate(
            val=100 * F('value') / F('percent_equity'),
            pct=Decimal(value) * 100 / F('val')
        ).filter(pct__gte=1)
        
        return render(request, 'suggestions.html', {'companies': selected_companies, 'areas': areas})


def see_company(request: HttpRequest, pk: int):
    """shows the page of the company with information to the investor"""
    company = get_object_or_404(Company, pk=pk)
    company_summary = ProposalInvestment.get_summary(company)
    sold_pct = company_summary.get('sold_pct')

    limiar = 80 * company.percent_equity / 100
    context = {
        'company': company,
        'docs': Document.objects.filter(company=company),
        'metrics': Metric.objects.filter(company=company),
        'sold_pct': int(sold_pct),
        'concretized': True if sold_pct >= limiar else False,
        'pct_available': company.percent_equity - int(sold_pct)
    }
    return render(request, 'see_company.html', context)


def propose(request: HttpRequest, pk: int):
    """receives an user's proposal and save it in the DB"""
    REDIRECT = redirect(reverse('see_company', args=[pk]))

    company = get_object_or_404(Company, pk=pk)
    value = cast(request.POST.get('valor'), int)
    percent = cast(request.POST.get('percentual'), int)

    if not all((value, percent)):
        messages.error(request, 'Há campos inválidos ou não preenchidos.')
        return REDIRECT
    
    proposal_valuation = value * 100 / percent
    min_available_valuation = float(company.valuation) // 2

    if proposal_valuation < min_available_valuation:
        messages.error(request, f'O valuation mínimo é de {min_available_valuation}. Recebido: {proposal_valuation}')
        return REDIRECT

    tot_pct = ProposalInvestment.objects.filter(
        company=company, status=ProposalInvestment.ProposalStatus.ACCEPTED
    ).aggregate(
        pct_sum=Sum('percent', default=0)
    ).get('pct_sum')

    available_pct = int(company.percent_equity - tot_pct)
    if percent > available_pct:
        messages.warning(
            request, f'Valor de porcentagem disponível para esta empresa é de {available_pct}%'
        )
        return REDIRECT
    
    proposal = ProposalInvestment(
        value=value,
        percent=percent,
        company=company,
        investor=request.user
    )

    try:
        proposal.full_clean()
    except ValidationError as exc:
        messages.error(request, exc.messages[0])
        return REDIRECT

    proposal.save()
    messages.success(request, 'Proposta enviada.')
    return REDIRECT


def contract(request: HttpRequest, pk: int):
    """requests to the user a selfie and document photo to validate
    the contract of the proposal investment
    """
    proposal = get_object_or_404(ProposalInvestment, pk=pk)
    if proposal.status != proposal.ProposalStatus.WAITING:
        raise Http404()
    
    if request.method == 'GET':
        return render(request, 'contract.html', {'proposal': proposal})
    
    elif request.method == "POST":
        selfie = request.FILES.get('selfie')
        rg = request.FILES.get('rg')

        proposal.selfie = selfie
        proposal.rg = rg
        
        # TODO: criar modelo para validar se foto do tg coincide com selfie
        
        proposal.status = proposal.ProposalStatus.SENT
        proposal.save()

        messages.success(request, f'Contrato assinado com sucesso, sua proposta foi enviada a empresa.')
        return redirect(reverse('see_company', args=[proposal.company.pk]))
