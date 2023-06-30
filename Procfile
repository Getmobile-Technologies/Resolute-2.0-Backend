web: daphne res_config.asgi:application --port $PORT --bind 0.0.0.0 -v2
release: python manage.py migrate
worker: python manage.py runworker --settings=res_config.settings -v2