window.addEventListener('load', () => {
  main();
});
var form;
var input_action;
var input_campaign_id;
var input_client_id;
var input_task_id;
var input_destination;
var new_campaign;

function main()
{
  input_action = document.getElementById('input_action');
  input_campaign_id = document.getElementById('input_campaign_id');
  input_client_id = document.getElementById('input_client_id');
  input_task_id = document.getElementById('input_task_id');
  input_destination = document.getElementById('input_destination');
  new_campaign = document.getElementById("new_icon");
  form = document.getElementById('form');
  
  var campaign_containers = Array.from(document.getElementsByClassName('campaign_container'));
  for (let container of campaign_containers) {
    container.addEventListener('click', () => {
      redirect_to("EDIT_CAMPAIGN", {'campaign_id': container.dataset.campaign_id});
    });
  }
  /*
  var task_containers = Array.from(document.getElementsByClassName('task_container'));
  for (let task of task_containers) {
    task.addEventListener('click', () => {
      if (confirm("Soll diese Aufgabe abgeschlossen werden?")) {
        finish_task(task.dataset.task_id);
      }
    });
  }
  */
  new_campaign.addEventListener('click', () => {
    redirect_to("NEW_CAMPAIGN", {});
  });
}

function redirect_to(destination, args) { //args == dict
  input_action.value = "REDIRECT";
  input_destination.value = destination;

  if ('campaign_id' in args) {
    input_campaign_id.value = args["campaign_id"];
  }

  form.submit();
}

function add_campaign(client_id) {
  input_action.value = "NEW_CAMPAIGN";
  input_client_id.value = client_id;

  form.submit();
}

function finish_task(task_id) {
  input_action.value = "FINISH_TASK";
  input_task_id.value = task_id;

  form.submit();
}
