import tkinter as tk
from tkinter import messagebox
import serial
import time

# Serial configuration
def send_command(command):
    try:
        ser.write(command.encode())  # Send command without \r\n
        log_text.insert(tk.END, f"Sent: {command}\n")
        log_text.see(tk.END)
        time.sleep(1)
    except Exception as e:
        messagebox.showerror("Serial Error", f"Cannot send data: {e}")

# Command sending function
def send_sms():
    phone_suffix = entry_phone.get()
    mode = entry_mode.get()
    
    if not phone_suffix.isdigit() or len(phone_suffix) != 9:
        messagebox.showerror("Input Error", "Phone number must be exactly 9 digits!")
        return
    
    phone_number = f"+84{phone_suffix}"
    
    commands = [
        f"admin {phone_number}",
        f"setsms {phone_number}",
        f"setcall1 {phone_number}",
        f"setcall2 {phone_number}",
        f"setcall3 {phone_number}",
        "setsignal 02",
        f"setmode {mode}",
        "save and reboot"  # Added info command

    ]
    
    for cmd in commands:
        send_command(cmd)
    
    messagebox.showinfo("Completed", "All commands sent successfully!")

# Reset function
def reset_factory():
    send_command("factory")
    messagebox.showinfo("Reset", "Factory reset command sent!")

# Serial connection
def connect_serial():
    global ser
    try:
        port = entry_port.get()
        ser = serial.Serial(port=port, baudrate=115200, timeout=1)
        messagebox.showinfo("Connection", f"Connected to {port}")
    except Exception as e:
        messagebox.showerror("Serial Error", f"Cannot open port {port}: {e}")

# Tkinter GUI
root = tk.Tk()
root.title("Serial Command Sender")
root.geometry("400x350")

# Serial port input
frame1 = tk.Frame(root)
frame1.pack(pady=5)
tk.Label(frame1, text="Serial Port:").pack(side=tk.LEFT)
entry_port = tk.Entry(frame1, width=10)
entry_port.pack(side=tk.LEFT)
entry_port.insert(0, "COM8")
tk.Button(frame1, text="Connect", command=connect_serial).pack(side=tk.LEFT)

# Phone number input
frame2 = tk.Frame(root)
frame2.pack(pady=5)
tk.Label(frame2, text="Phone Number (9 digits):").pack(side=tk.LEFT)
entry_phone = tk.Entry(frame2, width=12)
entry_phone.pack(side=tk.LEFT)

# Mode input
frame3 = tk.Frame(root)
frame3.pack(pady=5)
tk.Label(frame3, text="Mode:").pack(side=tk.LEFT)
entry_mode = tk.Entry(frame3, width=5)
entry_mode.pack(side=tk.LEFT)

# Send command button
btn_send = tk.Button(root, text="Send Command", command=send_sms)
btn_send.pack(pady=5)

# Reset button
btn_reset = tk.Button(root, text="Factory Reset", command=reset_factory, bg="red", fg="white")
btn_reset.pack(pady=5)

# Log display
log_text = tk.Text(root, height=6, width=50)
log_text.pack()

root.mainloop()