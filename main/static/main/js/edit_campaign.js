window.addEventListener('load', () => {
    main();
});

function main() {

}

function submit_grunddaten() {
    document.getElementById('grunddaten_form').submit();
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
        case "api":
            document.getElementById('api_container').style.display = "block";
            break;
        case "files":
            document.getElementById('files_container').style.display = "grid";
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