from django.template.loader import get_template
from django.core.mail import send_mail
from main.mails import Mail

def send_invitation_mail(email):
    m = Mail("Einladung zum Campagion Dashboard", "dashboard@campagion.com", [email])
    m.render('users/mails/invitation_mail.html', context={})
    m.send()
    
    
