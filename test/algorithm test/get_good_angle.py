from models import *
from utils import *
from utils.net import *


def main():
    camera = Camera(PORT, LIFECAM_3000)
    ok,frame = camera.read()



if __name__ == '__main__':
    main()
