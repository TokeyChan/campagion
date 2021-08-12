from django.core.mail import send_mail
from django.template.loader import get_template


class Mail:
    def __init__(self, subject, sender, recipients):
        self.subject = subject
        self.sender = sender
        self.recipients = recipients

    def render(self, html_source=None, text_source=None, context={}):
        if html_source is not None:
            html_template = get_template(html_source)
            self.html = html_template.render(context=context)
        else:
            self.html = None
        if text_source is not None:
            text_template = get_template(text_source)
            self.text = text_template.render(context=context)
        else:
            self.text = ""
        

    def send(self):
        try:
            send_mail(
                self.subject,
                self.text,
                self.sender,
                self.recipients,
                fail_silently=False,
                html_message=self.html
            )
        except:
            pass


