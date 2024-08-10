from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from entrepreneurs.models import Company
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from utils.investors.model_messages import ProposalInvestmentMessages
from django.db.models.aggregates import Sum


class ProposalInvestment(models.Model):
    class ProposalStatus(models.TextChoices):
        WAITING = 'AS', _('Aguardando assinatura')
        SENT = 'PE', _('Proposta enviada')
        ACCEPTED = 'PA', _('Proposta aceita')
        REFUSED = 'PR', _('Proposta recusada')
    
    value = models.DecimalField(
        'Valor',
        max_digits=9,
        decimal_places=2,
        blank=False,
        validators=[
            MinValueValidator(1, ProposalInvestmentMessages.INVALID_MIN_VALUE)
        ]
    )
    percent = models.FloatField(
        'Porcentagem',
        blank=False,
        validators=[
            MinValueValidator(1, ProposalInvestmentMessages.INVALID_MIN_PERCENT)
        ]
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.DO_NOTHING,
        verbose_name='Empresa',
    )
    investor = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name='Investidor',
    )
    status = models.CharField(
        max_length=2,
        choices=ProposalStatus.choices,
        blank=False,
        default=ProposalStatus.WAITING
    )
    selfie = models.FileField(upload_to="selfie", null=True, blank=True)
    rg = models.FileField(upload_to="rg", null=True, blank=True)

    def __str__(self):
        return str(self.value)
    
    @property
    def valuation(self):
        return 100 * float(self.value) / self.percent
    
    @staticmethod
    def get_summary(company: Company) -> dict[str, float|Decimal]:
        """returns the percent sold of the company and the total amount

        Args:
            company (Company): the target model

        Returns:
            dict: the aggregated dict result with sold_pct and amount keys
        """
        summary = ProposalInvestment.objects.filter(
            status=ProposalInvestment.ProposalStatus.ACCEPTED,
            company=company
        ).aggregate(
            sold_pct=Sum('percent', default=1e-10),
            amount=Sum('value', defualt=1e-10)
        )
        return summary

    class Meta:
        verbose_name = 'Proposta de investimento'
        verbose_name_plural = 'Propostas de investimentos'