import cv2
import face_recognition
import os

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
    """Identifica rostos no frame e retorna os nomes das pessoas."""
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    
    names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Pessoa não cadastrada"
        
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        
        names.append(name)
    
    return face_locations, names

video_capture = cv2.VideoCapture(0)



if not video_capture.isOpened():
    print("Erro ao abrir a webcam.")
    exit()

load_known_faces()

while True:
    try:
        ret, frame = video_capture.read()
        frame = cv2.flip(frame,1)
        
        if not ret:
            print("Erro ao capturar vídeo.")
            break
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        cv2.imshow('Video', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('g'):
            print("Identificando...")
            face_locations, names = identify_faces(small_frame)

            if len(face_locations) > 0:
                for name in names:
                    print(name) 
            else:
                print("Nenhum rosto detectado para identificar.")
        elif key == ord('q'):
            break

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        continue

video_capture.release()
cv2.destroyAllWindows()
