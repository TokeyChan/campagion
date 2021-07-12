function main() {
  let templates = document.getElementsByClassName("template");
  let form = document.getElementById("post_form");
  let input_template_id = document.getElementById("input_template_id");
  let input_action = document.getElementById("input_action");

  for (let template of templates) {
    let edit = template.getElementsByClassName('edit_icon')[0];
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
  }
}



window.addEventListener('load', () => { main(); });
