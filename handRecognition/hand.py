import mediapipe
import cv2
import os

class HandRecognitionRunner():
    def __init__(self, baseDir, ifDebug = True):
        self.baseDir = baseDir
        self.selfBaseDir = baseDir + '/handRecognition/'
        self.ifDebug = ifDebug
    
    def recognize_hand(self, img):
        os.chdir(self.baseDir)
        drawingModule = mediapipe.solutions.drawing_utils
        handsModule = mediapipe.solutions.hands

        hands = handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)
        img = cv2.imread(img)
        frame = cv2.resize(img, (640, 480))
        results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


        print(len(results.multi_hand_landmarks))
        if len(results.multi_hand_landmarks) == 2:
            print(results.multi_hand_landmarks[0].landmark[0])
            print(results.multi_hand_landmarks[1].landmark[0])
            mid_x = (results.multi_hand_landmarks[0].landmark[0].x + results.multi_hand_landmarks[1].landmark[0].x) / 2
            print(mid_x)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # print(hand_landmarks)
                drawingModule.draw_landmarks(frame, hand_landmarks, handsModule.HAND_CONNECTIONS)
        # cv2.imwrite('hand.jpg', img)

        cv2.imshow("Frame", frame);
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        return

if __name__ == "__main__":
    baseDir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    hand_recognition_runner = HandRecognitionRunner(baseDir, ifDebug=True)
    hand_recognition_runner.recognize_hand('hand.jpg')
    cv2.waitKey(0)
    cv2.destroyAllWindows()