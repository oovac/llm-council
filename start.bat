@echo off
echo Starting LLM Council...
echo.

echo Starting backend on http://localhost:8001...
start "backend" cmd /c "uv run python -m backend.main"
set BACKEND_PID=%!

timeout /t 2 >nul

echo Starting frontend on http://localhost:5173...
pushd frontend
start "frontend" cmd /c "npm run dev"
popd

echo.
echo ✓ LLM Council is running!
echo   Backend:  http://localhost:8001
echo   Frontend: http://localhost:5173
echo.
echo Press Ctrl+C to stop both servers
echo (Note: Windows cannot auto-kill both processes on Ctrl+C)

pause
