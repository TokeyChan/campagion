const ONE_DAY_IN_MILLIS = 86400000;
const TODAY_IN_MILLIS = new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate());

class Canvas { //start_date und end_date müssen Date Objekte mit Jahr, Monat und Tag sei
  constructor(container, start_date, end_date) {
    // allgemeines Init
    let date_canvas = container.getElementsByClassName('date_canvas')[0];
    let timeline_canvas = container.getElementsByClassName('timeline_canvas')[0];
    let upper = container.getElementsByClassName('upper_flexbox')[0];
    let lower = container.getElementsByClassName('lower_flexbox')[0];

    date_canvas.width = date_canvas.offsetWidth;
    date_canvas.height = date_canvas.offsetHeight;
    timeline_canvas.height = timeline_canvas.offsetHeight;
    timeline_canvas.width = timeline_canvas.offsetWidth;

    //Klassenattribute
    this.width = date_canvas.width;
    this.date_canvas = date_canvas;
    this.timeline_canvas = timeline_canvas;
    this.upper = upper;
    this.lower = lower;
    this.nodes_upper = [];
    this.nodes_lower = [];
    //Millis
    var difference_in_millis = Math.abs(end_date - start_date);
    this.difference_in_days = Math.round(difference_in_millis / ONE_DAY_IN_MILLIS);
    this.distance = (this.width - 20) / this.difference_in_days;
    this.start_millis = start_date.getTime();
    this.end_millis = end_date.getTime();

    this.timeline_canvas.addEventListener('drop', (e) => {
      let detail = e.detail;
      this.on_drop(detail.container, detail.pageX, detail.position == "UPPER");
    });
  }
  on_drop(container, x, is_upper) {
    let flexbox = (is_upper ? this.upper : this.lower);
    let nodes = (is_upper ? this.nodes_upper : this.nodes_lower);
    let inserted = false;
    let is_included = nodes.includes(container);

    for (let i = 0; i < nodes.length; i++) {
      let node = nodes[i];
      let rect = node.getBoundingClientRect();
      let start = rect.x;
      let end = rect.x + rect.width;

      if (start < x && end > x) {
        if ((start + ((end - start) / 2)) > x) {//wenn es in der ersten Hälfte ist
          flexbox.insertBefore(container, node);
          inserted = true;
        } else if (i != nodes.length - 1) { //nicht die letzte node
          node = nodes[i + 1]
          if (container == node) {
            if (i != nodes.length - 2) {
              node = nodes[i + 2]
            } else {
              continue;
            }
          }
          flexbox.insertBefore(container, node);
          inserted = true;
        }
      }
      if (inserted)
        break;
    }
    if (!inserted)
      flexbox.appendChild(container);

    if (is_included) {
      let index = nodes.indexOf(container);
      nodes.splice(index, 1);
    }
    //let rect = container.getBoundingClientRect();
    nodes.push(container);
    on_tasks_changed()
  }
  initialize() {
    this.create_date_canvas();
    this.create_timeline_canvas();
  }
  create_date_canvas() {
    var ctx = this.date_canvas.getContext("2d");
    var height = this.date_canvas.height;
    //Dates
    var millis = this.start_millis;
    var date;

    //Für den Loop
    var x = 10
    var y = height / 2
    var i = 0;

    ctx.lineWidth = 1;
    let fontsize = this.distance / 4;
    ctx.font = (fontsize > 18 ? "18" : fontsize) + "px Arial";
    ctx.textAlign = "center";
    while (millis <= this.end_millis) {
      ctx.fillStyle = "#63ff78";
      if (TODAY_IN_MILLIS > millis) {
        ctx.fillRect(x, 20, this.distance, height - 20);
      }
      ctx.fillStyle = "#000000";
      let date = new Date(millis);
      y = 40;
      if (millis == this.start_millis || millis == this.end_millis) {
        y = 20;
      } else if (date.getDay() == 1) { //Montag
        y = 30;
      }
      ctx.moveTo(x, y);
      ctx.lineTo(x, height);
      if (millis != this.end_millis)
        ctx.fillText(date.getDate() + ". " + (date.getMonth() + 1) + ".", x + this.distance/2, height - 2);
      x += this.distance;
      millis += ONE_DAY_IN_MILLIS;
    }
    ctx.stroke();
  }
  create_timeline_canvas() {
    var ctx = this.timeline_canvas.getContext("2d");
    var height = this.timeline_canvas.height;
    var width = this.width;

    var millis = this.start_millis;
    var date;

    ctx.beginPath();
    ctx.strokeStyle = "#000000";
    ctx.moveTo(9.5, 0);
    ctx.lineTo(9.5, height - 10);
    ctx.moveTo(9, height - 9.5);
    ctx.lineTo(width - 9, height - 9.5);
    ctx.moveTo(width - 9.5, height - 10);
    ctx.lineTo(width - 9.5, 0);
    ctx.moveTo(10, (height / 2) - 5);
    ctx.lineTo(width - 10, (height / 2) - 5);
    ctx.stroke();
    ctx.closePath();

    var x = 10;
    while (millis <= this.end_millis) {
      date = new Date(millis);
      ctx.beginPath();
      if (date.getDay() == 1) {
        ctx.strokeStyle = "#000000";
      } else {
        ctx.strokeStyle = "#a3a3a3";
      }
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height - 10);

      x += this.distance;
      millis += ONE_DAY_IN_MILLIS;

      ctx.stroke();
      ctx.closePath();
    }
  }
  get_millis_from_container(container) {
    let rect = container.getBoundingClientRect();
    let start_millis = Math.floor(this.get_millis_at_x(rect.x));
    let end_millis = Math.floor(this.get_millis_at_x(rect.x + rect.width));
    return {
      'start': start_millis,
      'end': end_millis
    }
  }
  get_millis_at_x(x) {
    var width = x - 10;
    return this.start_millis + (width / this.millis_to_pixel_ratio());
  }
  get_x_at_millis(millis) {
    millis = millis - this.start_millis
    return (millis * this.millis_to_pixel_ratio());
  }
  millis_to_pixel_ratio() {
    return this.distance / ONE_DAY_IN_MILLIS;
  }
}
