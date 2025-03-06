# 📌 Python Alarm Clock  
A modern, customizable alarm clock application built with Python, featuring an analog clock display, multiple alarm settings, and a unique wake-up puzzle to ensure you’re alert! This project combines functionality with an appealing user interface, offering a variety of themes and sound options to personalize your wake-up experience.

## 🔥 Unique Features Added

- **Analog Clock Animation**: A sleek, circular clock with moving hour, minute, and second hands for real-time display.
- **Multiple Alarms**: Set multiple alarms with custom times and sounds, each manageable through an intuitive list view.
- **Wake-Up Puzzle**: Solve a simple math problem (addition or multiplication) to stop the alarm, ensuring you’re awake and engaged.
- **Custom Sound Picker**: Choose your own `.mp3` or `.wav` alarm sounds, with a preview option to hear a 5-second snippet before setting.
- **Theme Selection**: Switch between four distinct themes—Basic Light, Basic Dark, Midnight, and Sunrise—with visually appealing color schemes.
- **Snooze Functionality**: Postpone alarms with a configurable snooze duration (default: 5 minutes).
- **Modern UI Design**: Enhanced clock face with a center dot, proportional hands, and prominent hour markers for a polished, contemporary look.

## 🛠 Technologies/Libraries Used
- **Python 3.x**: Core programming language.
- **Tkinter**: Standard GUI toolkit for building the interface (used via `tkinter` and `tkinter.ttk` for modern widgets).
- **Pygame**: Handles audio playback for alarm sounds (`pygame.mixer`).
- **Time**: Manages time-related operations.
- **Datetime**: Handles alarm scheduling and time comparisons.
- **Threading**: Enables non-blocking sound playback and preview.
- **Random**: Generates random math puzzles.
- **Math**: Calculates clock hand positions using trigonometry.

## 🎨 Screenshots of the UI

- **Main Window (Basic Light Theme)**
- <img width="402" alt="Screenshot 2025-03-06 at 2 12 13 PM" src="https://github.com/user-attachments/assets/96e408e8-3d0a-400c-b93c-e4306a9beecf" />

- **Main Window (Sunrise Theme)**
- ![image](https://github.com/user-attachments/assets/7cfa154b-c18b-4415-b5d3-164f00a81bb7)
- **Window (Midnight Theme)**
- ![image](https://github.com/user-attachments/assets/50cbdfa8-8d76-40d2-ab2a-2e29c234ee89)
- **Window(Basic Dark Theme)**
![image](https://github.com/user-attachments/assets/26172aa1-2f1c-4496-b111-138b80f1cf0d)

## 🚀 How to Run the Project

### Prerequisites

- Python 3.x installed (recommended: 3.12 for compatibility).
- Pip (Python package manager).

### Steps

1. **Clone or Download the Repository**:  
   Clone:  
   ```bash
   git clone <repository-link>
   Or download the ZIP file and extract it.

### Set Up a Virtual Environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```
Install Dependencies:
```bash
pip install pygame
```
Tkinter, time, datetime, threading, random, and math are part of Python’s standard library and require no additional installation.

## Prepare an Alarm Sound:
Place an .mp3 or .wav file named default_alarm.mp3 in the project directory (optional; you can select custom sounds later via the UI).
Alternatively, download sample alarm sounds from sites like Mixkit or Orange Free Sounds.

## Run the Application:
``` bash
python alarm_clock.py
```
Replace alarm_clock.py with the actual filename if you’ve named it differently.
