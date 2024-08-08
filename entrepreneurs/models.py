import os
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    MinLengthValidator,
    MinValueValidator,
    validate_image_file_extension,
)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.safestring import mark_safe
from utils.entrepreneurs.model_messages import CompanyMessages, DocumentMessages


def now_date():
    return timezone.now().date()


class Company(models.Model):
    class TimeOfExistenceChoices(models.TextChoices):
        """time of existence of the company"""
        LESS_6M = '-6', _('Menos de 6 meses')
        GREATEST_6M = '+6', _('Mais de 6 meses')
        LESS_1Y = '+1', _('Mais de 1 ano')
        GREATEST_5Y = '+5', _('Mais de 5 anos')
    
    class StageChoices(models.TextChoices):
        """the atual stage of the company"""
        IDEA = 'I', _('Tenho apenas uma idea')
        MVP = 'MVP', _('Possuo um MVP')
        MVPP = 'MVPP', _('Possuo um MVP com clientes pagantes')
        SCALABLE = 'E', _('Empresa pronta para escalar')
    
    class AreaChoices(models.TextChoices):
        """the area of actuation of the company"""
        ED_TECH = 'ED', _('Ed-tech')
        FIN_TECH = 'FT', _('Fintech')
        AGRO_TECH = 'AT', _('Agrotech')
    
    class TargetAudienceChoices(models.TextChoices):
        """the target audience which the company has interest"""
        B2B = 'B2B'
        B2C = 'B2C'

    user = models.ForeignKey(
        User, 
        on_delete=models.DO_NOTHING, 
        verbose_name='Usuário',
        null=False,
        blank=False,
        error_messages={
            'blank': CompanyMessages.EMPTY_NAME,
            'null': CompanyMessages.EMPTY_NAME,
            'invalid': CompanyMessages.INVALID_USER
        }
    )
    name = models.CharField(
        'Nome', 
        max_length=50,
        null=False,
        blank=False,
        unique=True,
        error_messages={
            'null': CompanyMessages.EMPTY_NAME,
            'blank': CompanyMessages.EMPTY_NAME,
            'invalid': CompanyMessages.INVALID_NAME,
            'unique': CompanyMessages.DUPLICATED_NAME
        }
    )
    cnpj = models.CharField(
        'CNPJ',
        max_length=30,
        null=False,
        blank=False,
        unique=True,
        error_messages={
            'unique': CompanyMessages.DUPLICATED_CNPJ,
            'null': CompanyMessages.EMPTY_CNPJ,
            'blank': CompanyMessages.EMPTY_CNPJ,
            'invalid': CompanyMessages.INVALID_CNPJ
        }
    )
    site = models.URLField(
        'Site',
        unique=True,
        blank=False,
        null=False,
        error_messages={
            'unique': CompanyMessages.DUPLICATED_SITE,
            'invalid': CompanyMessages.INVALID_SITE,
            'blank': CompanyMessages.EMPTY_SITE,
            'null': CompanyMessages.EMPTY_SITE,
        }
    )
    time_of_existence = models.CharField(
        'Tempo de existência',
        max_length=2,
        choices=TimeOfExistenceChoices.choices,
        default=TimeOfExistenceChoices.LESS_6M,
        null=False,
        blank=False,
        error_messages={
            'invalid': CompanyMessages.INVALID_TIME_OF_EXISTENCE,
            'null': CompanyMessages.EMPTY_TIME_OF_EXISTENCE,
            'blank': CompanyMessages.EMPTY_TIME_OF_EXISTENCE,
        }
    )
    desc = models.TextField(
        'Descrição',
        error_messages={
            'null': CompanyMessages.EMPTY_DESC,
            'blank': CompanyMessages.EMPTY_DESC,
        }
    )
    final_date_capitation = models.DateField(
        'Data final de capitação',
        null=False,
        blank=False,
        validators=[
            MinValueValidator(now_date, CompanyMessages.INVALID_FINAL_DATE_CAPITATION)
        ],
        error_messages={
            'invalid': CompanyMessages.INVALID_FINAL_DATE_CAPITATION,
            'blank': CompanyMessages.EMPTY_FINAL_DATE_CAPITATION,
        }
    )
    percent_equity = models.IntegerField(
        'Percentual Equity',
        null=False,
        blank=False,
        error_messages={
            'invalid': CompanyMessages.INVALID_PERCENT_EQUITY,
            'null': CompanyMessages.EMPTY_PERCENT_EQUITY,
            'blank': CompanyMessages.EMPTY_PERCENT_EQUITY,
        }
    )
    stage = models.CharField(
        'Estagio',
        max_length=4,
        choices=StageChoices.choices,
        default=StageChoices.IDEA,
        null=False,
        blank=False,
        error_messages={
            'invalid': CompanyMessages.INVALID_STAGE,
            'null': CompanyMessages.EMPTY_STAGE,
            'blank': CompanyMessages.EMPTY_STAGE,
        }
    )
    area = models.CharField(
        max_length=3,
        choices=AreaChoices.choices,
        default=AreaChoices.AGRO_TECH,
        null=False,
        blank=False,
        error_messages={
            'invalid': CompanyMessages.INVALID_AREA,
            'blank': CompanyMessages.EMPTY_AREA,
            'null': CompanyMessages.EMPTY_AREA,
        }
    )
    target_audience = models.CharField(
        'Publico alvo',
        max_length=3,
        choices=TargetAudienceChoices.choices,
        default=TargetAudienceChoices.B2B,
        null=False,
        blank=False,
        error_messages={
            'invalid': CompanyMessages.INVALID_TARGET_AUDIENCE,
            'null': CompanyMessages.EMPTY_TARGET_AUDIENCE,
            'blank': CompanyMessages.EMPTY_TARGET_AUDIENCE,
        }
    )
    value = models.DecimalField(
        'Valor de capitação',
        max_digits=9,
        decimal_places=2,
        null=False,
        blank=False,
        validators=[
            MinValueValidator(0, CompanyMessages.INVALID_VALUE)
        ],
        error_messages={
            'invalid': CompanyMessages.INVALID_VALUE,
            'blank': CompanyMessages.EMPTY_VALUE,
            'null': CompanyMessages.EMPTY_VALUE,
        }
    )
    pitch = models.FileField(
        upload_to='pitchs',
        validators=[
            FileExtensionValidator(['wav', 'mp4'])
        ],
        null=True,
        blank=True
    )
    logo = models.FileField(
        upload_to='logos',
        null=False,
        blank=False,
        validators=[
            validate_image_file_extension
        ],
        error_messages={
            'null': CompanyMessages.EMPTY_LOGO,
            'blank': CompanyMessages.EMPTY_LOGO,
        }
    )

    def  __str__(self):
        return f'{self.user.username} | {self.name}'
    
    def clean(self) -> None:
        super().clean()
        self.error_messages = {}
        PITCH_MAX_MB = 50
        LOGO_MAX_MB = 5
        if not self._validate_cnpj(self.cnpj):
            raise ValidationError({'cnpj': CompanyMessages.INVALID_CNPJ})
        
        elif self.pitch and self._validate_file_size(self.pitch, max_MB=PITCH_MAX_MB):
            msg = CompanyMessages.INVALID_FILE_SIZE.format_map({'field': 'pitch', 'size': f'{PITCH_MAX_MB}MB'})
            raise ValidationError({'pitch': msg})
        
        elif self.logo and self._validate_file_size(self.logo, max_MB=LOGO_MAX_MB):
            msg = CompanyMessages.INVALID_FILE_SIZE.format_map({'field': 'logo', 'size': f'{LOGO_MAX_MB}MB'})
            raise ValidationError({'logo': msg})
    
    @staticmethod
    def _validate_cnpj(cnpj: str) -> bool:
        """the function to validate if the CNPJ of the company is valid

        Args:
            cnpj (str): the company CNPJ to validate

        Returns:
            bool: True if the given CNPJ is valid
        
        Examples:
        >>> Company._validate_cnpj('24.040.568/0001-02)
        >>> True
        >>> Company._validate_cnpj('24040568000102)
        >>> True
        >>> Company._validate_cnpj('11111111111111')
        >>> False
        """
        cnpj = ''.join(filter(str.isdigit, cnpj))

        if len(cnpj) != 14:
            return False

        if cnpj in (c * 14 for c in "1234567890"):
            return False

        def calc_digito(cnpj, digit):
            if digit == 1:
                weight = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            elif digit == 2:
                weight = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

            sum_ = sum(int(cnpj[i]) * weight[i] for i in range(len(weight)))
            rest = sum_ % 11
            return 0 if rest < 2 else 11 - rest

        if calc_digito(cnpj[:12], 1) != int(cnpj[12]):
            return False
        if calc_digito(cnpj[:13], 2) != int(cnpj[13]):
            return False

        return True

    @staticmethod
    def _validate_file_size(file_field, max_MB=50):
        """validate the file size with considering the MB unit
        Args:
            image (Any): the file field with support to property `size`.
            max_MB (int, Optional): the max size in MB that the file can have. Defaults to 50MB
        
        Returns:
            bool: True if the file size is less or equal than `max_MB` else False

        Example:
        >>> my_company = Company.objects.first()
        >>> my_company.pitch.size 
        >>> 10240  # 10MB
        >>> Company._validate_image_size(my_company.pitch, max_MB=10)
        >>> True
        """
        max_ = max_MB * 1024
        return False if file_field.size > max_ else True

    @property
    def status(self) -> str:
        if timezone.now().date() > self.final_date_capitation:
            return mark_safe('<span class="badge bg-success">Finalizada</span>')
        return mark_safe('<span class="badge bg-primary">Disponível</span>')

    @property
    def valuation(self):
        val = f'{100 * self.value / self.percent_equity:.2f}'
        return val

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'


class Document(models.Model):
    company = models.ForeignKey(
        Company, 
        on_delete=models.DO_NOTHING,
        verbose_name='Empresa',
        blank=False,
        error_messages={
            'invalid': DocumentMessages.INVALID_COMPANY,
            'blank': DocumentMessages.EMPTY_COMPANY,
            'null': DocumentMessages.EMPTY_COMPANY,
        }
    )
    title = models.CharField(
        'Título', 
        max_length=30,
        blank=False,
        validators=[
            MinLengthValidator(
                2, DocumentMessages.MIN_TITLE_LENGTH.format_map({'len': 2})
            ),
        ],
        error_messages={
            'invalid': DocumentMessages.INVALID_TITLE,
            'blank': DocumentMessages.EMPTY_TITLE,
            'null': DocumentMessages.EMPTY_TITLE,
        }
    )
    file = models.FileField(
        'Arquivo',
        upload_to='documents',
        blank=False,
        unique=True,
        validators=[
            FileExtensionValidator(['pdf']),
        ],
        error_messages={
            'invalid': DocumentMessages.INVALID_FILE,
            'blank': DocumentMessages.EMPTY_FILE,
            'null': DocumentMessages.EMPTY_FILE,
        }
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'title'],
                name='company_title_unique_constraint',
                violation_error_message=DocumentMessages.DOCUMENT_ALREADY_EXISTS
            ),
            models.UniqueConstraint(
                fields=['company', 'file'],
                name='company_file_unique_constraint',
                violation_error_message=DocumentMessages.DOCUMENT_ALREADY_EXISTS
            ),
        ]


class Metric(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=30)
    value = models.FloatField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Métrica'
        verbose_name_plural = 'Métricas'
