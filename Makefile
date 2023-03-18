install:
	python -m pip install -r requirements.txt

run:
	python main.py

build-app:
	pyinstaller --onefile  src/main.py --icon=images/logo.ico --noconsole --uac-admin

clean:
	rm *.spec