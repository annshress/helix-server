from collections import OrderedDict
import json
import logging
import uuid

import boto3
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _, gettext
from django_enumfield import enum

from apps.contrib.models import MetaInformationAbstractModel, UUIDAbstractModel
from apps.users.roles import ADMIN

from utils.fields import CachedFileField

logger = logging.getLogger(__name__)
User = get_user_model()


class SourcePreview(MetaInformationAbstractModel):
    PREVIEW_FOLDER = 'source/previews'

    url = models.URLField(verbose_name=_('Source URL'))
    token = models.CharField(verbose_name=_('Token'),
                             max_length=64, db_index=True,
                             blank=True, null=True)
    pdf = CachedFileField(verbose_name=_('Rendered Pdf'),
                          blank=True, null=True,
                          upload_to=PREVIEW_FOLDER)
    completed = models.BooleanField(default=False)
    reason = models.TextField(verbose_name=_('Error Reason'),
                              blank=True, null=True)

    @classmethod
    def get_pdf(cls, url: str, instance: 'SourcePreview' = None, **kwargs) -> 'SourcePreview':
        """
        Based on the url, generate a pdf and store it.
        """
        if not instance:
            token = str(uuid.uuid4())
            instance = cls(token=token)
        instance.url = url
        # TODO: remove .pdf in production... this will happen after webhook
        instance.pdf = cls.PREVIEW_FOLDER + '/' + instance.token + '.pdf'

        instance.save()

        payload = dict(
            url=url,
            token=instance.token,
            filename=f'{instance.token}.pdf',
        )
        logger.info(f'Invoking lambda function for preview {url} {instance.token}')
        client = boto3.client('lambda')
        client.invoke(
            FunctionName=settings.LAMBDA_HTML_TO_PDF,
            InvocationType='Event',
            Payload=json.dumps(payload)
        )
        return instance


class Figure(MetaInformationAbstractModel, UUIDAbstractModel, models.Model):
    class QUANTIFIER(enum.Enum):
        MORE_THAN = 0
        LESS_THAN = 1
        EXACT = 2
        APPROXIMATELY = 3

        __labels__ = {
            MORE_THAN: _("More than"),
            LESS_THAN: _("Less than"),
            EXACT: _("Exact"),
            APPROXIMATELY: _("Approximately"),
        }

    class UNIT(enum.Enum):
        PERSON = 0
        HOUSEHOLD = 1

        __labels__ = {
            PERSON: _("Person"),
            HOUSEHOLD: _("Household"),
        }

    class TERM(enum.Enum):
        EVACUATED = 0
        DISPLACED = 1
        DESTROYED_HOUSING = 2
        PARTIALLY_DESTROYED_HOUSING = 3
        UNINHABITABLE_HOUSING = 4
        FORCED_TO_FLEE = 5
        HOMELESS = 6
        IN_RELIEF_CAMP = 7
        SHELTERED = 8
        RELOCATED = 9
        AFFECTED = 10
        RETURNS = 11
        MULTIPLE_OR_OTHER = 12

        __labels__ = {
            EVACUATED: _("Evacuated"),
            DISPLACED: _("Displaced"),
            DESTROYED_HOUSING: _("Destroyed housing"),
            PARTIALLY_DESTROYED_HOUSING: _("Partially destroyed housing"),
            UNINHABITABLE_HOUSING: _("Uninhabitable housing"),
            FORCED_TO_FLEE: _("Forced to flee"),
            HOMELESS: _("Homeless"),
            IN_RELIEF_CAMP: _("In relief camp"),
            SHELTERED: _("Sheltered"),
            RELOCATED: _("Relocated"),
            AFFECTED: _("Affected"),
            RETURNS: _("Returns"),
            MULTIPLE_OR_OTHER: _("Multiple/Other"),
        }

    class TYPE(enum.Enum):
        IDP_STOCK = 0

        __labels__ = {
            IDP_STOCK: _("IDP (Stock)"),
        }

    class ROLE(enum.Enum):
        RECOMMENDED = 0
        PARTIAL_ADDED = 1
        PARTIAL_SUBTRACTED = 2
        TRIANGULATION = 3

        __labels__ = {
            RECOMMENDED: _("Recommended figure"),
            PARTIAL_ADDED: _("Partial figure (Added)"),
            PARTIAL_SUBTRACTED: _("Partial figure (Subtracted)"),
            TRIANGULATION: _("Triangulation"),
        }

    entry = models.ForeignKey('Entry', verbose_name=_('Entry'),
                              related_name='figures', on_delete=models.CASCADE)
    district = models.TextField(verbose_name=_('District(s)'))
    town = models.CharField(verbose_name=_('Town/Village'), max_length=256)
    quantifier = enum.EnumField(enum=QUANTIFIER, verbose_name=_('Quantifier'))
    reported = models.PositiveIntegerField(verbose_name=_('Reported Figures'))
    unit = enum.EnumField(enum=UNIT, verbose_name=_('Unit of Figure'), default=UNIT.PERSON)
    household_size = models.PositiveSmallIntegerField(verbose_name=_('Household Size'),
                                                      default=1)
    total_figures = models.PositiveIntegerField(verbose_name=_('Total Figures'), default=0,
                                                editable=False)
    term = enum.EnumField(enum=TERM, verbose_name=_('Term'), default=TERM.EVACUATED)
    type = enum.EnumField(enum=TYPE, verbose_name=_('Figure Type'), default=TYPE.IDP_STOCK)
    role = enum.EnumField(enum=ROLE, verbose_name=_('Role'), default=ROLE.RECOMMENDED)

    start_date = models.DateField(verbose_name=_('Start Date'))
    include_idu = models.BooleanField(verbose_name=_('Include in IDU'))
    excerpt_idu = models.TextField(verbose_name=_('Excerpt for IDU'),
                                   blank=True, null=True)

    is_disaggregated = models.BooleanField(verbose_name=_('Is disaggregated'),
                                           default=False)
    # disaggregation information
    displacement_urban = models.PositiveIntegerField(verbose_name=_('Displacement/Urban'),
                                        blank=True, null=True)
    displacement_rural = models.PositiveIntegerField(verbose_name=_('Displacement/Rural'),
                                        blank=True, null=True)
    location_camp = models.PositiveIntegerField(verbose_name=_('Location/Camp'),
                                       blank=True, null=True)
    location_non_camp = models.PositiveIntegerField(verbose_name=_('Location/Non-Camp'),
                                           blank=True, null=True)
    sex_male = models.PositiveIntegerField(verbose_name=_('Sex/Male'),
                                       blank=True, null=True)
    sex_female = models.PositiveIntegerField(verbose_name=_('Sex/Female'),
                                         blank=True, null=True)
    age_json = ArrayField(base_field=JSONField(verbose_name=_('Age')),
                          verbose_name=_('Age Disaggregation'),
                          blank=True, null=True)
    strata_json = ArrayField(base_field=JSONField(verbose_name=_('Stratum')),
                             verbose_name=_('Strata Disaggregation'),
                             blank=True, null=True)
    # conflict based disaggregation
    conflict = models.PositiveIntegerField(verbose_name=_('Conflict/Conflict'),
                                           blank=True, null=True)
    conflict_political = models.PositiveIntegerField(verbose_name=_('Conflict/Violence-Political'),
                                                     blank=True, null=True)
    conflict_criminal = models.PositiveIntegerField(verbose_name=_('Conflict/Violence-Criminal'),
                                                    blank=True, null=True)
    conflict_communal = models.PositiveIntegerField(verbose_name=_('Conflict/Violence-Communal'),
                                                    blank=True, null=True)
    conflict_other = models.PositiveIntegerField(verbose_name=_('Other'),
                                                 blank=True, null=True)

    @classmethod
    def can_be_created_by(cls, user: User, entry: 'Entry') -> bool:
        return entry.can_be_updated_by(user)

    def can_be_updated_by(self, user: User) -> bool:
        """
        used to check before deleting as well
        """
        return self.entry.can_be_updated_by(user)

    @staticmethod
    def clean_idu(values: dict, instance=None) -> OrderedDict:
        errors = OrderedDict()
        if values.get('include_idu', getattr(instance, 'include_idu', None)):
            excerpt_idu = values.get('excerpt_idu', getattr(instance, 'excerpt_idu', None))
            if excerpt_idu is None or not excerpt_idu.strip():
                errors['excerpt_idu'] = gettext('This field is required. ')
        return errors

    def save(self, *args, **kwargs):
        self.total_figures = self.reported
        if self.unit == self.UNIT.HOUSEHOLD:
            self.total_figures = self.reported * self.household_size
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantifier.label} {self.reported} {self.term.label}'


class Entry(MetaInformationAbstractModel, models.Model):
    url = models.URLField(verbose_name=_('Source URL'),
                          blank=True, null=True)
    preview = models.OneToOneField('SourcePreview',
                                   related_name='entry', on_delete=models.SET_NULL,
                                   blank=True, null=True,
                                   help_text=_('After the preview has been generated pass its id'
                                               ' along during entry creation, so that during entry update'
                                               ' the preview can be obtained.'))
    document = models.FileField(verbose_name=_('document'), upload_to='entry/documents',
                                blank=True, null=True)
    article_title = models.TextField(verbose_name=_('Article Title'))
    source = models.CharField(verbose_name=_('Source'), max_length=256)
    publisher = models.CharField(verbose_name=_('Publisher'), max_length=256)
    publish_date = models.DateField(verbose_name=_('Published Date'))
    source_methodology = models.TextField(verbose_name=_('Source Methodology'),
                                          blank=True, null=True)
    source_excerpt = models.TextField(verbose_name=_('Excerpt from Source'),
                                      blank=True, null=True)
    source_breakdown = models.TextField(verbose_name=_('Source Breakdown and Reliability'),
                                        blank=True, null=True)
    event = models.ForeignKey('event.Event', verbose_name=_('Event'),
                              related_name='entries', on_delete=models.CASCADE)

    idmc_analysis = models.TextField(verbose_name=_('IDMC Analysis'),
                                     blank=False, null=True)
    methodology = models.TextField(verbose_name=_('Methodology'),
                                   blank=False, null=True)
    # grid TODO:
    tags = ArrayField(base_field=models.CharField(verbose_name=_('Tag'), max_length=32),
                      blank=True, null=True)

    reviewers = models.ManyToManyField('users.User', verbose_name=_('Reviewers'),
                                       blank=True,
                                       related_name='review_entries')

    @property
    def total_figures(self):
        return self.figures.aggregate(total=Sum('total_figures'))['total']

    @staticmethod
    def clean_url_and_document(values: dict, instance=None) -> OrderedDict:
        errors = OrderedDict()
        if instance:
            # we wont allow updates to entry sources
            return errors
        url = values.get('url', getattr(instance, 'url', None))
        document = values.get('document', getattr(instance, 'document', None))
        if not url and not document:
            errors['url'] = gettext('Please fill the URL or upload a document. ')
            errors['document'] = gettext('Please fill the URL or upload a document. ')
        return errors

    def can_be_updated_by(self, user: User) -> bool:
        """
        used to check before deleting as well
        """
        if user.is_superuser \
                or ADMIN in user.groups.values_list('name', flat=True):
            return True
        return self.created_by == user

    def __str__(self):
        return f'Entry {self.article_title}'
