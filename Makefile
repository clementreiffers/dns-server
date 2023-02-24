install:
	python -m pip install -r requirements.txt

run:
	python main.py

build-app:
	pyinstaller  src/main.py --uac-admin

clean:
	rm *.spec