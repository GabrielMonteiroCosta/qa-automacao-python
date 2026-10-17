@echo off
chcp 65001 >nul
setlocal

rem Roda os testes com o navegador visivel e abre o relatorio no final.
rem Na primeira vez, cria o ambiente Python fora do OneDrive e instala as dependencias.
rem Para rodar so uma parte, passe as opcoes do pytest. Ex.: rodar_testes.bat -m ui
rem Se nao tiver o Google Chrome, troque "--browser-channel chrome" por "--browser-channel msedge".

set "PROJETO=%~dp0"
set "AMBIENTE=%USERPROFILE%\.venvs\qa-automacao-python"

if not exist "%AMBIENTE%\Scripts\python.exe" (
    echo Preparando o ambiente pela primeira vez. Isso leva alguns minutos...
    python -m venv "%AMBIENTE%" || goto erro
    "%AMBIENTE%\Scripts\python.exe" -m pip install --disable-pip-version-check -r "%PROJETO%requirements.txt" || goto erro
    "%AMBIENTE%\Scripts\python.exe" -m playwright install chromium || goto erro
)

cd /d "%PROJETO%"
echo.
echo Rodando os testes. O Chrome abre e fecha a cada teste de interface.
echo.
"%AMBIENTE%\Scripts\python.exe" -m pytest --headed --slowmo 400 --browser-channel chrome %*
start "" "%PROJETO%reports\relatorio.html"
echo.
pause
exit /b 0

:erro
echo.
echo Algo deu errado ao preparar o ambiente. Veja a mensagem acima.
pause
exit /b 1
