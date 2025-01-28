run:
# xdg-open http://0.0.0.0:8000/docs 2> /dev/null
	python3 test/main.py & streamlit run test/front.py
