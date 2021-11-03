run:
	FLASK_APP=service:app flask run -h 0.0.0.0

debug:
	export FLASK_ENV="development" && FLASK_APP=service:app flask run -h 0.0.0.0
