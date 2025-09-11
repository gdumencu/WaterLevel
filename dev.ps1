param (
    [string]$target = ""
)

$backendPath = "C:\RnD\GigiProjects\WaterLevel\backend"
$frontendPath = "C:\RnD\GigiProjects\WaterLevel\frontend"

function Start-Backend {
    Write-Host "🚀 Starting FastAPI backend with reload..."
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; uvicorn app.main:app --reload --port 8001"
}

function Start-Frontend {
    Write-Host "🌐 Starting frontend..."
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm run dev"
}

switch ($target.ToLower()) {
    "backend" { Start-Backend }
    "frontend" { Start-Frontend }
    "both" {
        Write-Host "🔧 Starting both backend and frontend..."
        Start-Backend
        Start-Frontend
    }
    default {
        Write-Host "Usage: .\dev.ps1 [backend | frontend | both]"
    }
}
