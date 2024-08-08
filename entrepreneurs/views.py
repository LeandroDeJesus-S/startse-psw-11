from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest
from .models import Company, Document, Metric
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib.auth.decorators import login_required


@login_required(login_url='signin')
def signup_company(request: HttpRequest):
    """view with the function of to register a new company"""
    SIGNUP_COMPANY_REDIRECT = redirect('signup_company')
    
    if request.method == 'GET':
        context = {
            'time_of_existence': Company.TimeOfExistenceChoices,
            'area': Company.AreaChoices,
            'stage': Company.StageChoices,
            'target_audience': Company.TargetAudienceChoices
        }
        return render(request, 'signup_company.html', context)

    elif request.method == 'POST':
        name = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        site = request.POST.get('site')
        time_of_existence = request.POST.get('tempo_existencia')
        desc = request.POST.get('descricao')
        final_date_capitation = request.POST.get('data_final')
        percent_equity = request.POST.get('percentual_equity')
        stage = request.POST.get('estagio')
        area = request.POST.get('area')
        target_audience = request.POST.get('publico_alvo')
        value = request.POST.get('valor')
        pitch = request.FILES.get('pitch')
        logo = request.FILES.get('logo')
        print(final_date_capitation)
        try:
            company = Company(
            user=request.user,
            name=name,
            cnpj=cnpj,
            site=site,
            time_of_existence=time_of_existence,
            desc=desc,
            final_date_capitation=final_date_capitation,
            percent_equity=percent_equity,
            stage=stage,
            area=area,
            target_audience=target_audience,
            value=value,
            pitch=pitch,
            logo=logo
            )
            company.full_clean()
            company.save()
        
        except ValidationError as e:
            print('log:', e.error_dict)
            messages.error(request, e.messages[0])
            return SIGNUP_COMPANY_REDIRECT

        except Exception as e:
            print('log:', str(e))
            messages.error(request, 'Erro interno do sistema')
            return SIGNUP_COMPANY_REDIRECT

        messages.success(request, 'Empresa criada com sucesso')
        return SIGNUP_COMPANY_REDIRECT


@login_required(login_url='signin')
def list_companies(request: HttpRequest):
    """list all the companies of the authenticated user"""
    filter_ = request.GET.get('empresa')
    qs = Company.objects.filter(user=request.user)
    if filter_ is not None:
        qs = qs.filter(
            Q(name__icontains=filter_)|
            Q(cnpj=filter_)| 
            Q(desc__icontains=filter_)|
            Q(stage__icontains=filter_)|
            Q(area__icontains=filter_)
        )

    context = {
        'companies': qs
    }
    return render(request, 'list_companies.html', context)


@login_required(login_url='signin')
def company_detail(request: HttpRequest, pk: int):
    """show the details of the company"""
    context = {
        'company': get_object_or_404(Company, pk=pk, user=request.user),
        'docs': Document.objects.filter(company__pk=pk)
    }
    return render(request, 'company_detail.html', context)


def add_doc(request: HttpRequest, pk: int):
    """add a document to the requested company"""
    COMPANY_REDIRECT = redirect(reverse('company_detail', args=[pk]))

    if request.method == 'POST':
        company = get_object_or_404(Company, pk=pk)
        if company.user != request.user:
            raise PermissionDenied
        
        title = request.POST.get('titulo')
        file = request.FILES.get('arquivo')
        
        doc = Document(
            company=company,
            title=title,
            file=file,
        )
        try:
            doc.full_clean()

        except ValidationError as exc:
            print(exc.error_dict)
            messages.error(request, exc.messages[0])
            return COMPANY_REDIRECT
        
        doc.save()
        messages.success(request, 'Documento registrado com sucesso.')
        return COMPANY_REDIRECT


@login_required(login_url='signin')
def del_doc(request: HttpRequest, pk: int):
    """delete an existing document of the company"""
    if request.method == 'POST':
        doc = get_object_or_404(Document, pk=pk)
        if request.user != doc.company.user:
            raise PermissionDenied
        
        doc.delete()
        messages.success(request, f'{doc.title} deletado.')
        return redirect(reverse('company_detail', args=[doc.company.pk]))


@login_required(login_url='signin')
def add_metric(request: HttpRequest, pk: int):
    """add an new metric to the company"""
    COMPANY_REDIRECT = redirect(reverse('company_detail', args=[pk]))
    if request.method != "POST":
        return 
    
    company = get_object_or_404(Company, pk=pk)
    if request.user != company.user:
        raise PermissionDenied
    
    title = request.POST.get('titulo')
    value = request.POST.get('valor')
    
    metric = Metric(
        company=company,
        title=title,
        value=value
    )
    try:
        metric.full_clean()
    except ValidationError as exc:
        messages.error(request, exc.messages[0])
        return COMPANY_REDIRECT
    
    metric.save()
    messages.success(request, "Métrica cadastrada com sucesso")
    return COMPANY_REDIRECT
