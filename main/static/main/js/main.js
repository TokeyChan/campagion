window.addEventListener('load', () => { main(); });

var input_action;
var input_destination;
var form;
function main() {
    console.log("test");
    form = document.getElementById('main_form');
    input_destination = document.getElementById('input_destination');
    input_action = document.getElementById('input_action');

    var modules = document.getElementsByClassName('module');
    console.log(modules);
    for (let module of modules) {
        module.addEventListener('click', () => {
            input_action.value = "REDIRECT";
            input_destination.value = module.dataset.url;
            form.submit();
        });
    }
}