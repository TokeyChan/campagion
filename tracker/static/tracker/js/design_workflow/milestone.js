var active_milestone;
var active_bezier;

class Milestone
{
  constructor(args) {
    //Benötigt: element, nr
    //optional: task
    this.element = args.element;
    this.nr = args.nr;
    this.id = args.task != null ? args.task.id : null;
    this.task = args.task || null;
    this.milestone_id = args.task != null ? args.task.milestone.id : args.element.dataset.milestone_id;
    this.enabled = args.task != null ? args.enabled : true;

    console.log(this.enabled);

    this.dot_left = Array.from(this.element.getElementsByClassName("left"))[0];
    this.dot_right = Array.from(this.element.getElementsByClassName("right"))[0];
    this.dot_bottom = Array.from(this.element.getElementsByClassName("bottom"))[0];

    this.in_the_air = false;
    this.mouse_is_down = false;

    if (this.task != null) {
      this.populate_from_task();
    }

    this.add_event_listeners();
  }
  get is_linked() {
    return this.element.parentNode.id == "milestone_container";
  }
  get in_node_container() {
    try {
      return this.element.parentNode.id == "node_container";
    }
    catch {
      return false;
    }
  }

  static get selected_milestone() {
    let element = Array.from(document.getElementsByClassName('milestone')).filter(t => t.classList.contains('selected'))[0];
    if (element == null)
      return null;
    return milestone_from_nr(element.dataset.nr);
  }
  _enabled = null;
  get enabled() {
    return this._enabled;
  }
  set enabled(value) {
    this._enabled = value;
    if (value) {
      this.element.classList.remove('disabled');
    } else {
      this.element.classList.add('disabled');
    }
  }

  add_event_listeners() {
    this.element.addEventListener('mousedown', (e) => {
      select_milestone(this);
      if (e.pageX < (this.element.offsetLeft + 10) || e.pageX > (this.element.offsetLeft + this.element.offsetWidth - 10) || e.pageY > (this.element.offsetTop + this.element.offsetHeight - 10))
        return;
      console.log(e.pageY < (this.element.offsetTop + this.element.offsetHeight - 10));
      this.mouse_is_down = true;
      active_milestone = this;
      if (this.is_linked) {
        this.unlink(e.pageX - (this.element.offsetWidth / 2), e.pageY - (this.element.offsetHeight / 2));
      }
      document.addEventListener('mousemove', milestone_mousemove);
    });
    this.element.addEventListener('mouseup', (e) => {
      if (this.in_the_air)
        this.drop(e);
      this.mouse_is_down = false;
      active_milestone = null;
      document.removeEventListener('mousemove', milestone_mousemove);
      var elements = Array.from(document.elementsFromPoint(e.clientX, e.clientY));
      let element_ids = elements.map(t => t.id);
      if (element_ids.includes('milestone_container')) {
        this.link_element();
      }
    });
    this.dot_right.addEventListener('mousedown', (e) => {
      active_milestone = this;
      active_bezier = new Bezier({
        'svg': document.getElementById('svg'),
        'start_element': this.dot_right,
        'endx': e.clientX,
        'endY': e.clientY
      });
      document.addEventListener('mousemove', draw_bezier);
      document.addEventListener('mouseup', stop_draw_bezier);
    });
    this.dot_bottom.addEventListener('mousedown', (e) => {
      active_milestone = this;
      active_bezier = new Bezier({
        'svg': document.getElementById('svg'),
        'start_element': this.dot_bottom,
        'endx': e.clientX,
        'endY': e.clientY,
        'fallback': true
      });
      document.addEventListener('mousemove', draw_bezier);
      document.addEventListener('mouseup', stop_draw_bezier);
    });
  }
  link_element() {
    this.element.style.position = "relative";
    this.element.style.left = "0px";
    this.element.style.top = "0px";
    this.element.style.transform = "rotate(0deg)";
    document.getElementById("milestone_container").appendChild(this.element);
  }
  unlink(x, y) {
    this.in_the_air = true;
    this.element.parentNode.removeChild(this.element);
    this.element.style.position = "absolute";
    this.element.style.left = x + "px";
    this.element.style.top = y + "px";
    this.element.style.transform = "rotate(10deg)";
    document.body.appendChild(this.element);
  }
  drop(e) {
    console.log("DROPPED");
    var elements = Array.from(document.elementsFromPoint(e.clientX, e.clientY)).map(t => t.id);
    if (elements.includes("node_container")) {
      this.element.style.transform = "rotate(0deg)";
      this.element.style.position = "absolute";
      this.element.style.left = (e.pageX - (this.element.offsetWidth / 2)) + "px";
      this.element.style.top = (e.pageY - (this.element.offsetHeight / 2)) + "px";
      document.getElementById("node_container").appendChild(this.element);
    } else {
      this.link_element();
    }
    this.in_the_air = false;
  }
  move(e) {
    let x = e.pageX - (this.element.offsetWidth / 2);
    let y = e.pageY - (this.element.offsetHeight / 2);

    active_milestone.element.style.left = x + "px";
    active_milestone.element.style.top = y + "px";

    let left_rect = this.dot_left.getBoundingClientRect();
    let right_rect = this.dot_right.getBoundingClientRect();
    let bottom_rect = this.dot_bottom.getBoundingClientRect();
    this.dot_left.dispatchEvent(new CustomEvent('move', { detail: {'x': left_rect.x + (left_rect.width / 2), 'y': left_rect.y + (left_rect.height / 2)}}));
    this.dot_right.dispatchEvent(new CustomEvent('move', { detail: {'x': right_rect.x + (right_rect.width / 2), 'y': right_rect.y + (right_rect.height / 2)}}));
    this.dot_bottom.dispatchEvent(new CustomEvent('move', { detail: {'x': bottom_rect.x + (bottom_rect.width / 2), 'y': bottom_rect.y + (bottom_rect.height / 2)}}));
  }
  delete() {
    if (!this.enabled) {
      return;
    }
    this.element.parentNode.removeChild(this.element);
    let incoming_lines = beziers_from_element(this.dot_left);
    let outgoing_lines = beziers_from_element(this.dot_right);
    for (let line of incoming_lines) {
      let index = beziers.indexOf(line);
      beziers.splice(index, 1);
      line.delete();
    }
    for (let line of outgoing_lines) {
      let index = beziers.indexOf(line);
      beziers.splice(index, 1);
      line.delete();
    }
    this.link_element();
  }
  populate_from_task() {
    let name = this.element.getElementsByClassName("milestone_name")[0];
    let duration = this.element.getElementsByClassName("milestone_duration")[0];
    let department = this.element.getElementsByClassName("milestone_department")[0];

    name.textContent = this.task.milestone.name;
    duration.textContent = this.task.milestone.is_external ? "Extern" : (this.task.milestone.duration + "h");
    department.textContent = this.task.milestone.department.name;
  }
}

function select_milestone(milestone) {
  let milestone_elements = Array.from(document.getElementsByClassName('milestone'));
  for (let m of milestone_elements) {
    if (m.classList.contains('selected')) {
      m.classList.remove('selected');
    }
  }
  if (milestone != null)
    milestone.element.classList.add('selected');
}



function draw_bezier(e) {
  active_bezier.move_end(e.clientX, e.clientY);
}
function stop_draw_bezier(e) {
  document.removeEventListener('mousemove', draw_bezier);
  document.removeEventListener('mouseup', stop_draw_bezier);
  try {
    active_bezier.drop(e.clientX, e.clientY);
  }
  catch {
    active_bezier.delete();
    active_bezier = null;
    return;
  }
  document.dispatchEvent(new CustomEvent('new_line', { detail: { 'bezier': active_bezier }}));
  active_bezier = null;
}


function milestone_mousemove(e) {
  active_milestone.move(e);
}
