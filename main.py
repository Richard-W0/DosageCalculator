import math
import datetime as dt
import tkinter as tk
from tkinter import messagebox

def halfTime(t, dose, ht):
    return dose * math.exp(math.pow(ht, -1) * (- math.log(2)) * t)

def getTime(dose, time, ht, outputLabel):
    for i in range(10000):
        x = halfTime(i/60, dose, ht)
        if x < 1:
            change = dt.timedelta(minutes=i)
            newTime = time + change
            if newTime.strftime("%d") != time.strftime("%d"):
                result = f"Under 1mg: Tomorrow at {newTime.strftime('%H:%M')}"
            else:
                result = f"Under 1mg: {newTime.strftime('%H:%M')}"
            outputLabel.config(text=result)
            break

def printTime(time, dose, ht, textWidget):
    textWidget.delete('1.0', tk.END)
    for i in range(1, 24):
        chartTime = time.replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=i)
        minutes = (chartTime - time).total_seconds() / 60
        j = (minutes / 60)
        textWidget.insert(tk.END, f"{chartTime.strftime('%H:%M')}: {halfTime(j, dose, ht):.2f} mg\n")

def runCalculation():
    try:
        dose = int(doseEntry.get())
        half = float(halfTimeEntry.get())
        choice = timeChoiceVar.get()
        
        if choice == "Now":
            atm = dt.datetime.now()
            getTime(dose, atm, half, outputLabel)
            if chartVar.get():
                printTime(atm, dose, half, chartText)
        elif choice == "Earlier":
            time = timeEntry.get()
            taken = dt.datetime.strptime(time, "%H:%M")
            getTime(dose, taken, half, outputLabel)
            if chartVar.get():
                printTime(taken, dose, half, chartText)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter all values.")

app = tk.Tk()
app.title("Half-Life Calculator")

tk.Label(app, text="Dose (mg):").grid(row=0, column=0)
doseEntry = tk.Entry(app)
doseEntry.grid(row=0, column=1)

tk.Label(app, text="Half Time (hr):").grid(row=1, column=0)
halfTimeEntry = tk.Entry(app)
halfTimeEntry.grid(row=1, column=1)

timeChoiceVar = tk.StringVar(value="Now")
tk.Radiobutton(app, text="Now", variable=timeChoiceVar, value="Now").grid(row=2, column=0)
tk.Radiobutton(app, text="Earlier", variable=timeChoiceVar, value="Earlier").grid(row=2, column=1)

tk.Label(app, text="Time Taken (HH:MM):").grid(row=3, column=0)
timeEntry = tk.Entry(app)
timeEntry.grid(row=3, column=1)

chartVar = tk.BooleanVar()
tk.Checkbutton(app, text="Show Hourly Chart", variable=chartVar).grid(row=4, column=0, columnspan=2)

tk.Button(app, text="Calculate", command=runCalculation).grid(row=5, column=0, columnspan=2)

outputLabel = tk.Label(app, text="", fg="blue")
outputLabel.grid(row=6, column=0, columnspan=2)

chartText = tk.Text(app, height=15, width=30)
chartText.grid(row=7, column=0, columnspan=2)

app.mainloop()