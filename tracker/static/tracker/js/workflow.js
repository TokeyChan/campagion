var workflow_canvas;

function main() {
  workflow_canvas = initialize_canvas();
  initialize_flexboxes(workflow_canvas);
  populate_tasks(workflow_canvas);
  adjust_milestone_containers(workflow_canvas.millis_to_pixel_ratio());
  var milestone_containers = initialize_milestone_containers(workflow_canvas);
  enable_active_task_buttons(milestone_containers, workflow_canvas.millis_to_pixel_ratio());
}

function initialize_canvas() {
  var workflow_container = document.getElementById('workflow_container');

  var workflow_canvas = new Canvas(workflow_container, VALUES.start_date, new Date(2021, 6, 21));
  workflow_canvas.initialize();

  return workflow_canvas;
}
function adjust_milestone_containers(millis) {
  var containers = Array.from(document.getElementsByClassName('milestone_container'));
  adjust_containers(containers, millis);
}
function adjust_containers(containers, millis) {
  for (container of containers) {
    let hours = container.dataset.duration;
    let hours_in_millis = hours * (60000 * 60);

    let width = (millis * hours_in_millis) - 2;
    container.style.width = width + "px";
  }
}
function initialize_milestone_containers(workflow_canvas) {
  var milestone_containers = Array.from(document.getElementsByClassName('milestone_container'));
  var result = [];
  let refnr = 1;
  for (container of milestone_containers) {
    if (container.dataset.task_id == null) {
      container.dataset.refnr = refnr++;
    }
    result.push(new MilestoneContainer(container, workflow_canvas));
  }
  return result;
}
function initialize_flexboxes(workflow_canvas) {
  var upper_workflow = document.getElementById("workflow_flexbox_upper");
  var lower_workflow = document.getElementById("workflow_flexbox_lower");
  let rect = workflow_canvas.timeline_canvas.getBoundingClientRect();

  upper_workflow.style.left = (rect.left + 11) + "px";
  upper_workflow.style.top = (rect.top + 2) + "px";
  upper_workflow.style.width = (rect.width - 22) + "px";
  upper_workflow.style.height = ((rect.height / 2) - 8) + "px";

  lower_workflow.style.left = (rect.left + 11) + "px";
  lower_workflow.style.top = ((rect.top + rect.height / 2) - 4) + "px";
  lower_workflow.style.width = (rect.width - 22) + "px";
  lower_workflow.style.height = ((rect.height / 2) - 7) + "px";
}
function populate_tasks(canvas) {
  for (let task of VALUES.tasks) {
    let container = document.createElement("div");
    container.classList.add("milestone_container");
    container.classList.add("noselect");
    let millis;
    if (task['start_date'] != null) { //wenn es grad aktiv ist, oder schon fertig ist
      if (task['completion_date'] != null) { //wenn es schon fertig ist
        millis = task['completion_date'] - task['start_date'];
      } else if (task['is_external'] == true) {
        millis = new Date().getTime() - task['start_date'];
      } else {
        millis = task['due_date'] - task['start_date'];
      }
    } else {
      millis = task['due_date'] - task['planned_start_date'];
    }
    container.dataset.duration = Math.floor(millis / (60*60000));
    container.dataset.text = task.milestone.name;
    container.dataset.milestone_id = task.milestone.id;
    container.dataset.task_id = task.id;
    container.dataset.moveable = task['start_date'] == null;
    container.dataset.is_external = task['is_external'] == true;
    //
    container.style.backgroundColor = task.milestone.color;
    container.innerHTML = container.dataset.text + "<br>" + (container.dataset.is_external == "true" ? "~" : "") + container.dataset.duration + "h";
    //Jetzt je nachdem richten, auf welcher Planunsschiene es ist:
    document.getElementById("workflow_flexbox_upper").appendChild(container);
    canvas.nodes_upper.push(container);
  }
}
function enable_active_task_buttons(containers, millis) {
  var buttons = document.getElementsByClassName("active_task_button");
  for (let button of buttons) {
    button.addEventListener("click", () => {
      document.getElementById("post_form_action").value = "FINISH_TASK";
      document.getElementById("post_form_task_id").value = button.dataset.task_id;
      document.getElementById("post_form").submit();
    });
  }
}

function on_tasks_changed() {
  var tasks = Array.from(document.getElementById("workflow_flexbox_upper").childNodes).filter(t => t.classList.contains("milestone_container"));
  var array = [];
  for (let task of tasks) {
    array.push({
      'milestone_id': parseInt(task.dataset.milestone_id),
      'task_id': parseInt(task.dataset.task_id) || null,
      'refnr': parseInt(task.dataset.refnr) || null,
      'millis': workflow_canvas.get_millis_from_container(task),
    });
  }
  var data = { 'tasks': JSON.stringify(array) };
  let csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
  send_request("/tracker/js/update_tasks/" + VALUES.workflow.id + "/", "POST", data, on_response, csrf);
}
function delete_task(container) {
  let csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
  send_request("/tracker/js/update_task/" + container.dataset.task_id + "/", "DELETE", null, null, csrf);
}

function on_response(response) {
  var dict = JSON.parse(response);
  for (let new_task of dict['new_tasks']) {
    let container = document.querySelector("[data-refnr='" + new_task['refnr'] + "']");
    container.dataset.task_id = new_task['task_id'];
  }
}


function btn_start_workflow_click() {
  document.getElementById("post_form_action").value = "START_WORKFLOW";
  document.getElementById("post_form").submit();
}

window.addEventListener('load', () => {
  main();
  document.addEventListener('delete_task', (e) => {
    delete_task(e.detail['container']);
  });
});
window.addEventListener('resize', () => {
  //TODO: RESIZE
});
