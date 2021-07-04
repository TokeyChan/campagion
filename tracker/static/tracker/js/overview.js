window.addEventListener('load', () => {
  main();
});
var form;
var input_action;
var input_campaign_id;
var input_client_id;
var input_destination;

function main()
{
  input_action = document.getElementById('input_action');
  input_campaign_id = document.getElementById('input_campaign_id');
  input_client_id = document.getElementById('input_client_id');
  input_destination = document.getElementById('input_destination');
  form = document.getElementById('form');

  var client_campaign_containers = Array.from(document.getElementsByClassName('client_campaign'));
  for (let container of client_campaign_containers) {
    container.addEventListener('click', () => {
      redirect_to("WORKFLOW", {'campaign_id': container.dataset.campaign_id});
    });
  }
  var campaign_containers = Array.from(document.getElementsByClassName('campaign_container'));
  for (let container of campaign_containers) {
    container.addEventListener('click', () => {
      redirect_to("WORKFLOW", {'campaign_id': container.dataset.campaign_id});
    });
  }
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
