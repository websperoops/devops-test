from __future__ import print_function

from datetime import datetime
from django.utils import timezone
import time


BASE_URL = r"https://openapi.etsy.com/v2/"
st = .05

def getUser(request, user_id):
    avatar_url = BASE_URL + r"users/"+str(user_id)+r"/avatar/src"
    time.sleep(.101)
    avatar = request.get(avatar_url).json()["results"]

    profile_url = BASE_URL + r"users/" + str(user_id) + str("/profile")
    time.sleep(st)
    profile = request.get(profile_url).json()["results"]
    return [profile[0], avatar]

def getUserAddresses(request, user_id):
     user_address_url = BASE_URL + r"users/" + str(user_id) + r"/addresses"
     time.sleep(st)
     user_address = request.get(user_address_url).json()["results"]
     return user_address 

def getShops(request, user_id):
    shops_url = BASE_URL + r"users/" + str(user_id) + r"/shops"
    time.sleep(st)
    shops = request.get(shops_url).json()["results"]
    return shops

def getActiveListings(request, shop_id, offset = 0, limit = 10000000):
    time.sleep(st)
    listing_url = r"{}shops/{}/listings/active?limit={}&offset={}".format(BASE_URL, shop_id, limit, offset)
    listings = request.get(listing_url)
    listings = listings.json()["results"]
    return listings

def getInactiveListings(request, shop_id, offset = 0, limit = 10000000):
    time.sleep(st)
    listing_url = r"{}shops/{}/listings/inactive?limit={}&offset={}".format(BASE_URL, shop_id, limit, offset)
    listings = request.get(listing_url).json()["results"]
    return listings

def getDraftListings(request, shop_id, offset = 0, limit = 10000000):
    time.sleep(st)
    listing_url = r"{}shops/{}/listings/draft?limit={}&offset={}".format(BASE_URL, shop_id, limit, offset)
    listings = request.get(listing_url).json()["results"]
    return listings

def getExpiredListings(request, shop_id, offset = 0, limit = 10000000):
    time.sleep(st)
    listing_url = r"{}shops/{}/listings/expired?limit={}&offset={}".format(BASE_URL, shop_id, limit, offset)
    listings = request.get(listing_url).json()["results"]
    return listings

def getListingImage(request, list_id):
    image_url = BASE_URL + r"listings/"+str(list_id)+r"/images"
    time.sleep(st)
    images = request.get(image_url).json()["results"]
    return images

def getListingImageVariants(request, list_id):
    image_var_url = BASE_URL + r"listings/"+str(list_id)+r"/variation-images"
    time.sleep(st)
    all_image_vars = request.get(image_var_url).json()["results"]
    return all_image_vars

def getListingProducts(request, list_id):
    inven_url = BASE_URL + r"listings/"+str(list_id)+r"/inventory/"
    time.sleep(st)
    inven = request.get(inven_url).json()["results"]
    products = inven.get("products", None)
    return products

def getReceipts(request, shop_id, offset = 0, limit = 10000000):
    receipts_url = r"{}shops/{}/receipts?limit={}&offset={}".format(BASE_URL, shop_id, limit, offset)
    time.sleep(st)
    receipts = request.get(receipts_url).json()["results"]
    return receipts

def getPayments(request, shop_id, receipt_id):
    payments_url = r"{}shops/{}/receipts/{}/payments".format(BASE_URL, shop_id, receipt_id)
    time.sleep(st)
    payments = request.get(payments_url).json()["results"]
    return payments

def getPaymentAdjustments(request, payment_id):
    adjusts_url = r"{}payments/{}/adjustments".format(BASE_URL, payment_id)
    time.sleep(st)
    adjusts = request.get(adjusts_url).json()["results"]
    return adjusts

def getPaymentAdjustmentItems(request, payment_id, payment_adjustment_id):
    adjust_items_url = r"{}payments/{}/adjustments/{}/items".format(BASE_URL, payment_id, payment_adjustment_id)
    time.sleep(st)
    items = request.get(adjust_items_url).json()["results"]
    return items

def getTransactions(request, shop_id, offset = 0, limit = 10000000):
    transactions_url = r"{}shops/{}/transactions?limit={}&offset={}".format(BASE_URL, shop_id, limit, offset)
    time.sleep(st)
    transactions = request.get(transactions_url).json()["results"]
    return transactions

def getFeedback(request, user_id):
    feedback_url =r"{}users/{}/feedback/from-buyers".format(BASE_URL, user_id)
    time.sleep(st)
    feedback = request.get(feedback_url).json()["results"]
    return feedback

def getLedger(request, shop_id):
    ledger_url = r"{}shops/{}/ledger".format(BASE_URL, shop_id)
    time.sleep(st)
    ledger = request.get(ledger_url).json()["results"]
    return ledger

def getLedgerEntries(request, shop_id, offset = 0, limit = 10000000):
    adjust_items_url = r"{}shops/{}/ledger/entries?limit={}&offset={}".format(BASE_URL, shop_id, limit, offset)
    time.sleep(st)
    items = request.get(adjust_items_url).json()["results"]
    return items

def unix2UTC(ts):
    if ts is None or ts == 0:
        return None
    else:
        time_obj = timezone.make_aware(datetime.fromtimestamp(ts))
        return time_obj

def etsyBool(tf):
    if tf == 'true':
        return True
    elif tf == 'false':
        return False
    elif tf == 0:
        return False
    else:
        return tf 

def etsyDollars(val):
    if val == 0:
        return '0.00'
    elif val is None:
        return None
    else:
        return val/100