var milestones;
var beziers;
var milestone_nr;

function main() {
  beziers = [];
  document.addEventListener('new_line', (e) => {
    beziers.push(e.detail.bezier);
  });
  milestone_nr = 0;
  milestones = initialize_milestones();
  populate_nodes(NODES);

  document.getElementById('btn_save').addEventListener('click', () => {
    save_nodes();
  });
  document.getElementById('btn_add_task').addEventListener('click', () => {
    add_new_task();
  });
  document.getElementById('node_container').addEventListener('mousedown', (e) => {
    let elements = Array.from(document.elementsFromPoint(e.clientX, e.clientY));
    if (elements.filter(t => t.classList.contains('milestone')).length == 0) {
      select_milestone(null);
    }
  });
  document.addEventListener('keydown', (e) => {
    if (e.keyCode == 8 || e.keyCode == 46) {
      let milestone = Milestone.selected_milestone;
      if (milestone != null) {
        milestone.delete();
      }
      let bezier = Bezier.selected_bezier;
      if (bezier != null) {
        let index = beziers.indexOf(bezier);
        beziers.splice(index, 1);
        bezier.delete();
      }
    }
  });
}

function initialize_milestones() {
  let nr = milestone_nr;
  var milestones = Array.from(document.getElementById("milestone_container").getElementsByClassName("milestone"));
  let milestone_objects = [];
  for (let milestone of milestones) {
    let m = new Milestone({
      'element': milestone,
      'nr': nr
    });
    milestone.dataset.nr = nr;
    nr += 1;
    milestone_objects.push(m);
  }
  milestone_nr = nr;
  return milestone_objects;
}

function milestone_from_dot(dot) {
  let element = dot.parentNode;
  let nr = element.dataset.nr;
  let milestone = milestones.filter(t => t.nr == nr)[0];
  return milestone;
}
function milestone_from_id(id) {
  return milestones.filter(t => t.id != null && t.id == id)[0];
}
function milestone_from_nr(nr) {
  return milestones.filter(t => t.nr == nr)[0];
}
function beziers_from_element(element) {
  return beziers.filter(t => t.start_element == element || t.end_element == element);
}

function populate_nodes(data) {
  for (let task of data.tasks) {
    create_milestone_element(task);
  }
  for (let line of data.lines) {
    create_bezier_line(line);
  }
}
function create_milestone_element(task) {
  let template = document.getElementById("milestone_js_template");
  let node_container = document.getElementById("node_container");
  let element = template.cloneNode(true);
  element.id = "";
  element.style.left = task.node.left + "px";
  element.style.top = task.node.top + "px";
  element.style.position = "absolute";
  element.dataset.nr = milestone_nr;
  node_container.appendChild(element);

  milestones.push(new Milestone({
    'element': element,
    'nr': milestone_nr,
    'task': task
  }));
  milestone_nr += 1;
}
function create_bezier_line(line) {
  let from = milestone_from_id(line.from);
  let to = milestone_from_id(line.to);

  let bezier = new Bezier({
    'svg': document.getElementById("svg"),
    'start_element': line.is_fallback ? from.dot_bottom : from.dot_right,
    'end_element': to.dot_left,
    'id': line.id,
    'fallback': line.is_fallback
  });
  beziers.push(bezier);
}

function save_nodes() {
  data = {'nodes': [], 'lines': []};
  for (let milestone of milestones.filter(t => t.in_node_container)) {
    node = {
      'id': milestone.id, //Datenbank
      'nr': milestone.nr, //Innerhalb des HTML und JS
      'milestone_id': milestone.milestone_id || null,
      'left': milestone.element.style.left.slice(0, -2),
      'top': milestone.element.style.top.slice(0, -2)
    }
    data.nodes.push(node);
  }

  for (let i = 0; i < beziers.length; i++) {
    let line = beziers[i];
    let from = milestone_from_dot(line.start_element).nr;
    let to = milestone_from_dot(line.end_element).nr;
    data.lines.push({
      'id': line.id,
      'from': from,
      'to': to,
      'fallback': line.fallback
      //Hier Control Points hinzufügen
    });
  }
  document.getElementById('form_data_input').value = JSON.stringify(data);
  document.getElementById('data_form').submit();
}

function add_new_task() {
  show_popup();
}
function submit_milestone_form() {
  var form = document.getElementById('new_milestone_form');
  let form_data = new FormData(form);
  send_request(form.action, form.method, form_data, on_post_response, form_data.get("csrfmiddlewaretoken"));
}
function on_post_response(response_text) {
  let table = document.getElementById('new_milestone_table');
  let response = JSON.parse(response_text);
  if (response.html) {
    table.innerHTML = response.html;
  } else {
    let hidden_div = document.getElementById('hidden_div');
    let container = document.getElementById('milestone_container');
    hidden_div.innerHTML += response.milestone;
    let ms = Array.from(hidden_div.childNodes).filter(t => t.classList != null && t.classList.contains('milestone'));
    let element = ms[ms.length - 1];

    let m = new Milestone({
      'element': element,
      'nr': milestone_nr
    });
    element.dataset.nr = milestone_nr;
    milestone_nr += 1;
    milestones.push(m);

    hidden_div.removeChild(element);
    container.appendChild(element);

    hide_popup();
  }
}

window.addEventListener('load', () => { main() });
