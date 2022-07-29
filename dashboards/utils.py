def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def to_dollar(rounded_value):
    """
    Convert all currency fields to USD.

    Get current exchange rate, convert.
    """

    return rounded_value


def round_value(value):
    """
    Round the given value to 1 decimal place.

    If the value is 0 or None, then simply return 0.
    """
    if value:
        return round(float(value), 1)
    else:
        return 0


def percent(part, whole):
    """
    Get the percentage of the given values.

    If the the total/whole is 0 or none, then simply return 0.
    """
    if whole:
        return round_value(100 * float(part)/float(whole))
    else:
        return 0



def display_currency_setting(user, rounded_value):
    """
    Return the currency value based on the unit setting.

    currency values are stored in $ USD in the database. If a user's setting
    is set to EURO, convert the value.
    """
    from accounts.models import UserSettings
    set_currency = UserSettings.objects.filter(user=user).only('currency_unit')
    if set_currency == '$' or set_currency == 'USD':
        return to_dollar(rounded_value)
    else:
        return rounded_value