from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Sale
from .forms import SalesSearchForm
from .utils import get_customer_from_id, get_salesman_from_id

import pandas as pd


def home_view(request):
    df = None
    sales_df = None
    positions_df = None
    merged_df = None
    form = SalesSearchForm(request.POST or None)

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')

        sales_qs = Sale.objects.filter(
            created__date__lte=date_to, created__date__gte=date_from)
        if len(sales_qs) > 0:
            sales_df = pd.DataFrame(sales_qs.values())
            sales_df['customer_id'] = sales_df['customer_id'].apply(
                get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(
                get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(
                lambda x: x.strftime('%Y-%m-%d'))
            sales_df['updated'] = sales_df['updated'].apply(
                lambda x: x.strftime('%Y-%m-%d'))
            sales_df.rename({'customer_id': 'customer',
                            'salesman_id': 'salesman', 'id': 'sales_id'}, axis=1, inplace=True)
            positions_data = []
            for sale in sales_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id(),
                    }
                    positions_data.append(obj)
            positions_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')

            df = merged_df.groupby('transaction_id', as_index=False,)[
                'price'].sum()

            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            df = df.to_html()
            merged_df = merged_df.to_html()
        else:
            print('No data')
    context = {
        'df': df,
        'merged_df': merged_df,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'form': form,
    }
    return render(request, 'sales/home.html', context)


class SalesListView(ListView):
    model = Sale
    template_name = 'sales/main.html'


class SalesDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'
