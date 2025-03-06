import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import time
import datetime
import pygame  # Using pygame for sound
import threading
import random
import math

# Initialize pygame mixer once at startup
pygame.mixer.init()

# Global variables
alarms = []  # List to store alarm dictionaries
alarm_id_counter = 0  # Counter for unique alarm IDs
snooze_time = 5  # Default snooze time in minutes
current_theme = 'basic_light'  # Default theme

# Theme color schemes
themes = {
    'basic_light': {
        'bg': 'white',
        'fg': 'black',
        'button_bg': '#D3D3D3',  # Light gray
        'button_fg': 'black',
        'clock_bg': '#F0F0F0',  # Very light gray
        'clock_fg': 'black',
        'hand_hour': 'black',
        'hand_minute': 'black',
        'hand_second': 'red'
    },
    'basic_dark': {
        'bg': '#333333',  # Dark gray
        'fg': 'white',
        'button_bg': '#555555',  # Darker gray
        'button_fg': 'white',
        'clock_bg': '#444444',  # Medium dark gray
        'clock_fg': 'white',
        'hand_hour': 'white',
        'hand_minute': 'white',
        'hand_second': 'red'
    },
    'midnight': {
        'bg': '#191970',  # Midnight blue
        'fg': 'white',
        'button_bg': '#4169E1',  # Royal blue
        'button_fg': 'white',
        'clock_bg': '#000080',  # Navy blue
        'clock_fg': 'white',
        'hand_hour': 'white',
        'hand_minute': 'lightblue',
        'hand_second': 'red'
    },
    'sunrise': {
        'bg': '#FFDAB9',  # Peach puff
        'fg': 'black',
        'button_bg': '#FFA500',  # Orange
        'button_fg': 'black',
        'clock_bg': '#FFFFE0',  # Light yellow
        'clock_fg': 'black',
        'hand_hour': 'black',
        'hand_minute': 'blue',
        'hand_second': 'red'
    }
}

# Function to generate unique alarm IDs
def get_next_id():
    global alarm_id_counter
    alarm_id_counter += 1
    return alarm_id_counter

# Function to update the analog clock and check alarms
def update_clock():
    now = datetime.datetime.now()
    hour = now.hour % 12
    minute = now.minute
    second = now.second

    # Calculate angles for clock hands
    hour_angle = (hour + minute / 60) * 30  # 30° per hour
    minute_angle = (minute + second / 60) * 6  # 6° per minute
    second_angle = second * 6  # 6° per second

    # Delete old hands
    canvas.delete('hands')

    # Draw new hands with theme colors and adjusted lengths
    theme = themes[current_theme]
    hour_x = center_x + 60 * math.sin(math.radians(hour_angle))  # Shorter hour hand
    hour_y = center_y - 60 * math.cos(math.radians(hour_angle))
    canvas.create_line(center_x, center_y, hour_x, hour_y, width=8, fill=theme['hand_hour'], tags='hands')

    minute_x = center_x + 100 * math.sin(math.radians(minute_angle))  # Medium minute hand
    minute_y = center_y - 100 * math.cos(math.radians(minute_angle))
    canvas.create_line(center_x, center_y, minute_x, minute_y, width=4, fill=theme['hand_minute'], tags='hands')

    second_x = center_x + 120 * math.sin(math.radians(second_angle))  # Longer second hand
    second_y = center_y - 120 * math.cos(math.radians(second_angle))
    canvas.create_line(center_x, center_y, second_x, second_y, width=2, fill=theme['hand_second'], tags='hands')

    # Draw center dot
    canvas.create_oval(center_x - 5, center_y - 5, center_x + 5, center_y + 5, fill=theme['hand_hour'], tags='hands')

    # Check for active alarms
    for alarm in alarms:
        if alarm['active'] and not alarm['handling'] and now >= alarm['time']:
            alarm['handling'] = True  # Mark as being handled
            trigger_alarm(alarm)

    # Schedule next update (every 1 second)
    root.after(1000, update_clock)

# Function to trigger an alarm
def trigger_alarm(alarm):
    stop_event = threading.Event()
    sound_thread = threading.Thread(target=play_loop, args=(alarm['sound'], stop_event))
    sound_thread.start()

    # Create puzzle window with current theme
    puzzle_window = tk.Toplevel(root)
    puzzle_window.title("Wake Up!")
    puzzle_window.attributes('-topmost', True)  # Keep window on top
    puzzle_window.grab_set()  # Make it modal
    puzzle_window.configure(bg=themes[current_theme]['bg'])

    problem, result = generate_puzzle()
    # Use tk.Label for better color control
    tk.Label(puzzle_window, text=problem, bg=themes[current_theme]['bg'], fg=themes[current_theme]['fg']).pack(pady=10)
    answer_var = tk.StringVar()
    ttk.Entry(puzzle_window, textvariable=answer_var).pack(pady=5)

    def submit():
        try:
            if int(answer_var.get()) == result:
                stop_event.set()  # Stop sound
                alarm['active'] = False  # Deactivate alarm
                alarm['handling'] = False  # Reset handling flag
                update_alarm_list()
                puzzle_window.destroy()
            else:
                answer_var.set('')  # Clear incorrect input
        except ValueError:
            answer_var.set('')  # Clear invalid input

    def snooze():
        stop_event.set()  # Stop sound
        alarm['time'] = datetime.datetime.now() + datetime.timedelta(minutes=snooze_time)
        alarm['active'] = True  # Reactivate for snooze
        alarm['handling'] = False  # Reset handling flag
        update_alarm_list()
        puzzle_window.destroy()

    ttk.Button(puzzle_window, text="Submit", command=submit).pack(pady=5)
    ttk.Button(puzzle_window, text="Snooze", command=snooze).pack(pady=5)

# Function to play sound in a loop using pygame.mixer
def play_loop(sound, stop_event):
    try:
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play(loops=-1)  # Loop indefinitely
        while not stop_event.is_set():
            time.sleep(0.1)  # Small sleep to check stop_event periodically
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"Error playing alarm sound: {e}")

# Function to preview the selected sound
def preview_sound(sound):
    if sound:
        try:
            s = pygame.mixer.Sound(sound)
            s.play()
            threading.Timer(5, s.stop).start()  # Stop after 5 seconds
        except Exception as e:
            print(f"Error playing sound: {e}")

# Function to generate a random math puzzle
def generate_puzzle():
    operators = ['+', '*']
    operator = random.choice(operators)
    if operator == '+':
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        result = a + b
        problem = f"What is {a} + {b}?"
    else:  # '*'
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        result = a * b
        problem = f"What is {a} * {b}?"
    return problem, result

# Function to update the alarm list display
def update_alarm_list():
    for item in tree.get_children():
        tree.delete(item)
    for alarm in alarms:
        time_str = alarm['time'].strftime('%H:%M')
        sound_name = alarm['sound'].split('/')[-1] if alarm['sound'] else 'Default'
        active_str = 'Yes' if alarm['active'] else 'No'
        tree.insert('', 'end', values=(time_str, sound_name, active_str))

# Function to add a new alarm
def add_alarm():
    dialog = tk.Toplevel(root)
    dialog.title("Set Alarm")
    dialog.configure(bg=themes[current_theme]['bg'])

    # Time selection
    hour_var = tk.StringVar(value='00')
    minute_var = tk.StringVar(value='00')
    tk.Label(dialog, text="Hour:", bg=themes[current_theme]['bg'], fg=themes[current_theme]['fg']).grid(row=0, column=0, padx=10, pady=10)
    ttk.Spinbox(dialog, from_=0, to=23, textvariable=hour_var, width=2).grid(row=0, column=1)
    tk.Label(dialog, text="Minute:", bg=themes[current_theme]['bg'], fg=themes[current_theme]['fg']).grid(row=1, column=0, padx=10, pady=10)
    ttk.Spinbox(dialog, from_=0, to=59, textvariable=minute_var, width=2).grid(row=1, column=1)

    # Sound selection
    sound_var = tk.StringVar()
    tk.Label(dialog, text="Sound:", bg=themes[current_theme]['bg'], fg=themes[current_theme]['fg']).grid(row=2, column=0, padx=10, pady=10)
    sound_entry = ttk.Entry(dialog, textvariable=sound_var)
    sound_entry.grid(row=2, column=1)
    ttk.Button(dialog, text="Browse", command=lambda: sound_var.set(filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")]))).grid(row=2, column=2, padx=10)
    ttk.Button(dialog, text="Preview", command=lambda: preview_sound(sound_var.get())).grid(row=2, column=3, padx=10)

    # Active status
    active_var = tk.BooleanVar(value=True)
    ttk.Checkbutton(dialog, text="Active", variable=active_var).grid(row=3, column=0, columnspan=2, pady=10)

    def ok():
        hour = int(hour_var.get())
        minute = int(minute_var.get())
        now = datetime.datetime.now()
        alarm_time = datetime.datetime(now.year, now.month, now.day, hour, minute)
        if alarm_time < now:
            alarm_time += datetime.timedelta(days=1)  # Set for next day if time has passed
        sound = sound_var.get() or "default_alarm.mp3"  # Use default sound if none selected
        active = active_var.get()
        alarm = {'id': get_next_id(), 'time': alarm_time, 'sound': sound, 'active': active, 'handling': False}
        alarms.append(alarm)
        update_alarm_list()
        dialog.destroy()

    ttk.Button(dialog, text="OK", command=ok).grid(row=4, column=0, pady=10)
    ttk.Button(dialog, text="Cancel", command=dialog.destroy).grid(row=4, column=1, pady=10)

# Function to set the theme
def set_theme(theme_name):
    global current_theme
    current_theme = theme_name
    theme = themes[current_theme]
    style.configure('TButton', background=theme['button_bg'], foreground=theme['button_fg'])
    style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
    style.configure('TFrame', background=theme['bg'])
    # Configure custom Treeview style
    style.configure('Alarm.Treeview', background=theme['bg'], foreground=theme['fg'], fieldbackground=theme['bg'])
    style.configure('Alarm.Treeview.Heading', background=theme['button_bg'], foreground=theme['button_fg'])
    canvas.config(bg=theme['bg'])
    root.configure(bg=theme['bg'])
    # Redraw clock face with new colors
    canvas.delete('clock_face')
    canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                       fill=theme['clock_bg'], outline=theme['clock_fg'], width=2, tags='clock_face')
    for i in range(12):
        angle = i * 30
        angle_rad = math.radians(angle)
        if i % 3 == 0:
            x1 = center_x + (radius - 15) * math.sin(angle_rad)
            y1 = center_y - (radius - 15) * math.cos(angle_rad)
            x2 = center_x + radius * math.sin(angle_rad)
            y2 = center_y - radius * math.cos(angle_rad)
            canvas.create_line(x1, y1, x2, y2, width=3, fill=theme['clock_fg'], tags='clock_face')
        else:
            x1 = center_x + (radius - 10) * math.sin(angle_rad)
            y1 = center_y - (radius - 10) * math.cos(angle_rad)
            x2 = center_x + radius * math.sin(angle_rad)
            y2 = center_y - radius * math.cos(angle_rad)
            canvas.create_line(x1, y1, x2, y2, width=1, fill=theme['clock_fg'], tags='clock_face')
    update_clock()

# Main window setup
root = tk.Tk()
root.title("Python Alarm Clock")
root.configure(bg=themes[current_theme]['bg'])

style = ttk.Style()

# Analog clock canvas
canvas = tk.Canvas(root, width=400, height=400, bg=themes[current_theme]['bg'], highlightthickness=0)
canvas.pack(pady=20)

center_x = 200
center_y = 200
radius = 150

# Draw initial clock face
canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                   fill=themes[current_theme]['clock_bg'], outline=themes[current_theme]['clock_fg'], width=2, tags='clock_face')
for i in range(12):
    angle = i * 30
    angle_rad = math.radians(angle)
    if i % 3 == 0:
        x1 = center_x + (radius - 15) * math.sin(angle_rad)
        y1 = center_y - (radius - 15) * math.cos(angle_rad)
        x2 = center_x + radius * math.sin(angle_rad)
        y2 = center_y - radius * math.cos(angle_rad)
        canvas.create_line(x1, y1, x2, y2, width=3, fill=themes[current_theme]['clock_fg'], tags='clock_face')
    else:
        x1 = center_x + (radius - 10) * math.sin(angle_rad)
        y1 = center_y - (radius - 10) * math.cos(angle_rad)
        x2 = center_x + radius * math.sin(angle_rad)
        y2 = center_y - radius * math.cos(angle_rad)
        canvas.create_line(x1, y1, x2, y2, width=1, fill=themes[current_theme]['clock_fg'], tags='clock_face')

# Alarm list frame
alarms_frame = ttk.Frame(root)
alarms_frame.pack(pady=10)

columns = ('Time', 'Sound', 'Active')
tree = ttk.Treeview(alarms_frame, style='Alarm.Treeview', columns=columns, show='headings', height=5)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack()

# Buttons frame
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

add_button = ttk.Button(button_frame, text="Add Alarm", command=add_alarm)
add_button.pack(side='left', padx=10)

settings_button = ttk.Button(button_frame, text="Settings", command=lambda: open_settings())
settings_button.pack(side='left', padx=10)

# Function to open settings window
def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.configure(bg=themes[current_theme]['bg'])

    # Snooze time
    tk.Label(settings_window, text="Snooze Time (minutes):", bg=themes[current_theme]['bg'], fg=themes[current_theme]['fg']).grid(row=0, column=0, padx=10, pady=10)
    snooze_var = tk.IntVar(value=snooze_time)
    ttk.Entry(settings_window, textvariable=snooze_var, width=5).grid(row=0, column=1)

    # Theme selection
    tk.Label(settings_window, text="Theme:", bg=themes[current_theme]['bg'], fg=themes[current_theme]['fg']).grid(row=1, column=0, padx=10, pady=10)
    theme_var = tk.StringVar(value=current_theme)
    theme_combobox = ttk.Combobox(settings_window, textvariable=theme_var, values=list(themes.keys()), state='readonly')
    theme_combobox.grid(row=1, column=1)
    theme_combobox.bind('<<ComboboxSelected>>', lambda event: set_theme(theme_var.get()))

    def save():
        global snooze_time
        snooze_time = snooze_var.get()
        settings_window.destroy()

    ttk.Button(settings_window, text="Save", command=save).grid(row=2, column=0, columnspan=2, pady=10)

# Start the clock with initial theme
set_theme('basic_light')
update_clock()

root.mainloop()