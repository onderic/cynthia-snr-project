web: python manage.py runserver
tailwind: npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch
watchstatic: watchmedo shell-command --patterns="*.css;*.js;*.html" --command="python manage.py collectstatic --noinput" --recursive static
