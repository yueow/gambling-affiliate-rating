from casinos.models import Casino, Bonus, Payment

from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist

from collections import OrderedDict

# Top casinos
# Ordering by main rain (from higher to lower)
def casinoTop():
    result = Casino.objects.order_by('-rate')
    return result

def casinoTopSoft(): 
    result = Casino.objects.order_by('-rate_soft')
    return result
    
def casinoTopSafe():
    result = Casino.objects.order_by('-rate_safe')
    return result

def casinoTopFaith():
    result = Casino.objects.order_by('-rate_faith')
    return result

def casinoTopDesign():
    result = Casino.objects.order_by('-rate_design')
    return result


# New casinos
# Ordering by fresh
def casinoNew():
    result = Casino.objects.order_by('-dol')
    return result

# Returns casinos don't require documents for withdrawal
def casinoNoDocs():
    result = Casino.objects.filter(with_docs_bool=False)
    return result



# Markers
def casinoCrypto():
    result = Casino.objects.filter(crypto=True)
    return result

def casinoScam():
    result = Casino.objects.filter(scam=True)
    return result

def casinoScript():
    result = Casino.objects.filter(script=True)
    return result


#
def casinoOnlyLicense():
    result = Casino.objects.filter(ca_license_bool=True)
    return result

def casinoFastOut():
    query_raw = Q(with_freq__icontains="Каждый день") | Q(with_freq__icontains="день")

    result = Casino.objects.filter(query_raw)
    return result

def casinoAcceptCrypto():
    try:
        btc = Payment.objects.get(name="Bitcoin")
    except ObjectDoesNotExist as err:
        print(err)
        return []

    result = btc.casino.all()
    return result



# Казинычи по самым сочным бонусам
def casinoTopBonuses():
    bonuses = Bonus.objects.order_by("-bonus_digit")
    result = []
    
    for b in bonuses:
        for c in b.casino.all():
            result.append(c)
    result = OrderedDict((x, True) for x in result).keys()
   
    return result

# Казинычи по самомму большому количеству бонусов
def casinoBunchOfBonuses():
    casinos = Casino.objects.annotate(num_bonus=Count('bonus'))
    casinos_ordered = casinos.order_by('-num_bonus')

    return casinos_ordered 


# Казинычи только с бездеопзитными бонусами с сортировкой по количеству от большего к меньшему
def casinoNoDepBonuses():
    no_dep_bonuses = Bonus.objects.filter(dep_bool=False)
    no_dep_bonuses = no_dep_bonuses.order_by('-bonus_digit')

    result = []
    for b in no_dep_bonuses:
        for c in b.casino.all():
            result.append(c)
    result = OrderedDict((x, True) for x in result).keys()
    return result

# Казинычи только с джекпотами, от большего к меньшему
def casinoJackpots():
    cainos_with_jackpot = Casino.objects.filter(jackpot_bool=True)
    result = cainos_with_jackpot.order_by('-jackpot_value')
    return result



FILTERS = {
    "top": casinoTop,
    "top_safe": casinoTopSafe,
    "top_faith": casinoTop,
    "top_soft": casinoTopSoft,
    "top_design": casinoTop,

    "crypto": casinoCrypto,
    "script": casinoScript,
    "scam": casinoScam,


    "new": casinoNew,
    "nodocs": casinoNoDocs,
    "acceptcrypto": casinoAcceptCrypto,
    "onlylicense": casinoOnlyLicense,
    "fastout": casinoFastOut,

    "topbonus": casinoTopBonuses,
    "bonusbunch": casinoBunchOfBonuses,
    "nodep": casinoNoDepBonuses,
    "jackpot": casinoJackpots,

}

