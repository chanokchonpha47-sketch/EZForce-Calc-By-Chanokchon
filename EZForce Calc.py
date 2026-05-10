from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import math
import force_calc as fc

window=Tk()
window.title('EZForce Calc')
window.geometry('400x640')

BG_COLOR = "#0f172a"
CARD_COLOR = "#111827"
ACCENT = "#22c55e"
TEXT = "#e5e7eb"

window.configure(bg=BG_COLOR)
style = ttk.Style()
style.theme_use('clam')
style.configure("TEntry",
                fieldbackground="#1f2937",
                foreground=TEXT,
                borderwidth=0,
                padding=6)

style.configure("TCombobox",
                fieldbackground="#1f2937",
                background="#1f2937",
                foreground=TEXT,
                padding=5)

style.configure("Green.TButton",
                font=("Fredoka Light", 10),
                foreground="#ffffff",
                background="#228B22",
                borderwidth=0,
                padding=(14, 8)
                )
style.configure("Red.TButton",
                font=("Fredoka Light", 10),
                foreground="#ffffff",
                background="#B22222",
                borderwidth=0,
                padding=(4, 2)
                )
style.configure("Yellow.TButton",
                font=("Fredoka Light", 10),
                foreground="black",
                background="#FFFF33",
                borderwidth=0,
                padding=(12, 6)
                )

style.map("Green.TButton",
          background=[
              ("active", "#6B8E23"),
              ("pressed", "#6B8E23")
          ],
          foreground=[
              ("active", "white")
          ]
          )
style.map("Red.TButton",
          background=[
              ("active", "#FA8072"),
              ("pressed", "#FA8072")
          ],
          foreground=[
              ("active", "white")
          ]
          )
style.map("Yellow.TButton",
          background=[
              ("active", "#FFFF66"),
              ("pressed", "#FFFF66")
          ],
          foreground=[
              ("active", "#2F4F4F")
          ]
          )

font_main = ("Fredoka Light", 14)
font_title = ("Dynapuff", 18)

canvas = Canvas(window, width=400, height=300, bg="white")
canvas.grid(row=1, column=0, columnspan=10)

canvas.config(bg="#020617", highlightthickness=0)
origin_x = 200
origin_y = 150
canvas.create_line(0, origin_y, 400, origin_y, dash=(2,2))
canvas.create_line(origin_x, 0, origin_x, 300, dash=(2,2))

direction_map = {
    "Quadrant I (+,+)": (1, 1),
    "Quadrant II (-,+)": (-1, 1),
    "Quadrant III (-,-)": (-1, -1),
    "Quadrant IV (+,-)": (1, -1)
}
lbl_name = Label(window, text="EZForce Calculator",
                 font=font_title, bg=BG_COLOR, fg=ACCENT)
lbl_name.grid(row=0, column=0, columnspan=10, pady=10)
lbl_Force = Label(window, text="Force(N)")
lbl_Force.grid(row=2, column=0)
lbl_angle = Label(window, text="θ(°)")
lbl_angle.grid(row=2, column=3)

lbl_Force.config(font=font_main, bg=BG_COLOR, fg=TEXT)
lbl_angle.config(font=font_main, bg=BG_COLOR, fg=TEXT)
lbl_show = Label(window, text="Fx = ...")
lbl_show.grid(row=5, column=3)
lbl_show1 = Label(window, text="Fy = ...")
lbl_show1.grid(row=7, column=3)
lbl_show2 = Label(window, text="Fx = ...")
lbl_show2.grid(row=6, column=3)
lbl_show3 = Label(window, text="Fy = ...")
lbl_show3.grid(row=8, column=3)

lbl_show.config(font=font_main, bg=BG_COLOR, fg=ACCENT)
lbl_show1.config(font=font_main, bg=BG_COLOR, fg=ACCENT)
lbl_show2.config(font=font_main, bg=BG_COLOR, fg="#60a5fa")
lbl_show3.config(font=font_main, bg=BG_COLOR, fg="#f59e0b")

txtEntry = ttk.Entry(window, width=10, font=("Fredoka Light", 12))
txtEntry.grid(row=3, column=0)
txtEntry1 = ttk.Entry(window, width=10, font=("Fredoka Light", 12))
txtEntry1.grid(row=3, column=3)
lbl_Direction = Label(window, text="Select Force Quadrant")
lbl_Direction.grid(row=4, column=0)
lbl_Direction.config(font=font_main, bg=BG_COLOR, fg=TEXT)

combo = ttk.Combobox(window)
combo['values']=tuple(direction_map.keys())
combo.current(0)
combo.grid(row=5, column=0)
def clicked():
    if txtEntry.get() == "" or txtEntry1.get() == "":
        messagebox.showwarning("Warning", "กรุณากรอกข้อมูลให้ครบ")
        return
    try:
        F = float(txtEntry.get())
        angle = float(txtEntry1.get())
    except ValueError:
        messagebox.showerror("Error", "กรุณากรอกเป็นตัวเลข")
        return

    direction = combo.get()
    Fx, Fy = fc.calculate_force(F, angle, direction, direction_map)
    lbl_show2.config(text=f"Fx = {Fx:.2f} N")
    lbl_show3.config(text=f"Fy = {Fy:.2f} N")
    fc.draw_force(canvas, origin_x, origin_y, Fx, Fy, angle)
    lbl_show.config(text=f"Fx = {F}cos{angle}°")
    lbl_show1.config(text=f"Fy = {F}sin{angle}°")

def reset_force():
    txtEntry.delete(0, END)
    txtEntry1.delete(0, END)
    combo.current(0)
    lbl_show.config(text="Fx = ...")
    lbl_show1.config(text="Fy = ...")
    canvas.delete("force")

ttk.Button(window, text="Calculate",
           style="Green.TButton",
           command=clicked).grid(row=7, column=0)
ttk.Button(window, text="Reset",
           style="Red.TButton",
           command=reset_force).grid(row=9, column=0)
window.bind('<Return>', lambda event: clicked())


def open_R_window():
    R_window = Toplevel(window)
    R_window.title("Resultant Force (R)")
    R_window.geometry("380x530")
    R_window.configure(bg=BG_COLOR)
    Label(R_window, text="Resultant Force Calculator",
          font=font_title, bg=BG_COLOR, fg=ACCENT).pack(pady=10)
    frame = Frame(R_window, bg=CARD_COLOR)
    frame.pack(pady=10, padx=20, fill="both", expand=True)
    Label(frame, text="ΣFx", font=font_main,
          bg=CARD_COLOR, fg=TEXT).grid(row=0, column=0)
    txtFx = ttk.Entry(frame, width=10)
    txtFx.grid(row=0, column=1)
    Label(frame, text="ΣFy", font=font_main,
          bg=CARD_COLOR, fg=TEXT).grid(row=1, column=0)
    txtFy = ttk.Entry(frame, width=10)
    txtFy.grid(row=1, column=1)

    lbl_R1 = Label(frame, text="R = √(ΣFx² + ΣFy²)",font=font_main, bg=CARD_COLOR, fg=ACCENT)
    lbl_R1.grid(row=3, column=0, columnspan=2)
    lbl_R2 = Label(frame, text="R = ...", font=font_main, bg=CARD_COLOR, fg=ACCENT)
    lbl_R2.grid(row=4, column=0, columnspan=2)
    lbl_R3 = Label(frame, text="R = ...", font=font_main, bg=CARD_COLOR, fg="cyan")
    lbl_R3.grid(row=5, column=0, columnspan=2)

    lbl_angle1 = Label(frame,
                   text="θ = tan⁻¹(ΣFy / ΣFx)",
                   font=font_main,
                   bg=CARD_COLOR,
                   fg="#facc15")
    lbl_angle1.grid(row=6, column=0, columnspan=2)
    lbl_angle2 = Label(frame,
                   text="θ = ...",
                   font=font_main,
                   bg=CARD_COLOR,
                   fg="#facc15")
    lbl_angle2.grid(row=7, column=0, columnspan=2)

    canvas_popup = Canvas(frame, width=300, height=200,
                          bg="#020617", highlightthickness=0)
    canvas_popup.grid(row=8, column=0, columnspan=2)


    def calculate_popup():
        try:
            Fx = float(txtFx.get())
            Fy = float(txtFy.get())
        except:
            messagebox.showerror("Error", "กรอกตัวเลข")
            return
        canvas_popup.delete("all")
        R = fc.calculate_R(Fx, Fy)
        theta = math.degrees(math.atan2(Fy, Fx))
        lbl_R3.config(text=f"R = {R:.2f} N")
        lbl_angle2.config(text=f"θ = {theta:.2f}°")

        res = f"R = √(({Fx})² + ({Fy})²)"
        lbl_R2.config(text=res)

        max_size = max(abs(Fx), abs(Fy))
        if max_size == 0:
            scale = 1
        else:
            scale = 120 / max_size

        drawFx = Fx * scale
        drawFy = Fy * scale
        origin_x_popup = 150 - (drawFx / 2)
        origin_y_popup = 100 + (drawFy / 2)

        canvas_popup.create_line(origin_x_popup, origin_y_popup,
                         origin_x_popup + drawFx, origin_y_popup,
                         arrow=LAST, fill="green")
        canvas_popup.create_text(origin_x_popup + drawFx/2,
                                 origin_y_popup + 15,
                                 text=f"Fx = {Fx:.2f}",
                                 fill="green",
                                 font=("Prompt", 10)
                                 )

        canvas_popup.create_line(origin_x_popup + drawFx, origin_y_popup,
                         origin_x_popup + drawFx, origin_y_popup - drawFy,
                         arrow=LAST, fill="orange")
        canvas_popup.create_text(origin_x_popup + drawFx + 40,
                                 origin_y_popup - drawFy/2,
                                 text=f"Fy = {Fy:.2f}",
                                 fill="orange",
                                 font=("Prompt", 10)
                                 )

        canvas_popup.create_line(origin_x_popup, origin_y_popup,
                         origin_x_popup + drawFx,
                         origin_y_popup - drawFy,
                         arrow=LAST, fill="cyan", width=2)
        canvas_popup.create_text(origin_x_popup + drawFx/2 - 40,
                                 origin_y_popup - drawFy/2 - 25,
                                 text=f"R = {R:.2f}",
                                 fill="cyan",
                                 font=("Prompt", 10, "bold")
                                 )

        canvas_popup.create_text(origin_x_popup + 40,
                                 origin_y_popup - 20,
                                 text=f"θ = {theta:.1f}°",
                                 fill="yellow",
                                 font=("Prompt", 10, "bold")
                                 )

    ttk.Button(frame, text="Calculate",

               style="Green.TButton",

               command=calculate_popup).grid(row=2, column=0, columnspan=2)

ttk.Button(window, text="Open R Calculator",
           style="Yellow.TButton",
           command=open_R_window).grid(row=10, column=3, columnspan=4, pady=10)

window.mainloop()
