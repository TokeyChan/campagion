from importlib import import_module
from main.models import Assignee

class Module:
    def __init__(self, app_name):
        self.app_name = app_name
        module = import_module(app_name)
        self.img_path = module.apps.img_path()
        self.title = module.apps.title
        self.home_view = module.apps.home_view


def create_assignees(campaign_id, post_data):
    departments = [(int(data[0].split('_')[1]), int(data[1])) for data in post_data.items() if 'department' in data[0]]
    for tuple_ in departments:
        try:
            assignee = Assignee.objects.get(campaign_id=campaign_id, department_id=tuple_[0], user_id=tuple_[1])
        except Assignee.DoesNotExist:
            print("DOES NOT EXIST")
            previous = Assignee.objects.filter(campaign_id=campaign_id, department_id=tuple_[0])
            if len(previous) != 0:
                pass #HIER DANN DEN FALL EINGEHEN, DASS DIE PERSON UMBESETZT WIRD
            
            assignee = Assignee(user_id=tuple_[1], campaign_id=campaign_id, department_id=tuple_[0])
            assignee.save()
