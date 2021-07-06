window.addEventListener('load', () => { main() });

function main() {
  var milestones = initialize_milestones();
}

function initialize_milestones() {
  var milestones = Array.from(document.getElementsByClassName("milestone"));
  let milestone_objects = [];
  for (let milestone of milestones) {
    milestone_objects.push(new Milestone(milestone));
  }
  return milestone_objects;
}
