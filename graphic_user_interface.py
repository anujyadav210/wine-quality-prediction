import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import numpy as np
import joblib

# Load model
try:
    model = joblib.load("best_wine_quality_model.pkl")
except FileNotFoundError:
    messagebox.showerror("Error", "Model file not found.")
    exit()

# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Main window
root = ctk.CTk()
root.title("🍷 Wine Quality Predictor")
root.geometry("900x650")

# === Background Image using CTkImage ===
#bg_image = Image.open("wine-quality.jpg")
#bg_image_resized = bg_image.resize((900, 650), Image.LANCZOS)
#ctk_bg_image = ctk.CTkImage(light_image=bg_image_resized, dark_image=bg_image_resized, size=(900, 650))
#bg_label = ctk.CTkLabel(root, image=ctk_bg_image, text="")
#bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# === Overlay Frame ===
overlay = ctk.CTkFrame(root, fg_color=("gray20", "gray10"), corner_radius=25)
overlay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.8)

# Title
title = ctk.CTkLabel(
    overlay,
    text="🍇 Wine Quality Predictor",
    font=ctk.CTkFont("Georgia", 28, weight="bold"),
    text_color="#FFFFFF"
)
title.pack(pady=15)

# Input section
input_frame = ctk.CTkFrame(overlay, fg_color="transparent")
input_frame.pack(pady=10)

features = [
    "Fixed Acidity", "Volatile Acidity", "Citric Acid",
    "Chlorides", "Free Sulfur Dioxide", "Sulphates", "Alcohol"
]
entries = []

for i, feature in enumerate(features):
    row = ctk.CTkFrame(input_frame, fg_color="transparent")
    row.pack(pady=6, padx=10, fill="x")

    label = ctk.CTkLabel(row, text=feature + ":", width=180, anchor="w", font=ctk.CTkFont(size=14))
    label.pack(side="left", padx=10)

    entry = ctk.CTkEntry(row, width=180)
    entry.pack(side="right", padx=10)

    def bind_focus(e, idx=i):
        if idx + 1 < len(entries):
            entries[idx + 1].focus()
        else:
            entries[idx].focus()

    entry.bind("<Return>", bind_focus)
    entries.append(entry)

# Prediction result
result_label = ctk.CTkLabel(
    overlay,
    text="",
    font=ctk.CTkFont("Georgia", 18, weight="bold"),
    text_color="#FF6B6B"
)
result_label.pack(pady=10)

# Predict function
def predict_quality():
    try:
        features_input = [float(entry.get()) for entry in entries]
        features_np = np.array(features_input).reshape(1, -1)
        prediction = model.predict(features_np)[0]
        result_label.configure(text=f"✨ Predicted Wine Quality Score: {prediction}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

# Clear function
def clear_fields():
    for entry in entries:
        entry.delete(0, 'end')
    result_label.configure(text="")

# Buttons
button_frame = ctk.CTkFrame(overlay, fg_color="transparent")
button_frame.pack(pady=20)

predict_btn = ctk.CTkButton(
    button_frame, text="🍷 Predict", command=predict_quality,
    width=150, height=40, font=ctk.CTkFont(size=14, weight="bold")
)
predict_btn.grid(row=0, column=0, padx=20)

clear_btn = ctk.CTkButton(
    button_frame, text="🧹 Clear", command=clear_fields,
    width=150, height=40, font=ctk.CTkFont(size=14, weight="bold"), fg_color="#5D6D7E", hover_color="#34495E"
)
clear_btn.grid(row=0, column=1, padx=20)

# Make background image responsive to resizing
def on_resize(event):
    new_width = event.width
    new_height = event.height
    resized = bg_image.resize((new_width, new_height), Image.LANCZOS)
    new_ctk_img = ctk.CTkImage(light_image=resized, dark_image=resized, size=(new_width, new_height))
    bg_label.configure(image=new_ctk_img)
    bg_label.image = new_ctk_img  # prevent garbage collection

root.bind("<Configure>", on_resize)

# Launch
root.mainloop()
