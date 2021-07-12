var active_container;

class MilestoneContainer {
  constructor(container, canvas) {
    this.hours = container.dataset.duration;
    this.container = container;
    this.width = this.container.offsetWidth;
    this.height = this.container.offsetHeight;
    this.canvas = canvas;
  }
}
