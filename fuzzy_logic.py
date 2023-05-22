import tkinter
import numpy as np
# Shows plots inside tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

import skfuzzy as fuzz
from skfuzzy import control as ctrl

root = tkinter.Tk()
root.wm_title("Fuzzy Logic")

level = ctrl.Antecedent(np.arange(-50, 50, 1), 'Level')
temp = ctrl.Antecedent(np.arange(-50, 50, 1), 'Temperature')
heat = ctrl.Consequent(np.arange(-50, 50, 1), 'Heat')

level.automf(names=["Low", "Medium", "High"])
temp.automf(names=["Low", "Medium", "High"])
heat.automf(names=["Low", "Medium", "High"])

# Fuzzy rules

water_control_system = ctrl.ControlSystem([
   ctrl.Rule(level['Low'] | temp['High'], heat['High']),
   ctrl.Rule(level['Medium'] | temp['Medium'], heat['Medium']),
   ctrl.Rule(level['High'] | temp['Low'], heat['Low']),
])

water_control = ctrl.ControlSystemSimulation(water_control_system)


fig, _ = level.get_view()

# Define tkinter widgets

canvas_frame = tkinter.Frame(root)

canvas_frame.pack(
    side=tkinter.LEFT,
    fill=tkinter.BOTH,
    expand=1,
)

canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
canvas.draw()

canvas.get_tk_widget().pack(
    side=tkinter.LEFT,
    fill=tkinter.BOTH,
    expand=True,
)

control_frame = tkinter.Frame(root)
control_frame.pack(
    side=tkinter.LEFT,
    fill=tkinter.BOTH,
    expand=True,
    anchor=tkinter.CENTER,
    padx=20,
)
control_frame.grid_rowconfigure(0, weight=1)
control_frame.grid_columnconfigure(0, weight=1)

# Centers the items placed inside this frame
control_frame_buttons = tkinter.Frame(control_frame)
control_frame_buttons.grid(
    row=0,
    column=0,
    sticky="",
)

level_var = tkinter.DoubleVar()
temp_var = tkinter.DoubleVar()
output_var = tkinter.DoubleVar()

def update_system():
    water_control.inputs({
        'Level': level_var.get(),
        'Temperature': temp_var.get(),
    })
    water_control.compute()
    output_var.set(f"{water_control.output['Heat']:9.4f}")
    # output_var = water_control.output['heat']

level_frame = tkinter.Frame(
    control_frame_buttons,
    relief=tkinter.GROOVE,
    borderwidth=2,
    pady=20,
)
level_frame.pack(padx=20, pady=20)
level_label = tkinter.Label(
    level_frame,
    borderwidth=2,
    text="Level",
).pack()
level_entry = tkinter.Entry(
    level_frame,
    textvariable=level_var,
    width=4,
    justify=tkinter.CENTER,
).pack()
level_slider = tkinter.Scale(
    level_frame,
    variable=level_var,
    from_=-50,
    to=50,
    orient=tkinter.HORIZONTAL,
    showvalue=False,
).pack()
for child in level_frame.winfo_children():
    child.pack_configure(padx=5, pady=5)

temp_frame = tkinter.Frame(
    control_frame_buttons,
    relief=tkinter.GROOVE,
    pady=20,
    borderwidth=2,
)
temp_frame.pack(pady=20)
temp_label = tkinter.Label(
    temp_frame,
    text="Temperature",
).pack()
temp_entry = tkinter.Entry(
    temp_frame,
    textvariable=temp_var,
    width=4,
    justify=tkinter.CENTER,
).pack()
temp_slider = tkinter.Scale(
    temp_frame,
    variable=temp_var,
    from_=-50,
    to=50,
    orient=tkinter.HORIZONTAL,
    showvalue=False,
).pack()
for child in temp_frame.winfo_children():
    child.pack_configure(padx=5, pady=5)

output_frame = tkinter.Frame(
    control_frame_buttons,
    relief=tkinter.GROOVE,
    pady=10,
    borderwidth=4,
)
output_frame.pack(pady=20)
output_label = tkinter.Label(
    output_frame,
    text="Output",
).pack()
output_text = tkinter.Label(
    output_frame,
    textvariable=output_var,
).pack()
for child in output_frame.winfo_children():
    child.pack_configure(padx=5, pady=5)

button_calculate = tkinter.Button(
    control_frame_buttons,
    text="Calculate",
    command=update_system,
).pack(side=tkinter.BOTTOM, pady=20)

button_quit = tkinter.Button(
    control_frame_buttons,
    text="Quit",
    command=root.destroy,
).pack(side=tkinter.BOTTOM, pady=20)

tkinter.mainloop()
