from django.db import models
from django.utils.crypto import get_random_string
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.utils.timezone import now
from model_utils.models import TimeFramedModel, TimeStampedModel
from toy.models import ToyPage


def _generate_random_code(prefix=None):
    charset = list('abcdefghklmnpqrstuvwxyz23456789')
    rnd = get_random_string(length=5, allowed_chars=charset)
    return rnd


def generate_code(prefix=None):
    while True:
        code = _generate_random_code(prefix=prefix)
        if not Gift.objects.filter(code__iexact=code).exists():
            return code


class Event(TimeStampedModel):
    name = models.CharField('Company name', max_length=255, unique=True)
    start_datetime = models.DateTimeField('Event start date time')
    end_datetime = models.DateTimeField('Event end date time')
    number_of_codes = models.IntegerField('Number of codes')
    description = models.TextField('Comments', blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Gift(TimeStampedModel):
    code = models.CharField(
        verbose_name='Gift code',
        max_length=255, default=generate_code,
        db_index=True,
        validators=[MinLengthValidator(5)]
    )
    toy = models.ForeignKey(
        ToyPage,
        on_delete=models.CASCADE,
        related_name='gift_codes',
    )
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE,
                              related_name='+',
                              null=True,
                              )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             blank=True, null=True,
                             on_delete=models.CASCADE,
                             related_name='gift_codes')
    redeemed = models.PositiveIntegerField(
        verbose_name='Redeemed',
        default=0
    )
    max_usages = models.PositiveIntegerField(
        verbose_name='Max usage',
        default=1
    )
    allow_ignore_quota = models.BooleanField(
        default=False,
        verbose_name="Allow to bypass quota",
        help_text="If activated, a holder of this voucher code can buy tickets, even if there are none left.")
    gifted = models.BooleanField(default=False)

    class Meta:
        unique_together = (("toy", "code"),)
        ordering = ("code",)

    def __str__(self):
        return self.code

    def is_active(self):
        """
        Returns True if a gift has not yet been redeemed, but is still
        within its validity (if valid_until is set).
        """
        if self.redeemed >= self.max_usages:
            return False
        if self.event:
            if self.event.start_datetime and self.event.start_datetime > now():
                return False
            if self.event.end_datetime and self.event.end_datetime < now():
                return False
        return True

    def is_used(self):
        return self.redeemed >= self.max_usages


    # @staticmethod
    # def clean_gift_code(data, event, pk):
    #     if 'code' in data and Voucher.objects.filter(
    #             Q(code__iexact=data['code']) & Q(event=event) & ~Q(pk=pk)).exists():
    #         raise ValidationError(_('A voucher with this code already exists.'))

    # @staticmethod
    # def clean_max_usages(data, redeemed):
    #     if data.get('max_usages', 1) < redeemed:
    #         raise ValidationError(
    #             _('This voucher has already been redeemed %(redeemed)s times. You cannot reduce the maximum number of '
    #               'usages below this number.'),
    #             params={
    #                 'redeemed': redeemed
    #             }
