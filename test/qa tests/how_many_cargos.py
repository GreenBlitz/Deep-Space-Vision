from utils import *
from models import *


def main():
    camera = Camera(PORT, LIFECAM_3000)
    while True:
        ok, frame = camera.read()
        circs = (threshold_cargo + find_contours + contours_to_circles)(frame)
        elps = (threshold_cargo + find_contours + contours_to_ellipses)(frame)
        for i in range(len(circs)):
            elp = elps[i]
            circ = circs[i]

            




if __name__ == '__main__':
    main()