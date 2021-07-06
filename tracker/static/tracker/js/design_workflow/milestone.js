var active_milestone;
class Milestone
{
  constructor(element) {
    this.element = element;
    this.add_event_listeners();

    this.dot_left = Array.from(element.getElementsByClassName("left"))[0];
    this.dot_right = Array.from(element.getElementsByClassName("right"))[0];

    this.in_the_air = false;
    this.mouse_is_down = false;
  }
  get is_linked() {
    return this.element.parentNode.id == "milestone_container";
  }
  get in_node_container() {
    return this.element.parentNode.id == "node_container";
  }


  add_event_listeners() {
    this.element.addEventListener('mousedown', (e) => {
      this.mouse_is_down = true;
      active_milestone = this;
      if (this.is_linked)
        this.unlink(e.pageX - (this.element.offsetWidth / 2), e.pageY - (this.element.offsetHeight / 2));
      document.addEventListener('mousemove', mousemove);
    });
    this.element.addEventListener('mouseup', (e) => {
      if (this.in_the_air)
        this.drop(e);
      this.mouse_is_down = false;
      active_milestone = null;
      document.removeEventListener('mousemove', mousemove);
    });
    this.dot_right.addEventListener('mousedown', (e) => {

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
}


function mousemove(e) {
  let element = active_milestone.element;

  let x = e.pageX - (active_milestone.element.offsetWidth / 2);
  let y = e.pageY - (active_milestone.element.offsetHeight / 2);

  active_milestone.element.style.left = x + "px";
  active_milestone.element.style.top = y + "px";
}
