install:
	 python3 -m venv venv || python -m venv venv
	./venv/bin/pip install -r requirements.txt || .\venv\Scripts\pip install -r requirements.txt

run:
	./venv/bin/python -m uvicorn "main:application" || .\venv\Scripts\python.exe -m uvicorn "main:application"

test:
	./venv/bin/python -m pytest ../tests/test_homework_1.py || .\venv\Scripts\python.exe -m pytest ../tests/test_homework_1.py

clean:
	rm -rf ./venv || rd /s /q venv
