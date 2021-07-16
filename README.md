# Campagion


## Wie man es ausprobiert
Um die Webseite auszuprobieren, braucht man verschiedenr Sachen:
- Python (3.7 <=)
- Django (3.2 <=)

### Setup
Mit einem Terminal in den äußersten Ordner gehen.
Dann folgenden Befehl ausführen:

python3 manage.py migrate

Dabei wird eine kleine sqlite3 Datenbank mit dem Datenbankschema erstellt.

### Testen

Um den Testserver zu starten muss man in einem Terminal in den äußersten Ordner gehen und den folgenden Befehl ausführen:

python3 manage.py runserver

## Wie man die HTMLs und ihr CSS findet

Ein Django-Projekt ist in Apps aufgebaut. Diese bilden jeweils einen Ordner ab (zB. „main“ oder „tracker“)

In diesen Ordnern gibt es verschiedene Dateien, sowie Ordner.
Die zwei Ordner, die uns interessieren heißen „templates“ und „static“.

Templates beinhaltet die HTML-, Static die CSS- und JS-Files.

## Woher weiß man, welches CSS zu welchem HTML gehört?

- Jedes HTML hat „static/main/css/base.css“
Ansonsten findet man im HTML einen Block „head“ in welchem Dateien auf folgende Weise geladen werden:
{% static „path/to/file.css“ %}
