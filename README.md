# 🧠 Crush It - Daily Task Logger (SQLite Edition) 🚀

A simple and intuitive Streamlit app to log your daily tasks with start and end times, track programming languages and platforms used, and visualize your productivity patterns.  
Data is stored locally in a SQLite database (`task_log.db`). 🗄️

👉 **Try the live app here:** [https://tasklogger.streamlit.app/](https://tasklogger.streamlit.app/)
---

## ✨ Features

- 📝 Log tasks with date, start time, end time, language, and platform info.
- ⏰ Validate that end time is after start time.
- 📋 View a table of tasks logged for the current day.
- 📊 Visualize **Time Distribution by Hour** to identify your peak productivity hours.
- 🗃️ Uses SQLite for lightweight local storage — no external database required.
- 🌍 Easy to run locally or deploy anywhere Streamlit apps are supported.

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.7+
- [Streamlit](https://streamlit.io/) ⚡
- [Pandas](https://pandas.pydata.org/) 🐼

### 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/crush-it-logger.git
cd crush-it-logger
