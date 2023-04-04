import cloudinary.uploader
import cloudinary.utils
#import winsound
from flask import Flask, Response, render_template
import cv2
# from playsound import playsound
app = Flask(__name__)
import requests
import twilio
from twilio.rest import Client
cloudinary.config(
  cloud_name = "dymtzczdp",
  api_key = "278794557333869",
  api_secret = "wOtWveO_aixYQh89yRo7ZY6XOpw"
)


alarm_duration=5
frequency=2500
duration=1000
# Load the face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')



# reign of interest
top_left = (400, 50)
bottom_right = (800, 550)

# Open camera
cap = cv2.VideoCapture(0)

frequency = 2500
duration = 1000
# Set the alarm duration in seconds
alarm_duration = 5

# twilio credtial
account_sid="AC535ba97d039a980d56d7a80fb2d894b5"
auth_token="ce25f78334ed574c4aaef9ee858fccf7"

client=Client(account_sid,auth_token)
# sending the image to user
to_whatsapp_number='whatsapp:+918791391135'                         
from_whatsapp_number='whatsapp:+14155238886'

#           ---- FUNCTION---
def generate_frames():
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Draw rectangle for area of interest
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 3)

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            
            # Save the image
            if x > top_left[0] and y > top_left[1] and x + w < bottom_right[0] and y + h < bottom_right[1]:
                filename = "intruder.jpg"
                cv2.imwrite(filename, frame)
                # twilio sms alert
                message=client.messages.create(
                body="Alert Intrusion detected at your premise",
                from_="+19523730493",
                to="+918791391135"
                )

            
                print("INTRUDER ALERT")

                # winsound.Beep(frequency, duration)
                # alarm_duration_countdown = alarm_duration * 100
                # while alarm_duration_countdown > 0:
                #     winsound.Beep(frequency, duration)
                #     alarm_duration_countdown -= 1
                # playsound('Beep.mp3')
                # # sending the image to user by devansh
                mes=client.messages.create(
                    from_='whatsapp:+14155238886',
                    body='Intrusion detected using python',
                    to=to_whatsapp_number
                    
                )
                # # image url
                image_url='http://127.0.0.1:5000/intruder.jpg'
                Response=requests.get(image_url)
                
                upload_result = cloudinary.uploader.upload("intruder.jpg")
                public_id = upload_result['public_id']
                secure_url, options = cloudinary.utils.cloudinary_url(public_id, secure=True)

                message=client.messages.create(
                media_url=secure_url,
                from_=from_whatsapp_number,
                to=to_whatsapp_number
                )



                client.messages.create(
                    from_='whatsapp:+14155238886',
                    body='theif',
                    media_url=Response.url,
                    to=to_whatsapp_number

                )
        # Return the frame to the webpage
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)