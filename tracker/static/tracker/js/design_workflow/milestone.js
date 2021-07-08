var active_milestone;
var active_bezier;
class Milestone
{
  constructor(element) {
    this.element = element;

    this.dot_left = Array.from(element.getElementsByClassName("left"))[0];
    this.dot_right = Array.from(element.getElementsByClassName("right"))[0];

    this.in_the_air = false;
    this.mouse_is_down = false;

    this.add_event_listeners();
  }
  get is_linked() {
    return this.element.parentNode.id == "milestone_container";
  }
  get in_node_container() {
    return this.element.parentNode.id == "node_container";
  }


  add_event_listeners() {
    this.element.addEventListener('mousedown', (e) => {
      if (e.pageX < (this.element.offsetLeft + 10) || e.pageX > (this.element.offsetLeft + this.element.offsetWidth - 10))
        return;
      this.mouse_is_down = true;
      active_milestone = this;
      if (this.is_linked)
        this.unlink(e.pageX - (this.element.offsetWidth / 2), e.pageY - (this.element.offsetHeight / 2));
      document.addEventListener('mousemove', milestone_mousemove);
    });
    this.element.addEventListener('mouseup', (e) => {
      if (this.in_the_air)
        this.drop(e);
      this.mouse_is_down = false;
      active_milestone = null;
      document.removeEventListener('mousemove', milestone_mousemove);
    });
    this.dot_right.addEventListener('mousedown', (e) => {
      active_bezier = new Bezier({
        'svg': document.getElementById('svg'),
        'start_element': this.dot_right,
        'endx': e.pageX,
        'endY': e.pageY
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
    this.dot_left.dispatchEvent(new CustomEvent('move', { detail: {'x': left_rect.x + (left_rect.width / 2), 'y': left_rect.y + (left_rect.height / 2)}}));
    this.dot_right.dispatchEvent(new CustomEvent('move', { detail: {'x': right_rect.x + (right_rect.width / 2), 'y': right_rect.y + (right_rect.height / 2)}}));
  }
}

function draw_bezier(e) {
  active_bezier.move_end(e.pageX, e.pageY);
}
function stop_draw_bezier(e) {
  document.removeEventListener('mousemove', draw_bezier);
  document.removeEventListener('mouseup', stop_draw_bezier);
  try {
    active_bezier.drop(e.pageX, e.pageY);
  }
  catch {
    active_bezier.delete();
  }

  active_bezier = null;
}


function milestone_mousemove(e) {
  active_milestone.move(e);
}
