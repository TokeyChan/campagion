function main() {
  let templates = document.getElementsByClassName("template");
  let form = document.getElementById("post_form");
  let input_template_id = document.getElementById("input_template_id");
  let input_action = document.getElementById("input_action");
  let btn_abort = document.getElementById("btn_abort");
  let btn_new_template = document.getElementById("btn_new_template");

  for (let template of templates) {
    let edit = template.getElementsByClassName('edit_icon')[0];
    let del = template.getElementsByClassName('delete_icon')[0];
    edit.addEventListener('click', () => {
      input_action.value = "EDIT";
      input_template_id.value = template.dataset.template_id;
      form.submit();
    });
    template.addEventListener('click', () => {
      input_action.value = "CHOSEN";
      input_template_id.value = template.dataset.template_id;
      form.submit();
    });
    del.addEventListener('click', () => {
      input_action.value = "DELETE";
      input_template_id.value = template.dataset.template_id;
      form.submit();
    });
  }
  btn_abort.addEventListener('click', () => {
    input_action.value = "ABORT";
    form.submit();
  });
  btn_new_template.addEventListener('click', () => {
    input_action.value = "NEW_TEMPLATE";
    form.submit();
  });
}



window.addEventListener('load', () => { main(); });
