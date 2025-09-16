# Set base path (adjust if needed)
$basePath = "C:\RnD\GigiProjects\WaterLevel\prompt-library - WaterLevel"

# Define tasks from WaterLevel Plan
$tasks = @(
    @{ ID = "T0"; Topic = "EnvironmentSetup" },
    @{ ID = "T1"; Topic = "BackendSetup" },
    @{ ID = "T2"; Topic = "DatabaseCoreServices" },
    @{ ID = "T3"; Topic = "AuthLogin" },
    @{ ID = "T4"; Topic = "BasicDashboard" },
    @{ ID = "T5"; Topic = "RBAC" },
    @{ ID = "T6"; Topic = "LocalNetworkExposure" },
    @{ ID = "T7"; Topic = "InternetExposure" },
    @{ ID = "T8"; Topic = "Deployment" },
    @{ ID = "T9"; Topic = "DashboardDesign" },
    @{ ID = "T10"; Topic = "RBAC" },
    @{ ID = "T11"; Topic = "UARTConfigPanel" },
    @{ ID = "T12"; Topic = "UARTService" },
    @{ ID = "T13"; Topic = "WebSocketStreaming" },
    @{ ID = "T14"; Topic = "JobConfigPanel" },
    @{ ID = "T15"; Topic = "DashboardCharts" },
    @{ ID = "T16"; Topic = "OperatorControls" },
    @{ ID = "T18"; Topic = "ProjectionIntegration" },
    @{ ID = "T19"; Topic = "ErrorHandling" },
    @{ ID = "T20"; Topic = "UserManagement" },
    @{ ID = "T21"; Topic = "AuditLogging" },
    @{ ID = "T22"; Topic = "PDFReports" },
    @{ ID = "T23"; Topic = "PerformanceChecks" },
    @{ ID = "T24"; Topic = "SecurityHardening" },
    @{ ID = "T25"; Topic = "RunbookDemo" }
)

# Create folders and files
foreach ($task in $tasks) {
    $folderName = "$basePath\$($task.ID)_$($task.Topic)"
    $fileName = "$folderName\WL_$($task.ID)_Summary_$($task.Topic)_v1.md"

    # Create folder
    New-Item -ItemType Directory -Path $folderName -Force | Out-Null
    # Create file with template content
    $content = @"
# 📌 Prompt: Summary – $($task.Topic)

**Filename:** WL_$($task.ID)_Summary_$($task.Topic)_v1  
**Project:** WaterLevel  
**Milestone:** $($task.ID) – $($task.Topic)  
**Version:** v1  
**Author:** Dorel Dumencu

---

## 🎯 Goal

[Clearly state what you want Copilot to do.]

---

## 📚 Context

[Provide background information about the project, milestone, and why this prompt is needed.]

---

## 📂 Source

[Specify the document, codebase, or data Copilot should refer to.]

---

## 📐 Expectations

[Describe how you want the output to be structured or formatted.]

---

## ✅ Final Prompt

> [Write the full prompt here.]

---

## 🧠 Notes & Feedback

[Leave space for team comments, prompt performance notes, or version history.]
"@

    Set-Content -Path $fileName -Value $content -Encoding UTF8
}

Write-Host "✅ Prompt Library created at $basePath"
