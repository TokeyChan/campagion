var active_container;

class MilestoneContainer {
  constructor(container, canvas) {
    this.hours = container.dataset.duration;
    this.container = container;
    this.width = this.container.offsetWidth;
    this.height = this.container.offsetHeight;
    this.subscribe_to_events();
    this.mouse_is_down = false;
    this.resizing = false;
    this.resize_allowed = container.dataset.task_id != null;
    this.resize_right_possible = false;
    this.canvas = canvas;
    this.moving_allowed = container.dataset.moveable == "true";
  }
  subscribe_to_events() {
    this.container.addEventListener('mousedown', (e) => {
      if (this.resize_allowed && this.resize_right_possible) {
        this.resizing = true;
        active_container = this;
        document.addEventListener('mousemove', resize);
        document.addEventListener('mouseup', stop_resizing);
      } else if (this.moving_allowed) { //GRAB
        this.mouse_is_down = true;
        active_container = this;
        this.unlink_container(e.pageX - (this.container.offsetWidth / 2), e.pageY - (this.height / 2));
        document.addEventListener('mousemove', mousemove);
      }
    });

    this.container.addEventListener('mouseup', (e) => {
      if (this.resizing || !this.moving_allowed)
        return
      this.drop(e)
      this.mouse_is_down = false;
      active_container = this;
      document.removeEventListener('mousemove', mousemove);
    });

    this.container.addEventListener('mousemove', (e) => {
      if (!this.resize_allowed)
        return;
      if (this.resizing)
        return
      let delta = 7.5;
      let rect = this.container.getBoundingClientRect();
      let x = e.clientX - rect.left;

      if (x > rect.width - delta) {
        this.resize_right_possible = true;
      } else {
        this.resize_right_possible = false;
      }

      if (this.resize_right_possible) {
        this.container.style.cursor = "col-resize";
      } else {
        this.container.style.cursor = "grab";
        this.resize_right_possible = false;
      }
    });
  }
  unlink_container(x, y) {
    this.container.parentNode.removeChild(this.container);
    this.container.style.position = "absolute";
    this.container.style.left = x + "px";
    this.container.style.top = y + "px";
    this.container.style.transform = "rotate(10deg)";
    document.body.appendChild(this.container);
  }
  link_container() {
    this.container.style.position = "relative";
    this.container.style.left = "0px";
    this.container.style.top = "0px";
    this.container.style.transform = "rotate(0deg)";
    document.getElementById("milestone_container").appendChild(this.container);
  }
  drop(e) {
    var elements = Array.from(document.elementsFromPoint(e.clientX, e.clientY)).map(t => t.id).filter(t => t);
    if (elements.includes("workflow_canvas")) {
      this.container.style.transform = "rotate(0deg)";
      this.container.style.position = "relative";
      this.container.style.left = "0px";
      this.container.style.top = "0px";
      document.getElementById("workflow_canvas").dispatchEvent(new CustomEvent('drop',  {
        detail: {
          'container': this.container,
          'pageX': e.pageX,
          'pageY': e.pageY,
          'position': elements.includes("workflow_flexbox_upper") ? "UPPER" : "LOWER"
        }
      }));
      this.resize_allowed = true;
    } else {
      document.dispatchEvent(new CustomEvent('delete_task', { detail: {'container': this.container}}))
      this.resize_allowed = true; //false
      this.link_container();
    }
  }
  on_resize(width) {
    let millis_to_pixel_ratio = this.canvas.millis_to_pixel_ratio();
    let std = Math.floor((width / millis_to_pixel_ratio) / (60000 * 60));
    this.setHours(std);
  }
  setHours(hours) {
    this.hours = hours;
    this.container.dataset.duration = hours;
    this.container.innerHTML = this.container.dataset.text + "<br>" + hours + "h";
  }
}
function mousemove(e) {
  move_container(active_container.container, e.pageX - (active_container.container.offsetWidth / 2), e.pageY - (active_container.height / 2));
}
function move_container(container, x, y) {
  container.style.left = x + "px";
  container.style.top = y + "px";
}
function resize(e) {
  let container = active_container.container;
  let rect = container.getBoundingClientRect();
  container.style.width = e.clientX - rect.x + "px";
  active_container.on_resize(container.offsetWidth);
}
function stop_resizing(e) {
  active_container.resizing = false;
  document.removeEventListener('mouseup', stop_resizing);
  document.removeEventListener('mousemove', resize);
  on_tasks_changed()
}
