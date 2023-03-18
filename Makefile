install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

run:
	python3 main.py

build-app:
	pyinstaller --onefile  src/main.py --icon=images/logo.ico --noconsole --uac-admin

macos-build-app:
	pyinstaller --onefile  src/main.py --icon=images/logo.icns --noconsole --uac-admin

clean:
	rm *.spec