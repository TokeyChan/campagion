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
  if (method.toUpperCase() == 'POST') {
    if (data instanceof FormData){
      request.send(data)
    } else {
      let fd = new FormData();

      for (let key in data) {
        fd.append(key, data[key]);
      }
      request.send(fd);
    }
  } else {
    request.send();
  }
}

function get_absolute_position(element) {
  let rect = element.getBoundingClientRect();
  let left = rect.left + window.scrollX;
  let top = rect.top + window.scrollY;
  return {
    'left': left,
    'top': top
  }
}
function get_position(element) {
  let rect = element.getBoundingClientRect();
  return {
    'left': rect.left,
    'top': rect.top
  }
}

function show_popup() {
  var popup_background = document.getElementById('popup_background');
  popup_background.style.display = "flex";
}

function hide_popup() {
  var popup_background = document.getElementById('popup_background');
  popup_background.style.display = "none";
}

window.addEventListener('load', () => {
  let form = document.getElementById('base_form');
  let action = document.getElementById('base_input_action');
  let house = document.getElementById('house');
  let exit = document.getElementById('exit');
  let logo = document.getElementById('logo');

  if (house != null) {// house can be null if no Module is active i.e. in the index view
    house.addEventListener('click', () => {
      action.value = "HOME";
      form.submit();
    });
  }
  exit.addEventListener('click', () => {
    action.value = "LOGOUT";
    form.submit();
  });
  logo.addEventListener('click', () => {
    action.value = "TO_INDEX";
    form.submit();
  });


  let popup_closer = document.getElementById('popup_closer');
  if (popup_closer != null)
    popup_closer.addEventListener('click', hide_popup);
});
//document.querySelector('[name=csrfmiddlewaretoken]').value
