import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
from PIL import Image, ImageTk
import pyttsx3

translator = Translator()
engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def translate_text():
    source_text = source_text_widget.get("1.0", tk.END).strip()
    target_language = language_var.get()

    if not source_text:
        messagebox.showwarning("Warning", "Please enter text to translate")
        return

    if not target_language:
        messagebox.showwarning("Warning", "Please select a target language")
        return

    try:
        target_language_code = [code for code, lang in LANGUAGES.items() if lang == target_language][0]
        translation = translator.translate(source_text, dest=target_language_code)
        
        translation_window = tk.Toplevel(root)
        translation_window.title("Translation")
        translation_window.geometry("400x250")
        translation_window.configure(bg='#005F69')

        translation_label = tk.Label(translation_window, text="Translation:", bg='#987B71', fg='white', font=font)
        translation_label.pack(pady=5)

        translation_text = tk.Text(translation_window, height=5, width=40, font=font)
        translation_text.pack(pady=10)
        translation_text.insert(tk.END, translation.text)
        translation_text.config(state=tk.DISABLED)

        def copy_translation():
            root.clipboard_clear()
            root.clipboard_append(translation_text.get("1.0", tk.END))

        copy_button = tk.Button(translation_window, text="Copy Translation", command=copy_translation, bg='#088F8F', font=font)
        copy_button.pack(pady=5)

        def speak_translation():
            speak_text(translation.text)

        speak_button = tk.Button(translation_window, text="Speak Translation", command=speak_translation, bg='#088F8F', font=font)
        speak_button.pack(pady=5)

    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Translator App")
root.geometry("500x450")
root.configure(bg='#0047AB')
root.resizable(False, False)

image = Image.open("translation.jpg")
image = image.resize((200, 200), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

image_label = tk.Label(root, image=photo)
image_label.pack(pady=10)

font = ("Lexend", 12)

source_text_widget = tk.Text(root, height=5, width=50, font=font, bg="#A7C7E7")
source_text_widget.pack(pady=10)

language_frame = tk.Frame(root)
language_frame.pack(pady=10)

language_label = tk.Label(language_frame, text="Select Target Language: ", bg='#0047AB', fg='white', font=font)
language_label.pack(side=tk.LEFT)

language_var = tk.StringVar()
language_combo = ttk.Combobox(language_frame, textvariable=language_var, font=font)
language_combo['values'] = list(LANGUAGES.values())
language_combo.pack(side=tk.LEFT)

style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox")

translate_button = tk.Button(root, text="Translate", command=translate_text, bg='#088F8F', font=font)
translate_button.pack(pady=10)

root.mainloop()
