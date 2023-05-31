import tkinter
import numpy as np
# Shows plots inside tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

import skfuzzy as fuzz
from skfuzzy import control as ctrl


if __name__ == "__main__":
    root = tkinter.Tk()
    root.wm_title("Fuzzy Logic")

    level = ctrl.Antecedent(np.arange(0, 11, 1), 'Water Level')
    water_temperature = ctrl.Antecedent(
        np.arange(0, 136, 1), 
        'Water Temperature',
    )
    heater_value = ctrl.Consequent(np.arange(0, 11, 1), 'Heater Value')

    level['Very Low'] = fuzz.trimf(
        level.universe,
        [0, 1, 2]
    )
    level['Low'] = fuzz.trimf(
        level.universe,
        [1.5, 3, 4.5],
    )
    level['Medium'] = fuzz.trimf(
        level.universe,
        [4, 5, 6.5],
    )
    level['High'] = fuzz.trimf(
        level.universe,
        [6, 7, 8.5],
    )
    level['Very High'] = fuzz.trimf(
        level.universe,
        [8, 9, 10],
    )
    water_temperature['Very Cool'] = fuzz.trimf(
        water_temperature.universe,
        [0, 15, 30]
    )
    water_temperature['Cool'] = fuzz.trimf(
        water_temperature.universe,
        [22.5, 45, 67.5],
    )
    water_temperature['Medium'] = fuzz.trimf(
        water_temperature.universe,
        [60, 75, 97.5],
    )
    water_temperature['Hot'] = fuzz.trimf(
        water_temperature.universe,
        [90, 105, 127.5],
    )
    water_temperature['Very Hot'] = fuzz.trimf(
        water_temperature.universe,
        [120, 135, 135],
    )
    heater_value['Very Little'] = fuzz.trimf(
        heater_value.universe,
        [0, 1, 2],
    )
    heater_value['Little'] = fuzz.trimf(
        heater_value.universe,
        [1.5, 3, 4.5],
    )
    heater_value['Medium'] = fuzz.trimf(
        heater_value.universe,
        [4, 5, 6.5],
    )
    heater_value['High'] = fuzz.trimf(
        heater_value.universe,
        [6, 7, 8.5],
    )
    heater_value['A Lot'] = fuzz.trimf(
        heater_value.universe,
        [8, 9, 10],
    )

# Fuzzy rules
    water_control_system = ctrl.ControlSystem([
        ctrl.Rule(
            level['Very Low'] & water_temperature['Very Cool'], 
            heater_value['Medium'],
        ),
        ctrl.Rule(
            level['Very Low'] & water_temperature['Cool'],
            heater_value['Little'],
        ),
        ctrl.Rule(
            level['Very Low'] & water_temperature['Medium'],
            heater_value['Medium'],
        ),
        ctrl.Rule(
            level['Very Low'] & water_temperature['Hot'],
            heater_value['Very Little'],
        ),
        ctrl.Rule(
            level['Low'] & water_temperature['Very Cool'],
            heater_value['High'],
        ),
        ctrl.Rule(
            level['Low'] & water_temperature['Cool'],
            heater_value['Little'],
        ),
        ctrl.Rule(
            level['Low'] & water_temperature['Medium'],
            heater_value['High'],
        ),
        ctrl.Rule(
            level['Low'] & water_temperature['Hot'],
            heater_value['Very Little'],
        ),
        ctrl.Rule(
            level['Medium'] & water_temperature['Very Cool'],
            heater_value['High'],
        ),
        ctrl.Rule(
            level['Medium'] & water_temperature['Cool'],
            heater_value['Medium'],
        ),
        ctrl.Rule(
            level['Medium'] & water_temperature['Medium'],
            heater_value['High'],
        ),
        ctrl.Rule(
            level['Medium'] & water_temperature['Hot'],
            heater_value['Little'],
        ),
        ctrl.Rule(
            level['High'] & water_temperature['Very Cool'],
            heater_value['A Lot'],
        ),
        ctrl.Rule(
            level['High'] & water_temperature['Cool'],
            heater_value['High'],
        ),
        ctrl.Rule(
            level['High'] & water_temperature['Medium'],
            heater_value['A Lot'],
        ),
        ctrl.Rule(
            level['High'] & water_temperature['Hot'],
            heater_value['Little'],
        ),
        ctrl.Rule(
            level['High'] & water_temperature['Very Hot'],
            heater_value['Very Little'],
        ),
        ctrl.Rule(
            level['Very High'] & water_temperature['Very Cool'],
            heater_value['A Lot'],
        ),
        ctrl.Rule(
            level['Very High'] & water_temperature['Cool'],
            heater_value['A Lot'],
        ),
        ctrl.Rule(
            level['Very High'] & water_temperature['Medium'],
            heater_value['A Lot'],
        ),
        ctrl.Rule(
            level['Very High'] & water_temperature['Hot'],
            heater_value['Medium'],
        ),
        ctrl.Rule(
            level['Very High'] & water_temperature['Very Hot'],
            heater_value['Very Little'],
        ),
    ])

# Compute first so that when the frame is initialized,
# there is a value
    water_control = ctrl.ControlSystemSimulation(water_control_system)
    water_control.inputs({
        'Water Level': 0,
        'Water Temperature': 0,
    })
    water_control.compute()

    level_var = tkinter.DoubleVar()
    rate_var = tkinter.DoubleVar()
    output_var = tkinter.DoubleVar()
    output_formatted = tkinter.StringVar()

    fig, _ = heater_value.get_view(sim=water_control)

# Define tkinter widgets

    canvas_frame = tkinter.Frame(root)

    canvas_frame.pack(
        side=tkinter.LEFT,
        fill=tkinter.BOTH,
        expand=1,
    )

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()

    toolbar = NavigationToolbar2Tk(canvas, canvas_frame, pack_toolbar=False)
    toolbar.update()

    def update_system():
        global canvas
        global toolbar

        water_control.inputs({
            'Water Level': level_var.get(),
            'Water Temperature': rate_var.get(),
        })
        water_control.compute()
        if not 'Heater Value' in water_control.output: return
        output_var.set(water_control.output['Heater Value'])
        output_formatted.set(f"{output_var.get():9.2f}")

        # So far, only way to make it refresh
        # due to the unique construction of this widget
        canvas.get_tk_widget().destroy()
        fig, _ = heater_value.get_view(sim=water_control)
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()

        toolbar.destroy()
        toolbar = NavigationToolbar2Tk(canvas, canvas_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(
            side=tkinter.BOTTOM,
            fill=tkinter.X,
        )
        canvas.get_tk_widget().pack(
            side=tkinter.RIGHT,
            fill=tkinter.BOTH,
            expand=True,
        )


    toolbar.pack(
        side=tkinter.BOTTOM,
        fill=tkinter.X,
    )

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
        text="Water Level",
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
        from_=0,
        to=10,
        tickinterval=0.1,
        orient=tkinter.HORIZONTAL,
        showvalue=False,
    ).pack()
    for child in level_frame.winfo_children():
        child.pack_configure(padx=5, pady=5)

    water_temperature_frame = tkinter.Frame(
        control_frame_buttons,
        relief=tkinter.GROOVE,
        pady=20,
        borderwidth=2,
    )
    water_temperature_frame.pack(pady=20)
    water_temperature_label = tkinter.Label(
        water_temperature_frame,
        text="Water Temperature",
    ).pack()
    water_temperature_entry = tkinter.Entry(
        water_temperature_frame,
        textvariable=rate_var,
        width=4,
        justify=tkinter.CENTER,
    ).pack()
    water_temperature_slider = tkinter.Scale(
        water_temperature_frame,
        variable=rate_var,
        from_=0,
        to=135,
        tickinterval=0.1,
        orient=tkinter.HORIZONTAL,
        showvalue=False,
    ).pack()
    for child in water_temperature_frame.winfo_children():
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
        text="Output: Heater Value",
    ).pack()
    output_text = tkinter.Label(
        output_frame,
        textvariable=output_formatted,
        justify=tkinter.CENTER,
    ).pack()
    for child in output_frame.winfo_children():
        child.pack_configure(padx=5, pady=5)

    button_quit = tkinter.Button(
        control_frame_buttons,
        text="Quit",
        command=root.destroy,
    ).pack(side=tkinter.BOTTOM, pady=20)

    button_calculate = tkinter.Button(
        control_frame_buttons,
        text="Calculate",
        command=update_system,
    ).pack(side=tkinter.BOTTOM, pady=20)

    tkinter.mainloop()
