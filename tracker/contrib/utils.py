import json
from datetime import datetime
from tracker.models import Node, Task, Milestone, Line, Workflow

def handle_node_data(data, owner):
    #if isinstance(data, str):
    data = json.loads(data)
    lines = []
    nodes = {}
    present_tasks = {task.id:task for task in owner.task_set.all()}
    present_lines = owner.get_lines()
    for obj in data['nodes']:
        node = None
        if obj['id'] is not None:
            try:
                node = present_tasks[obj['id']].node
                del present_tasks[obj['id']]
            except KeyError:
                pass
        if node is None:
            node = Node()
            milestone = None
            try:
                milestone = Milestone.objects.get(id=obj['milestone_id'])
            except Milestone.DoesNotExist:
                pass
            t = Task(
                milestone = milestone,
                planned_start_date=datetime.now() #FALSCH ABER EGAL
            )
            if isinstance(owner, Workflow):
                t.workflow = owner
            else:
                t.template = owner
            t.save()
            node.task = t

        node.left = float(obj['left'])
        node.top = float(obj['top'])
        nodes[obj['nr']] = node

        node.save()

    for obj in data['lines']:
        if obj['id'] is not None:
            try:
                line = present_lines[obj['id']];
                del present_lines[obj['id']]
            except KeyError:
                line = Line()
        else:
            line = Line()
        line.from_node = nodes[obj['from']]
        line.to_node = nodes[obj['to']]
        line.save()

    for task in present_tasks.items():
        task[1].delete()
    for line in present_lines.items():
        line[1].delete()
