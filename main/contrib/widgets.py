from django.forms.widgets import Widget
import datetime

class DatePickerWidget(Widget):
    template_name = "main/widgets/datepicker.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)

    def format_value(self, value):
        if isinstance(value, datetime.date):
            return value.strftime('%d/%m/%Y')