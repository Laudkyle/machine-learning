from tkinter import filedialog
import os
import cv2
import pickle


# step 2
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")


cap = cv2.VideoCapture(0)
labels = {"person_name": 1}
with open("pickles/face-labels.pickle", 'rb') as f:
	og_labels = pickle.load(f)
	labels = {v:k for k,v in og_labels.items()}

while(True):
    ret, frame = cap.read()
    # STEP 3
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)

    # Getting the faces
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        id_, conf = recognizer.predict(roi_gray)
        if conf >= 75 and conf <= 100:
            font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
            name = labels[id_]
            color = (255, 255, 0)
            stroke = 1
            if conf >= 95 and conf <= 100:
                img_item = f'images/{name.replace("-", " ")}/my_image{x-y+w*h}.png'
                path = f'images/{name.replace("-", " ")}'
                files = len(os.listdir(path))
                if files <= 1000:
                    {cv2.imwrite(img_item, roi_color)}
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
        # Adding the r
        # ectangular box
        color = (225, 0, 0)
        stroke = 1
        end_cordx = x + w
        end_cordy = y + h
        cv2.rectangle(frame, (x, y), (end_cordx, end_cordy), color, stroke)

    cv2.imshow('Frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
