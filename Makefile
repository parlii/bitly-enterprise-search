run:
	streamlit run app.py --logger.level=debug --server.port=5001

freeze:
	pip freeze > requirements.txt