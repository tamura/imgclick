#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import cv2  
import numpy
import re


helptext = '''

-std: stdin
press Q: quit xy find
press G: NG


#cat m.jpg | tesseract -l jpn_best stdin stdout
#cat m.jpg | tesseract -l jpn_best stdin stdout
#cat test.png | convert - -crop 50x50+20+20 - |  tesseract -l jpn_best stdin stdout

convert logo: png:- |./xyimg-20200215.py >pipe_point
convert ll.pdf[0] png:- |./xyimg-20200215.py - --point > pipe_points


tail -f log.log |xargs -I {} notify-send {}

tail -f log.log |xargs -I {} sh -c "cat test.png | convert - -crop {} - |  tesseract -l jpn_best stdin stdout" 

tail -f log.log |xargs -I {} sh -c "cat ll.png | convert - -crop {} - |  tesseract -l eng stdin stdout" 


convert -density 150 -quality 100 ll.pdf[0]  png:- |./xyimg-20200215.py - >log.log



convert -density 150 -quality 100 ll.pdf[0]  png:- |./xyimg-20200215.py -stdin -file=test.jpg >> log.log

pdftoppm -png whys-poignant-guide-to-ruby.pdf -f 1 -l 4 xx



#ファイルを指定して使うときは -file　をつかう。
ls xx-0*.png |xargs -I {} sh -c '../xyimg-20200215.py -file={}'



#stdinname 標準入力するとき、出力にファイル名のようなものをいれたいとき（いれなくてもいい。）あるとawkでつかいやすい

    $ cat xx-003.png |../xyimg-20200215.py -stdin -stdinname=3_no_xy
    あとで
    -stdin=3_no_xy みたいにしていできるようにする

    出力の一行一行のまえに、　3_no_xy  123x345+50+50 　形式TSVで出力したい時  


'''




def draw_square(event,x,y,flags,param):
    global ix,iy,drawing,mode
    global square
    global xy
    # global img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),1)
            cv2.imshow("img", img)


    elif event == cv2.EVENT_LBUTTONUP:
        if (ix==x and iy==y):
            points.append([x,y])
            xy+=str(x)
            xy+=" "
            xy+=str(y)
            xy+=" "
            cv2.circle(img, (x, y), 3, (0, 0, 255), -1)


        drawing = False
        cv2.rectangle(img,(ix,iy),(x,y),(255,0,0),1)
        cv2.imshow("img", img)
        square.append([[ix,iy],[x,y]])

        # if("--realtime" in sys.argv):
        print('{width}x{height}+{px}+{py}'.format(
            px = ix if ix<=x else x,
            py = iy if iy<=y else y,
            width = abs(ix-x), height=abs(iy-y)
            ))
        sys.stdout.flush()






drawing = False 
xy=""
square=[]
points=[]

filename=""
stdinname=""


if ("-h" in sys.argv):
	print(helptext)
	exit()


for i in sys.argv:
    if(re.compile("-file=.*.[png,jpg]").match(str(i))):
        filename = i.split("=")[1]


for i in sys.argv:
    if(re.compile("-stdinname=.*").match(str(i))):
        stdinname = i.split("=")[1]



if ("-stdin" in sys.argv):
# if sys.argv[1]=="-":
    # stdin = sys.stdin.read()
    stdin = sys.stdin.buffer.read()
    array = numpy.frombuffer(stdin, dtype='uint8')
    img = cv2.imdecode(array, 1)
elif(filename!=""):
    img = cv2.imread(filename, 1)
else:
    print("no input data")
    exit;





if(filename!=""):
    print("============="+filename+"=============") 
elif(stdinname):
    print("============= STDIN ==="+stdinname+"============") 



# if("img" not in locals()):
#     print i.split("=")[1]
#     img = cv2.imread(i.split("=")[1], 1)




cv2.namedWindow("img", cv2.WINDOW_NORMAL)



# try:
#     if sys.argv[2]=="--point":
#         cv2.setMouseCallback("img", mouse_event)
# except:

cv2.setMouseCallback("img", draw_square)
    


cv2.imshow("img", img)





		
while (True):
    if cv2.waitKey(115) & 0xFF == ord("q"):
        break
    if cv2.waitKey(115) & 0xFF == ord("u"):
        print("---- NG -"+filename+"=----")
        print("============="+filename+"=============")
        img = cv2.imdecode(array, 1)
        cv2.imshow("img", img)





# try:
#     if sys.argv[2]=="--point":
#         print(xy)


# except:

#     for sq in square:
#         print('{width}x{height}+{px}+{py}'.format(
#             px = sq[0][0] if sq[0][0]<=sq[1][0] else sq[1][0],
#             py = sq[0][1] if sq[0][1]<=sq[1][1] else sq[1][1],
#             width = abs(sq[0][0]-sq[1][0]), height=abs(sq[0][1]-sq[1][1])
#             ))



# if ("-points" in sys.argv):
#     print(xy)


print("---- END -"+filename+"=----")

print(points)
print(xy)

print("---")



for sq in square:
    # print filename
        # filename = filename+' - ' if (filename in locals()) else "",
    # if(filename in locals()):
    print (filename)

    print('{width}x{height}+{px}+{py}'.format(
        px = sq[0][0] if sq[0][0]<=sq[1][0] else sq[1][0],
        py = sq[0][1] if sq[0][1]<=sq[1][1] else sq[1][1],
        width = abs(sq[0][0]-sq[1][0]), height=abs(sq[0][1]-sq[1][1])
        ))


print("----================----")


# def mouse_event(event, x, y, flags, param):

#     global xy
#     global square
#     global points

#     if event == cv2.EVENT_LBUTTONUP:
#         cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
#         xy+=str(x)
#         xy+=" "
#         xy+=str(y)
#         xy+=" "
#         square.append([x,y])
#         print(str(x)+' '+str(y))
#         # sys.stdout(str(x)+' '+str(y))
#         sys.stdout.flush()

#         