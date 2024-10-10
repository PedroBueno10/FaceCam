import cv2
import face_recognition
import os
import customtkinter as ctk
from PIL import Image, ImageTk
import random

photo_dir = 'fotos'
if not os.path.exists(photo_dir):
    os.makedirs(photo_dir)

known_face_encodings = []
known_face_names = []

def load_known_faces():
    """Carregar todas as fotos do diretório 'fotos' e obter as codificações faciais."""
    known_face_encodings.clear()
    known_face_names.clear()
    for filename in os.listdir(photo_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            path = os.path.join(photo_dir, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                face_encoding = encodings[0]
                known_face_encodings.append(face_encoding)
                known_face_names.append(os.path.splitext(filename)[0])

def identify_faces(frame):
    """Identifica rostos no frame e retorna os nomes das pessoas com informações adicionais."""
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    
    results = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Pessoa não cadastrada"
        person_number = random.randint(1, 100) 
        random_number = random.randint(1000, 9999)
        
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        results.append(f"{name} N° {person_number} - {random_number}")
    
    return face_locations, results

def show_frame():
    """Captura e exibe um frame da câmera."""
    ret, frame = video_capture.read()
    frame = cv2.flip(frame, 1)
    
    if ret:
        small_frame = cv2.resize(frame, (640, 480))  
        img = Image.fromarray(cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB))
        img_tk = ImageTk.PhotoImage(image=img)
    
        canvas.imgtk = img_tk
        canvas.create_image(0, 0, image=img_tk, anchor='nw')
      
        canvas.after(10, show_frame)

def identify():
    """Identifica rostos ao clicar no botão e exibe o resultado na tela."""
    ret, frame = video_capture.read()
    if ret:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        face_locations, names = identify_faces(small_frame)
        
        if len(face_locations) > 0:
            message = ", ".join(names) 
        else:
            message = "Nenhum rosto detectado para identificar."
        
        display_message(message)

def display_message(message):
    """Exibe uma mensagem na tela por um curto período de tempo."""
    message_label.configure(text=message)
    result_frame.place(relx=0.5, rely=0.85, anchor='center')
    root.after(3000, hide_message)  

def hide_message():
    """Esconde o frame de mensagem."""
    result_frame.place_forget()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") 

root = ctk.CTk()
root.title("Reconhecimento Facial")
root.geometry("640x600")

canvas = ctk.CTkCanvas(root, width=640, height=480)
canvas.pack(pady=(10, 20))

button = ctk.CTkButton(root, text="✅", command=identify, width=0, height=0)
button.pack(pady=(10, 0))

result_frame = ctk.CTkFrame(root, width=350, height=100, corner_radius=10, fg_color="#c9c9c9")
result_frame.pack_propagate(False)

message_label = ctk.CTkLabel(result_frame, text="", font=("Arial", 14), text_color="white")
message_label.pack(expand=True, fill='both', padx=5, pady=20)

video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("Erro ao abrir a webcam.")
    exit()

load_known_faces()
show_frame()
root.mainloop()
video_capture.release()
cv2.destroyAllWindows()
