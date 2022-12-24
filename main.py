# Import Search Console wrapper
import searchconsole as sc
import pandas as pd
from datetime import datetime as dt
from calendar import monthrange

# Get the last month, current year, the number of days of last month and
# insert a zero when the month is between 1-9
lastMonth = dt.now().month
lastMonth -= 1

currentYear = dt.now().year

num_days = monthrange(currentYear, lastMonth)[1]


def insert_zero(month):
    if month < 10:
        month = '0' + str(month)
    return month


# Authenticate and stores de webproperties object in a variable
account = sc.authenticate(
    client_config='./credentials/client_secret.json',
    credentials='./credentials/credentials.json')

# webproperties = account.webproperties


def export_nonbrand_keywords(client, web_property, brand_name):

    webproperty = account[web_property]

    # Get data from GSC
    export_gsc = webproperty.query.range(
        f'{currentYear}-04-01', f'{currentYear}-{lastMonth}-{num_days}') \
        .dimension('query', 'page') \
        .filter('query', brand_name, 'notContains') \
        .get()

    # Make it a Data Frame
    export_report = pd.DataFrame(data=export_gsc)

    # Export to *.csv
    export_report.to_csv(
        f'./reports/{currentYear}-{insert_zero(lastMonth)}-{client}.csv',
        index=False)


def export_all_keywords(client, web_property):

    webproperty = account[web_property]

    # Get data from GSC
    export_gsc = webproperty.query.range(
        f'{currentYear}-02-01', f'{currentYear}-{lastMonth}-{num_days}') \
        .dimension('query', 'page').get()

    # Make it a Data Frame
    export_report = pd.DataFrame(data=export_gsc)

    # Export to *.csv
    export_report.to_csv(
        f'./reports/{currentYear}-02-07-{client}.csv',
        index=False)


client = 'Farmashop'
web_property = 'https://tienda.farmashop.com.uy/'
brand_name = 'shop'

# export_nonbrand_keywords(client, web_property, brand_name)

export_all_keywords(client, web_property)
