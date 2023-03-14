import cv2
import numpy as np

cap = cv2.VideoCapture(0)

perspective = np.array([[0, 0], [30, 30], [60, 30], [0, 30]], dtype=np.float32)

persp = np.array([[0, 0], [640, 0], [0, 480], [640, 480]], dtype=np.float32)
mouseX1, mouseY1, mouseX2, mouseY2 = 0, 0, 0, 0
flag = True
cnt = 0


def draw_circle(event, x, y, flags, param):
    global flag, cnt
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        perspective[cnt] = [x, y]
        flag = False
        cnt += 1
        if cnt > 3:
            cnt = 0


cv2.namedWindow('IMG')
cv2.setMouseCallback('IMG', draw_circle)

while cv2.waitKey(1) != 27:
    _, img = cap.read()
    # img = cv2.imread("Road.png")
    w, h, t = img.shape
    M = cv2.getPerspectiveTransform(perspective, persp)
    result = cv2.warpPerspective(img, M, (h, w))
    cv2.imshow("IMG", img)
    gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(result, contours, -1, (255, 0, 0), 3, cv2.LINE_AA, hierarchy, 1)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    point1 = []
    points2 = []
    if contours:
        for i in contours:
            if cv2.contourArea(i) > 500:
                M = cv2.moments(i)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(result, (cX, cY), 7, (255, 255, 0), -1)
                if not point1:
                    point1 = cX
                else:
                    points2.append([cX])
                (x, y, w, h) = cv2.boundingRect(i)
                cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if point1 and points2:
        point2 = int(np.mean(points2, axis=0)[0])
        #print(point1 - point2 - 540)
        cv2.circle(result, (point1, 200), 7, (255, 0, 255), -1)
        cv2.circle(result, (point2, 200), 7, (255, 0, 255), -1)
    cv2.imshow("BIN", binary)
    cv2.imshow("RESULT", result)
