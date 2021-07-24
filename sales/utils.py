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


def get_chart(charts_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10, 4))
    if charts_type == '#1':
        # plt.bar(data['transaction_id'], data['price'])
        sns.barplot(x='transaction_id', y='price', data=data)
    elif charts_type == '#2':
        labels = kwargs.get('labels')
        plt.pie(data=data, x='price', labels=labels)
    elif charts_type == '#3':
        plt.plot(data['transaction_id'], data['price'], 'g--x')
    else:
        print('Invalid Chart type')
    plt.tight_layout()
    chart = get_graph()
    return chart
