import math
import datetime as dt
import tkinter as tk
from tkinter import messagebox

def halfTime(t, dose, ht):
    return dose * math.exp(math.pow(ht, -1) * (math.log(0.5)) * t)

def getTime(dose, time, ht, output_label):
    for i in range(10000):
        x = halfTime(i/60, dose, ht)
        if x < 1:
            change = dt.timedelta(minutes=i)
            newTime = time + change
            if newTime.strftime("%d") != time.strftime("%d"):
                result = f"Under 1mg: Tomorrow at {newTime.strftime('%H:%M')}"
            else:
                result = f"Under 1mg: {newTime.strftime('%H:%M')}"
            output_label.config(text=result)
            break

def printTime(time, dose, ht, text_widget):
    text_widget.delete('1.0', tk.END)
    for i in range(1, 24):
        chartTime = time.replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=i)
        minutes = (chartTime - time).total_seconds() / 60
        j = (minutes / 60)
        text_widget.insert(tk.END, f"{chartTime.strftime('%H:%M')}: {halfTime(j, dose, ht):.2f} mg\n")

def run_calculation():
    try:
        dose = int(dose_entry.get())
        half = float(half_time_entry.get())
        choice = time_choice_var.get()
        
        if choice == "Now":
            atm = dt.datetime.now()
            getTime(dose, atm, half, output_label)
            if chart_var.get():
                printTime(atm, dose, half, chart_text)
        elif choice == "Earlier":
            time = time_entry.get()
            taken = dt.datetime.strptime(time, "%H:%M")
            getTime(dose, taken, half, output_label)
            if chart_var.get():
                printTime(taken, dose, half, chart_text)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter all values.")

app = tk.Tk()
app.title("Half-Life Calculator")

tk.Label(app, text="Dose (mg):").grid(row=0, column=0)
dose_entry = tk.Entry(app)
dose_entry.grid(row=0, column=1)

tk.Label(app, text="Half Time (hr):").grid(row=1, column=0)
half_time_entry = tk.Entry(app)
half_time_entry.grid(row=1, column=1)

time_choice_var = tk.StringVar(value="Now")
tk.Radiobutton(app, text="Now", variable=time_choice_var, value="Now").grid(row=2, column=0)
tk.Radiobutton(app, text="Earlier", variable=time_choice_var, value="Earlier").grid(row=2, column=1)

tk.Label(app, text="Time Taken (HH:MM):").grid(row=3, column=0)
time_entry = tk.Entry(app)
time_entry.grid(row=3, column=1)

chart_var = tk.BooleanVar()
tk.Checkbutton(app, text="Show Hourly Chart", variable=chart_var).grid(row=4, column=0, columnspan=2)

tk.Button(app, text="Calculate", command=run_calculation).grid(row=5, column=0, columnspan=2)

output_label = tk.Label(app, text="", fg="blue")
output_label.grid(row=6, column=0, columnspan=2)

chart_text = tk.Text(app, height=15, width=30)
chart_text.grid(row=7, column=0, columnspan=2)

app.mainloop()
