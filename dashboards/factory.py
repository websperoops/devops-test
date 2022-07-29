from dashboards.models import Integrations_Shopify_Order


class Formatter(object):

    @classmethod
    def formatStructure(cls, start_date, end_date, queryset, chart_type):

        # Query set - Old options: [gateway, financial_status, referring_site]

        data = {'chart_data': []}
        for query in queryset:

            # BEGIN | BUILD A LIST OF ALL UNIQUE VALUES IN THE DB TABLE FOR THE SPECIFIED QUERY FIELD (e.g. for shopify orders table, all unique values for 'gateway')
            valslist = []
            vals = Integrations_Shopify_Order.objects.filter(created_at__gte=start_date,
                                                             created_at__lte=end_date).values(query)
            for val in vals:
                name = str(val[query]).split('.com/')[:1][0]
                if name not in valslist:
                    valslist.append(name)
            # END | BUILD A LIST OF ALL UNIQUE VALUES ...


            # remove duplicates
            valslist = set(valslist)

            # build a chart-data structure for every unique value in the list (i.e. if we want to find, for instance, the aggregate Sum
            # of field 'total_price' for all orders within a specified date range -- > and that, for each unique payment gateway (e.g. 'paypal', 'amazon payments', etc...)
            n=0
            for val in valslist:
                if val != '' and val != None:
                    n = n + 1
                    data['chart_data'].append({
                        'categorizer': val,
                        'chart_type': chart_type,
                        'categorizer_key': n,
                        'dateslist': [],
                        'categories': [],
                        'dataname': query,
                        chart_type: {
                            'totals': {'total_sales': [], 'total_discounts': [], 'avg_sales': [], 'avg_discounts': [],
                                       'total_refund_adj': [], 'avg_refund_adj': [], 'scatter': []},

                            val: {'total_sales': [], 'total_discounts': [], 'avg_sales': [], 'avg_discounts': [],
                                      'total_refund_adj': [], 'avg_refund_adj': [], 'scatter':[]}},

                        query: {
                            val: {
                                'total_sales': [],
                                'total_discounts': [],
                                'total_refund_adj': [],
                                'avg_sales': [],
                                'avg_discounts': [],
                                'avg_refund_adj': [],
                                'scatter':[],
                            }
                        }
                    })


        results = {'resultset': data, 'valslist':valslist}


        return results










