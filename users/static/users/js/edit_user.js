window.addEventListener('load', () => { main(); });

function main()
{
    var profile_picture_input = document.getElementById('id_profile_picture');
    var profile_picture_image = document.getElementById('profile_picture_img');
    var save_button = document.getElementById('save_button');

    document.getElementById('upload_button').addEventListener('click', () => {
        profile_picture_input.click();
    });
    profile_picture_input.addEventListener('change', () => {
        var file = profile_picture_input.files[0];
        if (file != null) {
            profile_picture_image.src = URL.createObjectURL(file);
        }
    });
    save_button.addEventListener('click', () => {
        document.getElementById('user_form').submit();
    });
}