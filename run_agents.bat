@echo off
REM Skrypt uruchamiający agentów dla Harmonogramu Zadań Windows
REM Jeśli używasz środowiska wirtualnego, zaktualizuj poniższą ścieżkę do pythona.

cd /d "%~dp0"
echo Uruchamiam agentow Cyfrowego Ksiegozbioru...

python run_agents.py
pause
