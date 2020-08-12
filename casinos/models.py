from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime
# Create your models here.

def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Casino(models.Model):
    title = models.CharField(max_length=100, verbose_name="Name")
    slug = models.SlugField(max_length=200, unique=True)

    ca_license = models.CharField(max_length=100, default="Нет", \
        blank=True, null=True, verbose_name="License")
    ca_license_bool = models.BooleanField(max_length=100, default=False, \
        verbose_name="License Y/N")

# Banned countries by casino(banned players)
    banned_countries = models.TextField(blank = True, \
        verbose_name="Banned players from ...")

# Date of launching(casino launching)
    dol = models.PositiveIntegerField(default=current_year(),\
        validators=[MinValueValidator(1984), max_value_current_year],\
        verbose_name="Date of launching")
# Casino Logo
    image = models.ImageField(upload_to="casino_logos/", blank=True, verbose_name="Logo")

# Tech markers
    crypto = models.BooleanField(default=False, verbose_name="Cryptocasino?")
    scam = models.BooleanField(default=False, verbose_name="Scam?")
    script = models.BooleanField(default=False, verbose_name="Script?")




# ! IMPORTANT
# Casino link, casino url(clean), casino affilate link
    # clean_link = models.CharField()
    link = models.URLField(max_length=300, blank=True, verbose_name="Casino Link")
# !




# Rating fields
    rate_soft = models.DecimalField (max_digits = 3, decimal_places=1,\
        default=0, verbose_name="Software rate")
    rate_design = models.DecimalField(max_digits = 3, decimal_places=1,\
        default=0, verbose_name="Design rate")
    rate_safe = models.DecimalField(max_digits = 3, decimal_places=1,\
        default=0, verbose_name="Safe rate")
    rate_faith = models.DecimalField(max_digits = 3, decimal_places=1,\
        default=0, verbose_name="Faith rate")

    rate = models.DecimalField(max_digits = 3, decimal_places=1, default=0,\
        verbose_name="Main rate")


# Content
    short_desc = models.TextField(max_length = 1024, blank = True,\
        verbose_name="Short description")
    content = models.TextField(blank = True, verbose_name="Content")


# Pros and Cons fields
    pros_c = models.TextField(blank = True, verbose_name="Pros")
    cons_c = models.TextField(blank = True, verbose_name="Cons")


# Jackpot
    jackpot_bool = models.BooleanField(default=False, verbose_name="Jackpot Y/N")
    jackpot = models.CharField(max_length=20, blank=True, null=True, verbose_name="Jackpot value" )
    jackpot_value = models.SmallIntegerField(blank=True, null=True, verbose_name="Jackpot value in digits($)")
# Withdrawal
    min_in = models.CharField(max_length=1024, blank=True, verbose_name="Min limit/deposit" )
    min_output = models.CharField(max_length=1024, blank=True, verbose_name="Min Output" )
    max_output = models.CharField(max_length=1024, blank=True, verbose_name="Max Output" )
# Documents for withdrawal
    with_docs_bool = models.BooleanField(default=True, verbose_name="Casino wants docs to withdrawal?")
# ! Переделать with_easy через INTEGER CHOISE, with_freq через INTEGER CHOISE
    with_easy = models.CharField(max_length=50, \
        verbose_name="How easy to withdrawal(Легко, Средне, Сложно, Суперсложно)")
# How often withdrawals(day, week)
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
        ordering = ['rate']

    def __str__(self):
        return self.title

    # def best_bonus(self):
    #     best_bonus = self.get_bonuses.order_by('-')[0]

    #     return best_bonus






# Pros and Cons rendering
    def pros_as_list(self):
        return self.pros_c.split("\n")
    def cons_as_list(self):
        return self.cons_c.split("\n")

# Star rendering for casino rating 
# Rating range(for rendering stars)
    def rate_range(self):
        rate_int = int(self.rate)
        rate_list = []
        for i in range(rate_int):
            rate_list.append(i)
        return rate_list

    def rate_safe_range(self):
        rate_int = int(self.rate_safe)
        rate_list = []
        for i in range(rate_int):
            rate_list.append(i)
        return rate_list


    def rate_faith_range(self):
        rate_int = int(self.rate_faith)
        rate_list = []
        for i in range(rate_int):
            rate_list.append(i)
        return rate_list

    def rate_design_range(self):
        rate_int = int(self.rate_design)
        rate_list = []
        for i in range(rate_int):
            rate_list.append(i)
        return rate_list

    def rate_soft_range(self):
        rate_int = int(self.rate_soft)
        rate_list = []
        for i in range(rate_int):
            rate_list.append(i)
        return rate_list


# Get payments
    def get_payments(self):
        return self.payment_set.all()
# Get bonuses
    def get_bonuses(self):
        return self.bonus_set.all()
# Get software
    def get_soft(self):
        return self.software_set.all()








# # Get payments
#     def get_License(self):
#         return self.payment_set.all()




# Check do object accept cryptocurrency payment method
    def acceptCrypto(self):
# If it accepts btc - it accepts crypto
        btc = self.payment_set.filter(name="Bitcoin")
        if btc:
            return True        
        else:
            return False






    # rateCount - is a function for counting the main rate for a casino
    # input_list -is a list instance contains rate_soft,....rate_faith
    #   or a Casino object
    def rateCount(self):
        # if type(input) == type([]):
        #     input_list = input 
        #     # print("Input in a list")
        # else:
        #     input_list = [input.rate_design, input.rate_faith, input.rate_safe, input.rate_soft]
        #     # print("Input in an object, but now it is a list")

        input_list = [self.rate_design, self.rate_faith, self.rate_safe, self.rate_soft]

        sum = 0
        for r in input_list:
            sum += r
        sum = sum/len(input_list)
        if sum <= 0:
            return 0
        if sum >= 10:
            return 10.0
        else: 
            return round(sum, 1)






class Bonus(models.Model):
    two_word_desc = models.CharField(max_length= 300, verbose_name="About the bonus in 2 words", \
        default="Нет бонусов")    
    bonus_digit = models.PositiveSmallIntegerField(verbose_name="Bonus value")
    bonus_desc = models.TextField(blank=True, verbose_name="Bonus description")

    casino = models.ManyToManyField(Casino)

# Депозитный или бездепозитный бонус
    dep_bool = models.BooleanField(default=True, blank=False)
    dep = models.PositiveSmallIntegerField(blank = False)



    class Meta:
        ordering = ['-bonus_digit']

    def __str__(self):
        return self.two_word_desc




class Payment(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False,\
        verbose_name="Payment method name")
    image = models.ImageField(upload_to='payment_logos/', blank = True,\
        verbose_name="Payment method image(PNG)")
    image_wd = models.PositiveSmallIntegerField(default=100, blank = True, null=True,
        verbose_name="Image width(in pixels)")
    image_hg = models.PositiveSmallIntegerField(default=100, blank = True, null=True,\
        verbose_name="Image height(in pixels)")

    is_crypto = models.BooleanField(default=False, verbose_name="Is it cryptocurrency??")
    casino = models.ManyToManyField(Casino, blank=True)


class Software(models.Model):
    name = models.CharField(max_length=100, default="Отсутствует", unique=True, blank=False) 
    description = models.TextField(max_length=1024, blank = True,\
        verbose_name="Game's description")
    casino = models.ManyToManyField(Casino, blank=True)
    icon = models.ImageField(upload_to="software_icons/", blank=True)

class Game(models.Model):
    name = models.CharField(max_length=100, default="Отсутствует", unique=True, blank=False) 
    description = models.TextField(max_length=1024, blank = True,\
        verbose_name="Game's description")
    casino = models.ManyToManyField(Casino, blank=True)
    icon = models.ImageField(upload_to="software_icons/", blank=True)


# class License(models.Model):
#     name = models.CharField(max_length=100, default="Отсутствует", unique=True, blank=False) 
#     description = models.TextField(blank = True, verbose_name="License's description")
#     casino = models.ForeignKey(Casino, on_delete=models.SET_NULL, blank=True, null=True)
#     validation_link = models.URLField(max_length=300, blank=True, verbose_name="Validation Link")
