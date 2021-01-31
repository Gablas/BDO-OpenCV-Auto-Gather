import os
import cv2 as cv


def org_img():
    dir = os.listdir("./debug")
    for img in dir:
        cvimg = cv.imread("./debug/"+img)
        cv.imshow("weed", cv.resize(cvimg, (cvimg.shape[1]//2, cvimg.shape[0]//2)))
        key = cv.waitKey(0)
        if(key == ord("d")):
            os.replace("./debug/"+img, "./discard/"+img)
        elif(key == ord("p")):
            os.replace("./debug/"+img, "./positive/"+img)
        elif(key == ord("n")):
            os.replace("./debug/"+img, "./neg/"+img)
        elif(key == ord("e")):
            break


def generate_negative_description_file():
    # open the output file for writing. will overwrite all existing data in there
    with open('neg.txt', 'w') as f:
        # loop over all the filenames
        for filename in os.listdir('neg'):
            f.write('neg/' + filename + '\n')


def make_imgs_smaller():
    dirs = ["./positive", "./neg"]
    for dir in dirs:
        imgs = os.listdir(dir)
        for img in imgs:
            image = cv.imread(dir + "/" + img)
            if(image.shape[1] == 3840):
                print("resizing image of shape " + str(image.shape[1]))
                image = cv.resize(image, (image.shape[1]//2, image.shape[0]//2))
                cv.imwrite(dir + "/" + img, image)




