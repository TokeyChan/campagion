window.addEventListener('load', () => { main(); });

var form;
var action_input;
var user_id_input;
var department_id_input;

var new_user_button;
var new_department_button;

function main() {
    form = document.getElementById('action_form');
    action_input = document.getElementById('input_action');
    user_id_input = document.getElementById('input_user_id');
    department_id_input = document.getElementById('input_department_id');

    new_user_button = document.getElementById('btn_new_user');
    new_department_button = document.getElementById('btn_new_department');

    var departments = Array.from(document.getElementsByClassName('department'));
    var users = Array.from(document.getElementsByClassName('user'));

    for (let department of departments) {
        department.addEventListener('click', () => {
            action_input.value = "EDIT_DEPARTMENT";
            department_id_input.value = department.dataset.department_id;
            form.submit();
        });
    }
    for (let user of users) {
        user.addEventListener('click', () => {
            action_input.value = "EDIT_USER";
            user_id_input.value = user.dataset.user_id;
            form.submit();
        });
    }
    new_user_button.addEventListener('click', () => {
        show_popup();
    });
    new_department_button.addEventListener('click', () => {
        action_input.value = "NEW_DEPARTMENT";
        form.submit();
    });

    if (VALUES.EDIT_INVITATION_FORM == true) {

        show_popup();
    }
}

function invite_user() {
    document.getElementById('invitation_form').submit();
}