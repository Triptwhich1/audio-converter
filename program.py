import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import os

# Function to add a prefix to the files, e.g. siren, and the .wav exported would be Dsiren01 etc.
def get_prefix(): 
    global prefix_text
    prefix_text = input_entry.get()
    if 1 <= len(prefix_text) <=6:
        print(f'Filename will be {prefix_text}01, Is this correct?')
    else:
        print("Please Choose a Suitable Name")
        prefix_text = ""

# Function to process a list of audio files
def process_audio_files(input_files, output_folder):
    try:
        os.makedirs(output_folder, exist_ok=True)

        for index, input_file in enumerate(input_files, start=1):
            print(f"Processing file: {input_file}")

            audio = AudioSegment.from_file(input_file)

            audio = audio.set_channels(1) # Converts sterio to mono

            audio = audio.set_sample_width(2) # Set the sample width to 16 bits (PCM)

            if audio.frame_rate != 48000: # Set the sample rate to 48000Hz (if not already)
                audio = audio.set_frame_rate(48000)

            output_filename = f"{prefix_text}{index:02}.wav" # Define file name
            output_file = os.path.join(output_folder, output_filename)
            print(f"Saving processed file: {output_file}")

            audio.export(output_file, format="wav") # Export the processed audio to the output file as WAV

        print("Processing complete!")
    except Exception as e:
        print(f"Error processing audio: {e}")

# Function to handle the input file selection
def select_input_files():
    input_files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.wav")])
    input_listbox.delete(0, tk.END)

    for file in input_files:
        input_listbox.insert(tk.END, file)

# Function to handle the output folder selection
def select_output_folder():
    output_folder = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_folder)

# Function to process the audio when the "Process" button is clicked
def process_button_click():
    input_files = input_listbox.get(0, tk.END)
    output_folder = output_entry.get()

    if input_files and output_folder:
        process_audio_files(input_files, output_folder)

# Create the main application window
app = tk.Tk()
app.title("Audio File Processor")

# Prefix selection
input_entry_label = tk.Label(app, text="Enter Prefix: \n *Must be 1-6 Characters")
input_entry_label.pack()

input_entry = tk.Entry(app, text="")
input_entry.pack()

input_entry_button = tk.Button(app, text="Select", command= get_prefix)
input_entry_button.pack()

# Input file selection
input_label = tk.Label(app, text="Select Input Files:")
input_label.pack()

input_listbox = tk.Listbox(app, selectmode=tk.MULTIPLE, width=40, height=5)
input_listbox.pack()

input_button = tk.Button(app, text="Browse", command=select_input_files)
input_button.pack()

# Output folder selection
output_label = tk.Label(app, text="Select Output Folder:")
output_label.pack()

output_entry = tk.Entry(app, width=40)
output_entry.pack()

output_button = tk.Button(app, text="Browse", command=select_output_folder)
output_button.pack()

# Process button
process_button = tk.Button(app, text="Process", command=process_button_click)
process_button.pack()

app.mainloop()
