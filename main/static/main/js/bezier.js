
class Bezier {
  constructor(args) {
    //Notwendige Args: svg
    //Mögliche args: startx, starty, endx, endy, start_element, end_element
    // drawing
    this.path = null;
    this.svg = args.svg;
    if (args.start_element == null) {
      this.startx = args.startx;
      this.starty = args.starty;
    }
    else {
      this.setStartElement(args.start_element);
    }

    if (args.end_element == null) {
      this.endx = args.endx;
      this.endy = args.endy;
    } else {
      this.setEndElement(args.end_element);
    }

    if (args.with_control_points == true) {
        this.control_points = {
          'left': new ControlPoint(this.svg, this.starty, this.endx),
          'right': new ControlPoint(this.svg, this.endy, this.startx)
        };
    }

    this.add_event_listeners();
    this.create();
  }
  //private
  get creation_string() {
    let values = ["M", this.startx, this.starty];
    if (this.control_points != null) {
      Array.prototype.push.apply(values, ["C", this.control_points.left.x, this.control_points.left.y, this.control_points.right.x, this.control_points.right.y]);
    }
    Array.prototype.push.apply(values, [this.endx, this.endy]);
    return values.join(' ');
  }
  setStartElement(element) {
    this.start_element = element;
    let rect = element.getBoundingClientRect();
    let svg_rect = this.svg.getBoundingClientRect();
    this.startx = rect.left + (rect.width / 2) - svg_rect.left;
    this.starty = rect.top + (rect.height/ 2) - svg_rect.top;
    this.add_start_element_listeners();
  }
  setEndElement(element) {
    this.end_element = element;
    let rect = element.getBoundingClientRect();
    let svg_rect = this.svg.getBoundingClientRect();
    this.endx = rect.left + (rect.width / 2) - svg_rect.left;
    this.endy = rect.top + (rect.height/ 2) - svg_rect.top;
    this.add_end_element_listeners();
  }
  add_end_element_listeners() {
    if (this.end_element != null) {
      this.end_element.addEventListener('move', (e) => {
        this.move_end(e.detail.x, e.detail.y);
      });
    }
  }
  add_start_element_listeners() {
    if (this.start_element != null) {
      this.start_element.addEventListener('move', (e) => { //Musst du noch definieren und callen
        this.move_start(e.detail.x, e.detail.y);
      });
    }
  }
  add_event_listeners() {
    if (this.control_points != null) {
      this.control_points.left.circle.addEventListener('move', () => {
        this.draw();
      });
      this.control_points.right.circle.addEventListener('move', () => {
        this.draw();
      });
    }
  }
  create() {
    this.path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    this.path.setAttribute("d", this.creation_string);
    this.path.setAttribute("stroke", "green");
    this.path.setAttribute("stroke-width", "2");
    this.path.setAttribute("fill", "none");
    this.svg.appendChild(this.path);
  }

  //public
  move_start(x, y) {
    let rect = this.svg.getBoundingClientRect();
    this.startx = x - rect.left;
    this.starty = y - rect.top;
    this.draw();
  }
  move_end(x, y) {
    let rect = this.svg.getBoundingClientRect();
    this.endx = x - rect.left;
    this.endy = y - rect.top;
    this.draw();
  }
  draw() {
    this.path.setAttribute("d", this.creation_string);
  }
  drop(x, y) {
    let elements = Array.from(document.elementsFromPoint(x, y))
    let left_dots = elements.filter(t => t.classList.contains("dot") && t.classList.contains("left"));
    if (left_dots.length == 0) {
      throw new Error("could not be dropped");
    }
    let left_dot = left_dots[0];
    this.setEndElement(left_dot);
  }
  delete() {
    this.svg.removeChild(this.path);
    if (this.control_points != null) {
      for (let point of this.control_points) {
        point.delete();
      }
    }
  }
}

var active_control_point;

class ControlPoint {
  constructor(svg, x, y) {
    this.x = x;
    this.y = y;
    this.svg = svg;
    this.circle = this.create_element();
    this.add_event_listeners();

    this.mouse_is_down = false;
  }
  create_element() {
    let circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.classList.add('bezier_control_point');
    circle.setAttribute('cx', this.x);
    circle.setAttribute('cy', this.y);
    circle.setAttribute('r', '10');
    this.svg.appendChild(circle);
    return circle;
  }
  add_event_listeners() {
    this.circle.addEventListener('mousedown', () => {
      this.mouse_is_down = true;
      active_control_point = this;
      document.addEventListener('mousemove', control_point_mousemove);
    });
    this.circle.addEventListener('mouseup', (e) => {
        this.mouse_is_down = false;
        active_control_point = null;
        document.removeEventListener('mousemove', control_point_mousemove);
    });
  }
  move(e) {
    let radius = this.circle.getAttribute('r');
    let rect = this.svg.getBoundingClientRect();
    this.x = e.clientX - (radius / 2) - rect.left;
    this.y = e.clientY - (radius / 2) - rect.top;
    this.circle.setAttribute('cx', this.x);
    this.circle.setAttribute('cy', this.y);

    this.circle.dispatchEvent(new CustomEvent('move'));
    }
  show() {
    this.circle.display = "block";
  }
  hide() {
    this.circle.display = "none";
  }
  delete() {
    this.svg.removeChild(this.circle);
  }
}


function control_point_mousemove(e) {
  active_control_point.move(e);
}
