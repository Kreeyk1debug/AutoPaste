from tkinter import *
from tkinter import ttk
import keyboard
import time
import threading

root = Tk()
root.resizable(height=False, width=False)
root["bg"] = "#1E1D1D"
root.geometry("1050x750")
root.title("AutoPaste")

is_running = False
current_thread = None

time_mode = StringVar(value="seconds")

def paste_cycle():
    global is_running
    while is_running:
        text = t_field.get(1.0, END).strip()
        if text:
            time.sleep(1)
            
            import pyperclip
            pyperclip.copy(text)
            
            time.sleep(0.2)
            keyboard.press_and_release('ctrl+v')
            time.sleep(0.1)
            keyboard.press("enter")
            time.sleep(0.1)
            keyboard.release("enter")
        
        if time_mode.get() == "seconds":
            interval = seconds_scale.get()
        else:
            interval = minutes_scale.get() * 60
        
        time.sleep(interval)

def toggle_pasting():
    if is_running:
        stop_pasting()
    else:
        start_pasting()

def start_pasting():
    global is_running, current_thread
    if not is_running:
        is_running = True
        current_thread = threading.Thread(target=paste_cycle, daemon=True)
        current_thread.start()
        status_label.config(text="СТАТУС: АКТИВНО 🟢", fg="green")
        start_btn.config(bg="orange", text="АКТИВНО")

def stop_pasting():
    global is_running
    is_running = False
    status_label.config(text="СТАТУС: ОСТАНОВЛЕНО 🔴", fg="red")
    start_btn.config(bg="lightgreen", text="СТАРТ")

def on_closing():
    stop_pasting()
    try:
        keyboard.remove_hotkey(hotkey_id)
    except:
        pass
    root.destroy()

def toggle_scales():
    if time_mode.get() == "seconds":
        seconds_frame.pack()
        minutes_frame.pack_forget()
    else:
        seconds_frame.pack_forget()
        minutes_frame.pack()

def format_minutes(value):
    minutes = int(value)
    if value % 1 == 0:
        return f"{int(minutes)} мин"
    else:
        return f"{minutes} мин 30 сек"

text_frame = Frame(root, bg="#1E1D1D")
text_frame.pack(pady=10)

t_field = Text(text_frame, bg='white', width=80, height=20, wrap=WORD)

t_field.bind('<Control-c>', lambda e: t_field.event_generate('<<Copy>>'))
t_field.bind('<Control-v>', lambda e: t_field.event_generate('<<Paste>>'))
t_field.bind('<Control-x>', lambda e: t_field.event_generate('<<Cut>>'))

def show_context_menu(event):
    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label="Копировать", command=lambda: t_field.event_generate('<<Copy>>'))
    context_menu.add_command(label="Вставить", command=lambda: t_field.event_generate('<<Paste>>'))
    context_menu.add_command(label="Вырезать", command=lambda: t_field.event_generate('<<Cut>>'))
    context_menu.tk_popup(event.x_root, event.y_root)

t_field.bind('<Button-3>', show_context_menu)
t_field.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(text_frame, command=t_field.yview)
scrollbar.pack(side=RIGHT, fill=Y)
t_field.config(yscrollcommand=scrollbar.set)

btn_frame = Frame(root, bg="#1E1D1D")
btn_frame.pack(pady=10)

start_btn = Button(btn_frame, text="СТАРТ", bg="lightgreen", 
                   font=("Arial", 10, "bold"), padx=20, pady=10, 
                   command=start_pasting)
start_btn.pack(side=LEFT, padx=5)

stop_btn = Button(btn_frame, text="СТОП", bg="lightcoral", 
                  font=("Arial", 10, "bold"), padx=20, pady=10, 
                  command=stop_pasting)
stop_btn.pack(side=LEFT, padx=5)

scales_frame = Frame(root, bg="#1E1D1D")
scales_frame.pack(pady=10)

mode_frame = Frame(scales_frame, bg="#1E1D1D")
mode_frame.pack()

Label(mode_frame, text="Режим:", bg="#1E1D1D", fg="white").pack(side=LEFT, padx=5)

Radiobutton(mode_frame, text="Секунды", variable=time_mode, value="seconds", 
            bg="#1E1D1D", fg="white", selectcolor="#1E1D1D", 
            command=toggle_scales).pack(side=LEFT, padx=5)

Radiobutton(mode_frame, text="Минуты", variable=time_mode, value="minutes", 
            bg="#1E1D1D", fg="white", selectcolor="#1E1D1D",
            command=toggle_scales).pack(side=LEFT, padx=5)

seconds_frame = Frame(scales_frame, bg="#1E1D1D")
Label(seconds_frame, text="Интервал (секунды):", bg="#1E1D1D", fg="white").pack()
seconds_scale = Scale(seconds_frame, from_=1, to=60, orient=HORIZONTAL, length=300, bg="white")
seconds_scale.set(3)
seconds_scale.pack()

minutes_frame = Frame(scales_frame, bg="#1E1D1D")
Label(minutes_frame, text="Интервал (минуты):", bg="#1E1D1D", fg="white").pack()

minutes_scale = Scale(minutes_frame, from_=0.5, to=10, resolution=0.5, 
                     orient=HORIZONTAL, length=300, bg="white")
minutes_scale.set(1)

minutes_frame_lower = Frame(minutes_frame, bg="#1E1D1D")
minutes_frame_lower.pack()
for i in range(1, 11):
    Label(minutes_frame_lower, text=str(i), bg="#1E1D1D", fg="white", font=("Arial", 8)).pack(side=LEFT, padx=12)

minutes_scale.pack()

def update_minutes_label(val):
    val = float(val)
    minutes = int(val)
    seconds_part = 30 if val % 1 != 0 else 0
    if seconds_part > 0:
        minutes_label.config(text=f"Текущее: {minutes} мин {seconds_part} сек")
    else:
        minutes_label.config(text=f"Текущее: {minutes} мин 00 сек")

minutes_scale.config(command=update_minutes_label)

minutes_label = Label(minutes_frame, text="Текущее: 1 мин 00 сек", 
                      bg="#1E1D1D", fg="cyan", font=("Arial", 10, "bold"))
minutes_label.pack()

toggle_scales()

status_label = Label(root, text="СТАТУС: ОСТАНОВЛЕНО 🔴", 
                     bg="#1E1D1D", fg="red", font=("Arial", 12, "bold"))
status_label.pack(pady=10)

hotkey_id = keyboard.add_hotkey('f9', toggle_pasting)

f9_label = Label(root, text="F9 - СТАРТ/СТОП", bg="#1E1D1D", fg="yellow", font=("Arial", 10, "bold"))
f9_label.pack()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()