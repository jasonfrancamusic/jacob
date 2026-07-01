@echo off
cd /d %~dp0frontend
echo Jacob OS iniciando em http://127.0.0.1:5500
echo Deixe esta janela aberta.
echo.
start http://127.0.0.1:5500
py -m http.server 5500
pause
