@echo off
echo Starting local web server for testing...
echo.
echo ==============================================================
echo IMPORTANT: A browser window will open automatically.
echo DO NOT CLOSE THIS BLACK WINDOW while you are testing!
echo ==============================================================
echo.
start http://localhost:8000/gurudev-super.html
python -m http.server 8000
