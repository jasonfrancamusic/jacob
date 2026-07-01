@echo off
cd /d %~dp0backend
if not exist .venv (
  echo Criando ambiente virtual do Jacob...
  py -m venv .venv
)
call .venv\Scripts\activate
py -m pip install -r requirements.txt
echo.
echo Jacob Core API iniciando em http://127.0.0.1:8000
echo Deixe esta janela aberta.
echo.
py -m uvicorn app:app --reload
pause
