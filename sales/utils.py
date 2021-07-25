from customers.models import Customer
from profiles.models import Profile

from io import BytesIO

import uuid
import base64
import matplotlib.pyplot as plt
import seaborn as sns


def generate_code():
    code = str(uuid.uuid4()).replace('-', '').upper()[:12]
    return code


def get_salesman_from_id(value):
    salesman = Profile.objects.get(id=value)
    return salesman.user.username


def get_customer_from_id(value):
    customer = Customer.objects.get(id=value)
    return customer


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_key(res_by):
    if res_by == '#1':
        key = 'transaction_id'
    elif res_by == '#2':
        key = 'created'
    return key


def get_chart(charts_type, data, results_by, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10, 4))
    key = get_key(results_by)
    df = data.groupby(key, as_index=False)['total_price'].sum()
    if charts_type == '#1':
        # plt.bar(df[key], df['total_price'])
        sns.barplot(x=key, y='total_price', data=df)
    elif charts_type == '#2':
        plt.pie(data=df, x='total_price', labels=df[key].values)
    elif charts_type == '#3':
        plt.plot(df[key], df['total_price'], 'g--x')
    else:
        print('Invalid Chart type')
    plt.tight_layout()
    chart = get_graph()
    return chart
