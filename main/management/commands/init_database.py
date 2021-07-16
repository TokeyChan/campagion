from tracker.models import Completer

click_completer = Completer(
    name = 'ClickCompleter',
    handler = 'tracker.contrib.completers.ClickCompleter'
)
click_completer.save()

upload_completer = Completer(
    name = 'UploadCompleter',
    handler = 'tracker.contrib.completers.UploadCompleter'
)
upload_completer.save()