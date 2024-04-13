import cv2
import os



if __name__ == "__main__":
    baseDir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    hand_recognition_runner = HandRecognitionRunner(baseDir, ifDebug=True)
    hand_recognition_runner.recognize_hand('hand.jpg')
    cv2.waitKey(0)
    cv2.destroyAllWindows()