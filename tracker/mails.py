from main.mails import Mail

def send_task_mail(task):
    user = task.assigned_user()
    m = Mail("Neue Aufgabe: " + task.milestone.name, "dashboard@meetjudao.at", [user.email]) #Eigentlich dashboard@campagion.com
    m.render('tracker/mails/task_mail.html', context={
        'task': task,
        'user_': user
    })
    m.send()