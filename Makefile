run:
	streamlit run app.py

freeze:
	pip freeze > requirements.txt

deploy:
	gcloud app deploy app.yaml --project=bitly-ai-experiments --service-account=bitly-ai-experiments@appspot.gserviceaccount.com --quiet

logs:
	gcloud app logs tail -s default

browse:
	gcloud app browse