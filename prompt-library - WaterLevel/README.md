# 📚 WaterLevel Prompt Library

Welcome to the **Prompt Library** for the WaterLevel telemetry system. This repository contains reusable, well-structured prompts designed to help you and your team interact effectively with Copilot for R&D tasks.

---

## 🧠 Purpose

This library helps standardize how prompts are written and used across milestones, making it easier to:
- Summarize technical work
- Review code and architecture
- Plan next steps
- Generate documentation
- Collaborate with Copilot consistently
---

## 📁 Folder Structure

prompt-library/ └── WaterLevel/ ├── T0_EnvironmentSetup/ │ └── WL_T0_Summary_EnvironmentSetup_v1.md ├── T1_BackendSetup/ │ └── WL_T1_Summary_BackendSetup_v1.md ├── T2_DatabaseCoreServices/ │ └── WL_T2_Summary_DatabaseCoreServices_v1.md └── ... (and so on for each task)

Each folder contains:
- A Markdown file named using this format:  
  `WL_[TaskID]_[PromptType]_[Topic]_v1.md`

---

## 🧩 Prompt Template Structure

Each prompt file includes the following sections:

- **🎯 Goal** – What Copilot should do
- **📚 Context** – Background about the task or milestone
- **📂 Source** – Where Copilot should pull information from
- **📐 Expectations** – How the output should be structured
- **✅ Final Prompt** – The actual prompt to use
- **🧠 Notes & Feedback** – Space for team comments or improvements

---

## 🛠 How to Use in VS Code

1. Open your WaterLevel project in **Visual Studio Code**.
2. Navigate to the `prompt-library/WaterLevel/` folder.
3. Open any `.md` file to view, edit, or copy the prompt.
4. Paste the final prompt into Copilot or use it as a starting point.

---

## 🔄 Versioning & Collaboration

- Use Git to track changes to prompts.
- Add new versions with updated filenames (e.g., `v2`, `2025-09-17`).
- Collaborate via pull requests or comments.

---

## 📌 Naming Convention
[ProjectCode][MilestoneID][PromptType][Topic][Version]

Example:
WL_T3_Summary_AuthLogin_v1

---

## ✅ Tips for Writing Great Prompts

- Be clear and specific.
- Include all four ingredients: Goal, Context, Source, Expectations.
- Use structured formatting (bullet points, sections).
- Keep prompts short but informative.

---

## 📬 Questions or Suggestions?

Feel free to add notes in the `🧠 Notes & Feedback` section of each prompt file or open a GitHub issue if you're using version control.

---

Happy prompting!  
— Dorel Dumencu & R&D Team