from models import *
from utils import *
from vision import *
from drawings import *
import winsound

def main():
    #print "init"
    camera = Camera(0, LIFECAM_STUDIO)
    time = 0
    tracking_circles = []
    while True:
        time += 1
        ok, frame = camera.read()
        thr = threshold_fuel(frame)
        cv2.imshow('hello i is vision', thr)
        circles = find_fuel_circles(frame)
        circles_locations = find_fuels(frame, camera.data)
        trash_location = find_trash(frame, camera.data)
        trash_location += 0.20*trash_location/np.linalg.norm(trash_location) # center
        trash_location[1] -= 0.45
        for i, c in enumerate(circles):
            cv2.circle(frame, (int(c[0][0]), int(c[0][1])), int(c[1]), (0, 255, 0), 2)
            cv2.circle(frame, (int(c[0][0]), int(c[0][1])), 2, (0, 0, 255), 2)
        thr = threshold_trash(frame)
        cnts = sorted_contours(thr)
        rects = contours_to_rects_sorted(cnts)
        if len(rects) > 0:
            rtag = np.array(rects[0]).astype(int)
            cv2.rectangle(frame, (int(rtag[0]), int(rtag[1])), (int(rtag[0]+rtag[2]), int(rtag[1] + rtag[3])), (255, 0, 0), 2)

        cv2.circle(frame, (frame.shape[1] // 2, frame.shape[0] // 2), 2, (255, 0, 0), 2)

        cv2.imshow('hello i is also vision', frame)

        for i in circles_locations:
            exists = False
            for ind, j in enumerate(tracking_circles):
                if np.linalg.norm(i - j[0]) < 0.2 and time - j[1] < 10:
                    #print "resetting ball"
                    #print str([i, time]) + " -> " + str(j)
                    #print "\r\n"
                    tracking_circles[ind] = [i, time]
                    exists = True
                    break
            if np.linalg.norm(i - trash_location) < 0.3 and not exists:
                #print "adding ball"
                #print [i, time]
                tracking_circles.append([i, time])
        rem = []
        for i, c in enumerate(tracking_circles):
            if np.linalg.norm(c[0] - trash_location) > 0.3:
                #print "removing ball"
                #print c
                rem.append(i)
            elif time - c[1] > 20:
                print("ball in trash  -> %i" % time)
                winsound.PlaySound("ta da.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                rem.append(i)
        rem.reverse()
        for i in rem:
            del tracking_circles[i]

        #if time % 60 == 0:
            #print circles_locations
            #print trash_location

        k = cv2.waitKey(1) & 0xFF

        if k == ord('c') or k == ord('C'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
