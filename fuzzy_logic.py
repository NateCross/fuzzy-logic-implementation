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

    level = ctrl.Antecedent(np.arange(0, 100, 1), 'Level')
    rate_of_change = ctrl.Antecedent(
        np.arange(-100, 100, 1), 
        'Rate of Change',
    )
    valve = ctrl.Consequent(np.arange(0, 100, 1), 'State of Valve')

    level.automf(names=[
        "Very Low", 
        "Low", 
        "Medium", 
        "High", 
        "Very High",
    ])
    rate_of_change.automf(names=[
        "Negative", 
        "Neutral", 
        "Positive",
    ])
    valve.automf(names=[
        "Sudden Close",
        "Open Slow",
        "Open Medium",
        "Open Fast",
        "Sudden Open",
    ])

# Fuzzy rules
    water_control_system = ctrl.ControlSystem([
        ctrl.Rule(
            level['Very High'], 
            valve['Sudden Close'],
        ),
        ctrl.Rule(
            level['High'] & rate_of_change['Positive'],
            valve['Open Medium'],
        ),
        ctrl.Rule(
            level['High'] & rate_of_change['Neutral'],
            valve['Sudden Close'],
        ),
        ctrl.Rule(
            level['High'] & rate_of_change['Negative'],
            valve['Sudden Close'],
        ),
        ctrl.Rule(
            level['Medium'],
            valve['Open Medium'],
        ),
        ctrl.Rule(
            level['Low'],
            valve['Open Fast'],
        ),
        ctrl.Rule(
            level['Very Low'],
            valve['Sudden Open'],
        ),
    ])

# Compute first so that when the frame is initialized,
# there is a value
    water_control = ctrl.ControlSystemSimulation(water_control_system)
    water_control.inputs({
        'Level': 0,
        'Rate of Change': 0,
    })
    water_control.compute()

    level_var = tkinter.DoubleVar()
    rate_var = tkinter.DoubleVar()
    output_var = tkinter.DoubleVar()
    output_formatted = tkinter.StringVar()

    fig, _ = valve.get_view(sim=water_control)

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
            'Level': level_var.get(),
            'Rate of Change': rate_var.get(),
        })
        water_control.compute()
        output_var.set(water_control.output['State of Valve'])
        output_formatted.set(f"{output_var.get():9.2f}")

        # So far, only way to make it refresh
        # due to the unique construction of this widget
        canvas.get_tk_widget().destroy()
        fig, _ = valve.get_view(sim=water_control)
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()

        # toolbar.update()
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
        from_=0,
        to=100,
        orient=tkinter.HORIZONTAL,
        showvalue=False,
    ).pack()
    for child in level_frame.winfo_children():
        child.pack_configure(padx=5, pady=5)

    rate_frame = tkinter.Frame(
        control_frame_buttons,
        relief=tkinter.GROOVE,
        pady=20,
        borderwidth=2,
    )
    rate_frame.pack(pady=20)
    rate_label = tkinter.Label(
        rate_frame,
        text="Rate of Change",
    ).pack()
    rate_entry = tkinter.Entry(
        rate_frame,
        textvariable=rate_var,
        width=4,
        justify=tkinter.CENTER,
    ).pack()
    rate_slider = tkinter.Scale(
        rate_frame,
        variable=rate_var,
        from_=-100,
        to=100,
        orient=tkinter.HORIZONTAL,
        showvalue=False,
    ).pack()
    for child in rate_frame.winfo_children():
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
        text="Output: State of Valve",
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
