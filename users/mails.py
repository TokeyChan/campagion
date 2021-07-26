from django.template.loader import get_template
from django.core.mail import send_mail
from main.mails import Mail

def send_invitation_mail(invitation):
    m = Mail("Einladung zum Campagion Dashboard", "dashboard@meetjudao.at", [invitation.email]) #Eigentlich E-Mail: dashboard@campagion.com
    m.render('users/mails/invitation_mail.html', context={
        'invitor': invitation.invitor,
        'link': invitation.link()
    })
    m.send()
    
    
