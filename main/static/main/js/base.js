function send_request(url, method, data, callback, csrfmiddlewaretoken)
{
  var request = new XMLHttpRequest();

  request.open(method, url, true);
  request.addEventListener('load', function(event) {
     if (request.status >= 200 && request.status < 300) {
        if (callback != null)
          callback(request.responseText);
     } else {
        console.warn(request.statusText, request.responseText);
     }
  });
  if (csrfmiddlewaretoken != null)
    request.setRequestHeader('X-CSRFToken', csrfmiddlewaretoken);
  if (method == 'POST') {
    let fd = new FormData();

    for (let key in data) {
      fd.append(key, data[key]);
    }
    request.send(fd);
  } else {
    request.send();
  }
}

window.addEventListener('load', () => {
  let form = document.getElementById('base_form');
  let action = document.getElementById('input_action');
  let house = document.getElementById('house');
  let exit = document.getElementById('exit');
  house.addEventListener('click', () => {
    action.value = "TO_OVERVIEW";
    form.submit();
  });
  exit.addEventListener('click', () => {
    action.value = "LOGOUT";
    form.submit();
  });
});
//document.querySelector('[name=csrfmiddlewaretoken]').value
