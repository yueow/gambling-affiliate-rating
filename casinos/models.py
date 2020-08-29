import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

from autoslug import AutoSlugField


# Rating Exceptions 
# User already rated the casino
class UserExists(Exception):
    pass

# Casino was already rated by the ip address
class IpExists(Exception):
    pass


def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Feature(models.Model):
    NEUTRAL = 'NEUTRAL'
    PROS = 'PROS'
    CONS = 'CONS'

    POLE_CHOICES = (
        (NEUTRAL, 'NEUTRAL'),
        (PROS, 'PROS'),
        (CONS, 'CONS'),
    )

    name = models.CharField(max_length=100)
    pole = models.CharField(max_length=20, choices=POLE_CHOICES, default=NEUTRAL)

    def __str__(self):
        return f'{self.pole} - {self.name}'


class CasinoDetail(models.Model):
    ca_license = models.CharField(max_length=100, default="Нет", \
        blank=True, null=True, verbose_name="License")
    ca_license_bool = models.BooleanField(max_length=100, default=False, \
        verbose_name="License")

    # Banned countries
    banned_countries = models.TextField(blank = True,
        verbose_name="Banned players from")

    dol = models.PositiveIntegerField(default=current_year(),
        validators=[MinValueValidator(1984), max_value_current_year],
        verbose_name="Date of launching")

    crypto = models.BooleanField(default=False, verbose_name="Cryptocasino?")
    scam = models.BooleanField(default=False, verbose_name="Scam?")
    script = models.BooleanField(default=False, verbose_name="Script?")

    feature = models.ManyToManyField(Feature, related_name='features')

    # Content
    short_desc = models.TextField(max_length = 1024, blank = True,\
        verbose_name="Short description")
    content = models.TextField(blank = True, verbose_name="Content")

    # Jackpot
    jackpot_bool = models.BooleanField(default=False, verbose_name="Jackpot Y/N")
    jackpot = models.CharField(max_length=20, blank=True, null=True, verbose_name="Jackpot value" )
    jackpot_value = models.SmallIntegerField(blank=True, null=True, verbose_name="Jackpot value in digits($)")

    # Withdrawal
    min_in = models.CharField(max_length=1024, blank=True, verbose_name="Min limit/deposit" )
    min_output = models.CharField(max_length=1024, blank=True, verbose_name="Min Output" )
    max_output = models.CharField(max_length=1024, blank=True, verbose_name="Max Output" )
    
    # Withdrawal docs
    with_docs_bool = models.BooleanField(default=True, verbose_name="Casino wants docs to withdrawal?")
    with_easy = models.CharField(max_length=50, verbose_name="How easy to withdrawal?")
    with_freq = models.CharField(max_length=1024, blank=True, verbose_name="Witdrawal frequency(d,w)" )

    # Cashback
    cashback = models.CharField(max_length=50, blank=True, null=True,\
        verbose_name="Cashback value")
    cashback_bool = models.BooleanField(default=False, verbose_name="Cashback Y/N")

    # Customer support
    support_grade = models.DecimalField (max_digits = 3, decimal_places=1,\
        default=0, verbose_name="Customer support grade")
    support_desc = models.CharField(max_length=1024, verbose_name="Support grade")
    rus_support = models.BooleanField(default=False, verbose_name="Russian support?")

    class Meta:
        abstract = True


class Casino(CasinoDetail):
    title = models.CharField(max_length=100, verbose_name="Name")
    slug = AutoSlugField(populate_from='title')
    image = models.ImageField(upload_to="casino_logos/")
    link = models.URLField(max_length=300, blank=True, verbose_name="Affiliate link")

    def __str__(self):
        return self.title
    
    # Is an instance marked as a 'top casino'
    def is_top(self):
        if TopCasino.objects.filter(casino=self).exists():
            return True
        return False
    
    # Features 
    def get_neutral(self):
        return self.feature.filter(pole=Feature.NEUTRAL)

    def get_pros(self):
        return self.feature.filter(pole=Feature.PROS)

    def get_cons(self):
        return self.feature.filter(pole=Feature.CONS)

    # Rating
    @property
    def get_rates(self):
        return CasinoRating.objects.filter(casino=self)        

    def get_rating_count(self):
        return CasinoRating.objects.filter(casino=self).count()

    def get_avg_main_rate(self):
        return float(CasinoRating.objects.filter(casino=self).aggregate(models.Avg('rate'))['rate__avg'])
    def get_avg_safe_rate(self):
        return float(CasinoRating.objects.filter(casino=self).aggregate(models.Avg('rate_safe'))['rate_safe__avg'])
    def get_avg_faith_rate(self):
        return float(CasinoRating.objects.filter(casino=self).aggregate(models.Avg('rate_faith'))['rate_faith__avg'])
    def get_avg_soft_rate(self):
        return float(CasinoRating.objects.filter(casino=self).aggregate(models.Avg('rate_soft'))['rate_soft__avg'])
    def get_avg_design_rate(self):
        return float(CasinoRating.objects.filter(casino=self).aggregate(models.Avg('rate_design'))['rate_design__avg'])

    # Get payments
    def get_payments(self):
        return self.payment_set.all()
    
    # Get bonuses
    def get_bonuses(self):
        return self.bonus_set.all()
    
    # Get software
    def get_soft(self):
        return self.software_set.all()

    ## Get license
    # def get_license(self):
        # pass

    # Does accept cryptocurrency as a payment gateway
    def does_accept_crypto(self):
        # If it accepts btc - it accepts crypto
        if self.payment_set.filter(name="Bitcoin"):
            return True
        return False


class CasinoRating(models.Model):
    rate = models.DecimalField(max_digits=3, decimal_places=1, default=0,
        verbose_name="Main rate")

    rate_soft = models.DecimalField(max_digits=3, decimal_places=1,
        default=0, verbose_name="Software Rate")
    rate_design = models.DecimalField(max_digits=3, decimal_places=1,
        default=0, verbose_name="Design Rate")
    rate_safe = models.DecimalField(max_digits=3, decimal_places=1,
        default=0, verbose_name="Safe Rate")
    rate_faith = models.DecimalField(max_digits=3, decimal_places=1,
        default=0, verbose_name="Faith Rate")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
        on_delete=models.SET_NULL)

    ip = models.GenericIPAddressField(blank=True, null=True)
    casino = models.ForeignKey(Casino, on_delete=models.CASCADE)

    class Meta:
        # unique_together = [['casino', 'user'], ['casino', 'ip']]
        verbose_name_plural = 'Casino Ratings'

    def __str__(self):
        return f'{self.rate} - {self.casino.title}'

    def save(self, *args, **kwargs):
        # Logged In
        if self.user:
            # Checks if 
            user_ratings = CasinoRating.objects.filter(casino=self.casino).filter(user=self.user)
            if user_ratings.exists():
                raise UserExists('You have already rated this casino')
            else:
                super(CasinoRating, self).save(*args, **kwargs)
        # Anonymous User 
        else:
            ip_ratings = CasinoRating.objects.filter(casino=self.casino).filter(ip=self.ip)
            if ip_ratings.exists():
                raise IpExists('Casino was already rated by this IP')
            else:
                super(CasinoRating, self).save(*args, **kwargs)


class TopCasino(models.Model):
    casino = models.OneToOneField(Casino, on_delete=models.CASCADE)
    sponsored = models.BooleanField(default=False)

    class Meta:
        ordering = ['sponsored', 'casino']

    def __str__(self):
        return f'[S:{self.sponsored}]- {self.casino.title}'    

    @classmethod
    def get_top_casinos(cls, self):
        pass


class Bonus(models.Model):
    two_word_desc = models.CharField(max_length= 300, default="No bonuses")    
    bonus_digit = models.PositiveSmallIntegerField(verbose_name="Bonus value")
    bonus_desc = models.TextField(blank=True, verbose_name="Bonus Description")

    casino = models.ManyToManyField(Casino)

    dep_bool = models.BooleanField(default=True, blank=False)
    dep = models.PositiveSmallIntegerField(blank = False)

    class Meta:
        ordering = ['-bonus_digit']

    def __str__(self):
        return self.two_word_desc


class Payment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='payment_logos/', blank=True, null=True)

    is_crypto = models.BooleanField(default=False, verbose_name="Is it crypto ?")
    casino = models.ManyToManyField(Casino, blank=True, null=True)


class Software(models.Model):
    name = models.CharField(max_length=100, unique=True) 
    description = models.TextField(max_length=1024, blank=True, null=True)
    casino = models.ManyToManyField(Casino, blank=True, null=True)
    icon = models.ImageField(upload_to="software_icons/", blank=True, null=True)


class Game(models.Model):
    name = models.CharField(max_length=100, unique=True) 
    description = models.TextField(max_length=1024, blank=True, null=True)
    casino = models.ManyToManyField(Casino, blank=True, null=True)
    icon = models.ImageField(upload_to="software_icons/", blank=True, null=True)


# class License(models.Model):
#     name = models.CharField(max_length=100, default="Отсутствует", unique=True, blank=False) 
#     description = models.TextField(blank = True, verbose_name="License's description")
#     casino = models.ForeignKey(Casino, on_delete=models.SET_NULL, blank=True, null=True)
#     validation_link = models.URLField(max_length=300, blank=True, verbose_name="Validation Link")
