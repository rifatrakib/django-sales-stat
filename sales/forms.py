from django import forms


CHART_CHOICES = (
    ('#1', 'Bar Chart'),
    ('#2', 'Pie Chart'),
    ('#3', 'Line Chart'),
)

RESULT_CHOICES = (
    ('#1', 'Transaction ID'),
    ('#2', 'Sales Date'),
)


class SalesSearchForm(forms.Form):
    date_from = forms.DateTimeField(
        widget=forms.DateInput(attrs={'type': 'date', }))
    date_to = forms.DateTimeField(
        widget=forms.DateInput(attrs={'type': 'date', }))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
    results_by = forms.ChoiceField(choices=RESULT_CHOICES)
