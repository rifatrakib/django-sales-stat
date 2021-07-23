from customers.models import Customer
from profiles.models import Profile

import uuid


def generate_code():
    code = str(uuid.uuid4()).replace('-', '').upper()[:12]
    return code


def get_salesman_from_id(value):
    salesman = Profile.objects.get(id=value)
    return salesman.user.username


def get_customer_from_id(value):
    customer = Customer.objects.get(id=value)
    return customer
