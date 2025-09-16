
# 🚀 Starting prompt generation...

# Set base path (adjust to your project folder)
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
    @{ ID = "T10"; Topic = "UARTConfigPanel" },
    @{ ID = "T11"; Topic = "UARTService" },
    @{ ID = "T12"; Topic = "WebSocketStreaming" },
    @{ ID = "T13"; Topic = "JobConfigPanel" },
    @{ ID = "T14"; Topic = "DashboardCharts" },
    @{ ID = "T15"; Topic = "OperatorControls" },
    @{ ID = "T16"; Topic = "ProjectionIntegration" },
    @{ ID = "T17"; Topic = "ErrorHandling" },
    @{ ID = "T18"; Topic = "UserManagement" },
    @{ ID = "T19"; Topic = "AuditLogging" },
    @{ ID = "T20"; Topic = "PDFReports" },
    @{ ID = "T21"; Topic = "PerformanceChecks" },
    @{ ID = "T22"; Topic = "SecurityHardening" },
    @{ ID = "T23"; Topic = "RunbookDemo" }
)

# Define prompt types
$promptTypes = @("1_Plan", "2_ArchitectureReview", "3_CodeReview", "4_TestPlan", "5_Summary", "6_NextSteps", "7_Roadmap")

# Template generator
function Get-PromptTemplate {
    param (
        [string]$PromptType,
        [string]$TaskID,
        [string]$Topic
    )

    $filename = "WL_${TaskID}_${PromptType}_${Topic}_v1"
    $milestone = "$TaskID – $Topic"

    $goal = switch ($PromptType) {
        "Plan" { "Generate a detailed implementation plan for the $milestone milestone." }
        "ArchitectureReview" { "Evaluate the system architecture for $Topic in terms of scalability, security, and maintainability." }
        "CodeReview" { "Review the code implementation for $Topic and provide feedback on quality and best practices." }
        "TestPlan" { "Define a comprehensive testing strategy for $Topic." }
        "Summary" { "Summarize the implementation details and progress of the $milestone milestone." }
        "NextSteps" { "Identify logical next steps following the completion of $milestone." }
        "Roadmap" { "Generate a roadmap for the next phase following $milestone." }
    }

    $expectations = switch ($PromptType) {
        "1_Plan" {
            @"
- Break down the task into actionable steps  
- Include backend, frontend, and integration components  
- Suggest best practices and reusable components  
- Format as a checklist or structured plan  
- **Generate a component diagram showing interactions between modules**
"@
        }
        "2_ArchitectureReview" {
            @"
- Identify strengths and weaknesses  
- Suggest improvements or alternatives  
- Highlight missing components or risks  
- Format feedback as pros/cons and recommendations
"@
        }
        "3_CodeReview" {
            @"
- Highlight issues with readability, performance, or security  
- Suggest improvements or refactoring opportunities  
- Use inline comments or bullet points for clarity
"@
        }
        "4_TestPlan" {
            @"
- List test cases and expected outcomes  
- Recommend tools or frameworks  
- Include edge cases and failure scenarios  
- Format as a checklist or table
"@
        }
        "5_Summary" {
            @"
- Highlight key technologies and components used  
- Summarize backend and frontend implementation steps  
- Include challenges and resolutions  
- Provide next-step recommendations  
- Format as a structured summary
"@
        }
        "6_NextSteps" {
            @"
- List next tasks in priority order  
- Include dependencies and estimated effort  
- Format as a checklist or timeline
"@
        }
        "R7_oadmap" {
            @"
- List tasks in priority order  
- Include dependencies and estimated effort  
- Format as a roadmap or timeline
"@
        }
    }

    return @"
# 📌 Prompt: $PromptType – $Topic

**Filename:** $filename  
**Project:** WaterLevel  
**Milestone:** $milestone  
**Version:** v1  
**Author:** Dorel Dumencu

---

## 🎯 Goal

$goal

---

## 📚 Context

This task is part of the WaterLevel telemetry system, which monitors angle-controlled robots.

---

## 📂 Source

Refer to the WaterLevel Plan.xlsx and any related implementation files.

---

## 📐 Expectations
$expectations
---

## ✅ Final Prompt

> [Write the full prompt here.]

---

## 🧠 Notes & Feedback

[Leave space for team comments or improvements.]
"@
}

# Create folders and files
if (!(Test-Path $basePath)) {
    Write-Host "❌ Base path does not exist: $basePath"
    exit
}

foreach ($task in $tasks) {
    $folderName = "$basePath\$($task.ID)_$($task.Topic)"
    try {
        if (!(Test-Path $folderName)) {
            New-Item -ItemType Directory -Path $folderName -Force | Out-Null
            Write-Host "📁 Created folder: $folderName"
        }
    } catch {
        Write-Host "❌ Error creating folder: $folderName - $_"
        continue
    }

    foreach ($type in $promptTypes) {
        Write-Host "✅ Creating: $type for $($task.ID) - $($type)"
        $fileName = "$folderName\WL_$($task.ID)_$type_$($type)_v1.md"
        Write-Host "✅ Creating: $fileName"

        if (!(Test-Path $fileName)) {
            $content = Get-PromptTemplate -PromptType $type -TaskID $task.ID -Topic $task.Topic
            if ($null -ne $content -and $content -ne "") {
                try {
                     Write-Host "✅ Creating: $fileName - set content"
                    Set-Content -Path $fileName -Value $content -Encoding UTF8
                    Write-Host "✅ Created: $fileName"
                } catch {
                    Write-Host "❌ Error creating file: $fileName - $_"
                }
            } else {
                Write-Host "⚠️ Empty content for $fileName"
            }
        } else {
            Write-Host "⚠️ Skipped (already exists): $fileName"
        }
    }
}

Write-Host "`n🎉 Prompt file generation completed with overwrite protection!"

