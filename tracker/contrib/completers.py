from datetime import datetime
from django.shortcuts import redirect, reverse
from django.http import HttpResponseRedirect

class Completer:
    def __init__(self, request, task, url):
        self.task = task
        self.url = url
        self.request = request

    def complete(self):
        self.task.workflow.complete_task(self.task)
    
class ClickCompleter(Completer):
    def handle(self):
        self.complete()
        return redirect(self.url)

class UploadCompleter(Completer):
    def handle(self):
        return redirect('tracker:upload_file', task_id=self.task.id)
