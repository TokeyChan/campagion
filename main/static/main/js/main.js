window.addEventListener('load', () => { main(); });

var input_action;
var input_module;
var form;
function main() {
    form = document.getElementById('main_form');
    input_module = document.getElementById('input_module');
    input_action = document.getElementById('input_action');

    var modules = document.getElementsByClassName('module');
    for (let module of modules) {
        module.addEventListener('click', () => {
            input_action.value = "REDIRECT";
            input_module.value = module.dataset.name;
            form.submit();
        });
    }
}