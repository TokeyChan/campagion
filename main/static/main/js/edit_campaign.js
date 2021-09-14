window.addEventListener('load', () => {
    main();
});

function main() {
    document.getElementById('add_client').addEventListener('click', () => {
        show_popup();
    });
    document.getElementById('new_minicampaign').addEventListener('click', () => {
        new_minicampaign();
    });
    const api_manager = new ApiManager(CAMPAIGN_ID);
}

function submit_grunddaten() {
    document.getElementById('grunddaten_form').submit();
}

function delete_row(img) {
    if (confirm('Soll dieser Eintrag wirklich gelöscht werden?')) {
        const table = document.getElementById('children_table');
        const row = img.parentNode.parentNode;
        row.parentNode.removeChild(row);
    }
}

function new_minicampaign() {
    const table = document.getElementById('children_table');
    const row = document.createElement('tr');
    for (let i = 0; i < 3; i++) {
        const td = document.createElement('td');
        if (i != 2) {
            const input = document.createElement('input');
            input.type = 'text';
            td.appendChild(input);
        } else {
            const img = document.createElement('img');
            img.src = DELETE_ICON_PATH;
            img.addEventListener('click', () => {
                delete_row(img);
            });
            td.appendChild(img);
        }
        row.appendChild(td);
    }
    table.appendChild(row);
}

function change_view(sender) {
    if (sender.classList.contains('selected'))
        return;
    let menu_items = Array.from(document.getElementsByClassName('sidebar_menu'));
    let selected_item = menu_items.filter(t => t.classList.contains('selected'))[0];
    selected_item.classList.remove('selected');
    sender.classList.add('selected');

    let visible_container = Array.from(document.getElementsByClassName('view_container')).filter(t => t.style.display != "none")[0];
    visible_container.style.display = "none";

    switch (sender.dataset.tag) {
        case "grunddaten":
            document.getElementById('grunddaten_container').style.display = "block";
            break;
        case "children":
            document.getElementById('children_container').style.display = "grid";
            break;
        case "api":
            document.getElementById('api_container').style.display = "block";
            break;
        case "files":
            document.getElementById('files_container').style.display = "grid";
            break;
        case "progress":
            document.getElementById('progress_container').style.display = "block";
            break;
    }
}

function open_folder(sender) {
    if (sender.classList.contains('selected'))
        return;

    let selected_folder = Array.from(document.getElementsByClassName('folder')).filter(t => t.classList.contains('selected'))[0];
    if (selected_folder != null)
        selected_folder.classList.remove('selected');

    sender.classList.add('selected');

    let folder = sender.dataset.folder;

    let sidemenu = document.getElementById('files_sidemenu');
    let visible_files = Array.from(sidemenu.getElementsByClassName('file'));

    let hidden_div = document.getElementById("hidden_div");
    for(let file of visible_files) {
        hidden_div.appendChild(file);
    }
    let files = Array.from(document.getElementsByClassName('file')).filter(t => t.dataset.folder == folder);
    for (let file of files) {
        sidemenu.appendChild(file);
    }
}

function show_file(sender) {
    if (sender.classList.contains('selected'))
        return;
    let selected_file = Array.from(document.getElementsByClassName('file')).filter(t => t.classList.contains('selected'))[0];
    if (selected_file != null)
        selected_file.classList.remove('selected');

    sender.classList.add('selected')

    let url = sender.dataset.url;
    let iframe = document.getElementById('file_iframe');
    iframe.src = url;
}

function submit_client_form()
{
    var form = document.getElementById('new_client_form');
    let form_data = new FormData(form);
    send_request(form.action, form.method, form_data, on_post_response, form_data.get("csrfmiddlewaretoken"));
}

function on_post_response(response_text) {
    console.log(response_text);
    let table = document.getElementById('new_client_table');
    let response = JSON.parse(response_text);
    if (response.html) {
        table.innerHTML = response.html;
    } else {
        let select = document.getElementById('id_client');
        let hidden_div = document.getElementById('hidden_div');
        hidden_div.innerHTML += response.option;
        let option = hidden_div.getElementsByTagName('option')[0];
        hidden_div.removeChild(option);
        select.appendChild(option);
        let option_count = select.getElementsByTagName('option').length;
        select.selectedIndex = option_count - 1;
        hide_popup();
    }
}

function post(action) {
    document.getElementById('input_action').value = action;
    document.getElementById('button_form').submit();
}

function save_children() {
    const table = document.getElementById('children_table');
    var rows = Array.from(table.rows);
    rows.shift();
    var obj = {'rows': []};
    for (const row of rows) {
        obj['rows'].push({
            'id': parseInt(row.dataset.child_id) || null,
            'name': row.cells[0].getElementsByTagName('input')[0].value,
            'api_id': parseInt(row.cells[1].getElementsByTagName('input')[0].value)
        });
    }
    const input = document.getElementById('id_children_json');
    input.value = JSON.stringify(obj);
    document.getElementById('grunddaten_form').submit();
}