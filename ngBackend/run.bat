@echo off
cmd /k "cd /d ../env/Scripts/ & activate & cd /d ../../ngBackend & python manage.py runserver"

# Development environment only