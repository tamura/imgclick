#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import cv2  
import numpy
import re

# sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
# sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)
# sys.stdin = os.fdopen(sys.stdin.fileno(), 'r', buffering=1)


# filename....?
# import os
# print(os.readlink('/proc/self/fd/0'))


helptext = '''

-std: stdin
press Q: quit xy find
press U: UNDO


#cat m.jpg | tesseract -l jpn_best stdin stdout

#cat test.png | convert - -crop 50x50+20+20 | tesseract -l jpn_best stdin stdout


convert ll.pdf[0] png:- |./xyimg-20200215.py > pipe_points


tail -f log.log |xargs -I {} notify-send {}

tail -f log.log |xargs -I {} sh -c "cat test.png | convert - -crop {} - |  tesseract -l jpn_best stdin stdout" 

tail -f log.log |xargs -I {} sh -c "cat ll.png | convert - -crop {} - |  tesseract -l eng stdin stdout" 


convert -density 150 -quality 100 ll.pdf[0]  png:- |./xyimg-20200215.py - >log.log


convert -density 150 -quality 100 ll.pdf[0]  png:- |./xyimg-20200215.py -stdin -file=test.jpg >> log.log

pdftoppm -png whys-poignant-guide-to-ruby.pdf -f 1 -l 4 xx


cat test.png |./xyimg-20200215.py --format='notify-send "{x}+{y}"' |sh


#ファイルを指定して使うときは -file　をつかう。
ls xx-0*.png |xargs -I {} sh -c '../xyimg-20200215.py -file={}'



#stdinname 標準入力するとき、出力にファイル名のようなものをいれたいとき（いれなくてもいい。）あるとawkでつかいやすい

    $ cat xx-003.png |../xyimg-20200215.py -stdin -stdinname=3_no_xy
    あとで
    -stdin=3_no_xy みたいにしていできるようにする

    出力の一行一行のまえに、　3_no_xy  123x345+50+50 　形式TSVで出力したい時  


#ls test.*|xargs -I {} bash -c "./xyimg-20200215.py {}"


'''




def draw_square(event,px,py,flags,param):
    global ix,iy,drawing,mode
    global square
    global xy
    global outputformat
    # global img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = px,py

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(img,(ix,iy),(px,py),(0,255,0),1)
            cv2.imshow("img", img)


    elif event == cv2.EVENT_LBUTTONUP:
        if (ix==px and iy==py):
            points.append([px,py])
            xy+=str(px)
            xy+=" "
            xy+=str(py)
            xy+=" "
            cv2.circle(img, (px, py), 3, (0, 0, 255), -1)


        drawing = False
        cv2.rectangle(img,(ix,iy),(px,py),(255,0,0),1)
        cv2.imshow("img", img)
        square.append([[ix,iy],[px,py]])

        print(outputformat.format(
            x = ix if ix<=px else px,
            y = iy if iy<=py else py,
            w = abs(ix-px), h=abs(iy-py)
            ))
        sys.stdout.flush()






drawing = False 
xy=""
square=[]
points=[]



name=""
filename=""
stdinname=""





import argparse






# def main():
#     parser = argparse.ArgumentParser()


# if __name__ == "__main__":
#     main()






parser = argparse.ArgumentParser(description="draw squares or points on the image with mouse, to get its coordinate X and Y posioton and width, height and so on",usage=helptext)

parser.add_argument('filename', nargs='?')

parser.add_argument('--name',help="Specify name of the group you make, if you like.")


parser.add_argument('--only-result',help="じょじょにprintしないでいい")


parser.add_argument('--whxy',help="format: imagemagick coordinates (width)x(height)+X+Y")

parser.add_argument('--format',help="{w} {h} {x1} {y1} {x2} {x2}")

# parser.add_argument('--resize',help="return resized numbers ")





args = parser.parse_args()

if args.filename is None:
    try:
        unicode # python2
        stdin = sys.stdin.read()
    except:
        stdin = sys.stdin.buffer.read()

    array = numpy.frombuffer(stdin, dtype='uint8')
    # array = numpy.frombuffer(stdin, dtype='uint8')
    img = cv2.imdecode(array, 1)

else:
    # with open(args.filename) as f:
    # process(f)
    img = cv2.imread(args.filename, 1)
    name = args.filename;


if args.name is None:
    None
else:
    name = args.name
    print(name)

if args.format is None:
    outputformat="{w}+{h}+{x}+{y}"
else:
    outputformat=args.format


if(name!=""):
    print("============="+name+"=============") 
elif(stdinname):
    print("============= STDIN ==="+name+"============") 




cv2.namedWindow("img", cv2.WINDOW_NORMAL)

cv2.setMouseCallback("img", draw_square)

cv2.imshow("img", img)




		
while (True):
    if cv2.waitKey(115) & 0xFF == ord("q"):
        break
    if cv2.waitKey(115) & 0xFF == ord("u"):
        print("---- NG -"+name+"=----")
        print("============="+name+"=============")

        if args.filename is None:
            img = cv2.imdecode(array, 1)
        else:
            img = cv2.imread(args.filename, 1)

        cv2.imshow("img", img)






print("---- END -"+name+"=----")

print(points)
print(xy)

print("---")



for sq in square:
    # print name
        # name = name+' - ' if (name in locals()) else "",
    # if(name in locals()):
    print (name)

    print(outputformat.format(
        x = sq[0][0] if sq[0][0]<=sq[1][0] else sq[1][0],
        y = sq[0][1] if sq[0][1]<=sq[1][1] else sq[1][1],
        w = abs(sq[0][0]-sq[1][0]), h=abs(sq[0][1]-sq[1][1])
        ))


print("----================----")

