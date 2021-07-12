var workflow_canvas;

function main() {
  workflow_canvas = initialize_canvas();
  populate_tasks(workflow_canvas);
  adjust_task_containers(workflow_canvas.millis_to_pixel_ratio());
  enable_active_task_buttons();
}

function initialize_canvas() {

  var workflow_container = document.getElementById('workflow_container');

  var workflow_canvas = new Canvas(workflow_container, VALUES.start_date, VALUES.end_date, VALUES.departments);
  workflow_canvas.initialize();

  return workflow_canvas;
}
function adjust_task_containers(millis) {
  var containers = Array.from(document.getElementsByClassName('task_container'));
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
function populate_tasks(canvas) {
  for (let task of VALUES.tasks) {
    let container = document.createElement("div");
    container.classList.add("task_container");
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
    container.dataset.department = task.milestone.department.id;
    container.dataset.duration = Math.floor(millis / (60 * 60000));
    //style
    container.style.backgroundColor = task.milestone.color;
    container.style.left = canvas.get_x_at_millis(task['planned_start_date']) + "px";
    //
    container.innerHTML = task.milestone.name + "<br>" + (container.dataset.is_external == "true" ? "~" : "") + container.dataset.duration + "h";
    //Jetzt je nachdem richten, auf welcher Planunsschiene es ist:
    canvas.add_task(container);
  }
}
function enable_active_task_buttons() {
  var buttons = document.getElementsByClassName("active_task_button");
  for (let button of buttons) {
    button.addEventListener("click", () => {
      document.getElementById("post_form_action").value = "FINISH_TASK";
      document.getElementById("post_form_task_id").value = button.dataset.task_id;
      document.getElementById("post_form").submit();
    });
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

function open_design() {
  document.getElementById("post_form_action").value = "OPEN_DESIGN";
  document.getElementById("post_form").submit();
}
function open_template() {
  document.getElementById("post_form_action").value = "CHOOSE_TEMPLATE";
  document.getElementById("post_form").submit();
}
