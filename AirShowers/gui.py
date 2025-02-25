#!/usr/bin/python

import tkinter as tk
from tkinter import messagebox

from call_airsim import *

###################################
def update_label():
    """Updates the label with the user's input."""
    text = entry.get()
    if text:
        label.config(text=f"Hello, {text}!")
    else:
        label.config(text="Please enter a name!")

###################################
def get_logE():
    """Retrieves the selected number from the Spinbox and shows it."""
    selected_logE = spinbox.get()
    # messagebox.showinfo("Selected log(E)", f"You selected: {selected_logE}")
    return selected_logE

###################################
def show_message():
    """Displays a message based on the toggle state."""
    if toggle_var.get():
        messagebox.showinfo("Info", "You have enabled the toggle!")
    else:
        messagebox.showwarning("Warning", "Toggle is OFF!")

###################################
def update_theme():
    """Switches between light and dark mode themes."""
    if theme_var.get() == "black":
        root.configure(bg="#2E2E2E")
        label.config(bg="#2E2E2E", fg="white")
    else:
        root.configure(bg="white")
        label.config(bg="white", fg="black")

###################################
def exit_app():
    """Closes the application."""
    root.destroy()


###################################
def run_app():
    """Closes the application."""
    selected_logE = get_logE()
    argv = [sys.argv[0]]
    argv.append(selected_logE)
    simulate(argv)
    return

    

###################################
###################################
###################################

def main(argv):
    """Main function to initialize the GUI."""
    global root, label, entry, spinbox, toggle_var, theme_var  # Make widgets accessible in functions

    root = tk.Tk()
    root.title("Enhanced GUI")
    root.geometry("400x400")
    root.configure(bg="black")  # Default light mode

    # Label
    label = tk.Label(root, text="Enter your name:", font=("Arial", 14), bg="white")
    label.pack(pady=5)

    # Entry field
    entry = tk.Entry(root, font=("Arial", 12))
    entry.insert(0, "Some value")  # Default value
    entry.pack(pady=5)

    # Frame for horizontal buttons
    button_frame = tk.Frame(root, bg="white")
    button_frame.pack(pady=5)

    # Buttons inside frame
    btn_update = tk.Button(button_frame, text="Greet Me", command=update_label)
    btn_update.pack(side="left", padx=5)

    btn_get_logE = tk.Button(button_frame, text="Show logE", command=get_logE)
    btn_get_logE.pack(side="left", padx=5)

    # Numeric Input (Spinbox)
    spinbox_label = tk.Label(root, text="Select logE:", font=("Arial", 12), bg="white")
    spinbox_label.pack(pady=5)

    spinbox = tk.Spinbox(root, from_=11, to=15, font=("Arial", 12), width=5)
    spinbox.pack(pady=5)

    # Toggle Checkbutton
    toggle_var = tk.BooleanVar(value=False)
    toggle_button = tk.Checkbutton(root, text="Enable Feature", variable=toggle_var, command=show_message)
    toggle_button.pack(pady=5)

    # Theme selection using Radiobuttons
    theme_var = tk.StringVar(value="light")  # Default theme
    rb_light = tk.Radiobutton(root, text="Light Mode", variable=theme_var, value="light", command=update_theme)
    rb_dark = tk.Radiobutton(root, text="Dark Mode", variable=theme_var, value="black", command=update_theme)

    rb_light.pack(pady=2)
    rb_dark.pack(pady=2)

    # Run Sim Button
    run_button = tk.Button(root, text="Simulate!", command=run_app, bg="red", fg="black")
    run_button.pack(pady=10)

    
    # Exit Button
    exit_button = tk.Button(root, text="Exit", command=exit_app, bg="red", fg="white")
    exit_button.pack(pady=10)

    # Run Tkinter event loop
    root.mainloop()


###################################
###################################
###################################

# Run the main function when the script is executed
if __name__ == "__main__":
    main(sys.argv)
    print(f'...Thanks for running {sys.argv[0]}')
    print('...Returning and kiling oneself!')
    print('...So long, and thanks for all the fish!')
    os.system('killall -9 airsim.py')
    
###################################
###################################
###################################
