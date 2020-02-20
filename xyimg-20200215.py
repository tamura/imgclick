#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import cv2  
import numpy
import re


helptext = '''

-std: stdin
press Q: quit xy find
press U: UNDO


#cat m.jpg | tesseract -l jpn_best stdin stdout

#cat test.png | convert - -crop 50x50+20+20 - |  tesseract -l jpn_best stdin stdout


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



name=""
filename=""
stdinname=""


# if ("-h" in sys.argv):
# 	print(helptext)
# 	exit()


# for i in sys.argv:
#     if(re.compile("-file=.*.[png,jpg]").match(str(i))):
#         filename = i.split("=")[1]


for i in sys.argv:
    if(re.compile("-stdinname=.*").match(str(i))):
        stdinname = i.split("=")[1]



# if ("-stdin" in sys.argv):
# # if sys.argv[1]=="-":
#     stdin = sys.stdin.read()
#     # stdin = sys.stdin.buffer.read()
#     array = numpy.frombuffer(stdin, dtype='uint8')
#     img = cv2.imdecode(array, 1)
# elif(filename!=""):
#     img = cv2.imread(filename, 1)
# else:
#     print("no input data")
#     exit;




import argparse

parser = argparse.ArgumentParser(description="joooooin",usage=helptext)

parser.add_argument('filename', nargs='?')

parser.add_argument('--name',help="name of your input")

args = parser.parse_args()

if args.filename is None:
    # process(sys.stdin)
    stdin = sys.stdin.read()
    # stdin = sys.stdin.buffer.read()
    array = numpy.frombuffer(stdin, dtype='uint8')
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




# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('filename', nargs='?')
#     args = parser.parse_args()

#     if args.filename is None:
#         process(sys.stdin)
#     else:
#         with open(args.filename) as f:
#             process(f)

# if __name__ == "__main__":
#     main()








if(name!=""):
    print("============="+name+"=============") 
elif(stdinname):
    print("============= STDIN ==="+name+"============") 



# if("img" not in locals()):
#     print i.split("=")[1]
#     img = cv2.imread(i.split("=")[1], 1)




cv2.namedWindow("img", cv2.WINDOW_NORMAL)


cv2.setMouseCallback("img", draw_square)
    

cv2.imshow("img", img)





		
while (True):
    if cv2.waitKey(115) & 0xFF == ord("q"):
        break
    if cv2.waitKey(115) & 0xFF == ord("u"):
        print("---- NG -"+name+"=----")
        print("============="+name+"=============")
        img = cv2.imdecode(array, 1)
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

    print('{width}x{height}+{px}+{py}'.format(
        px = sq[0][0] if sq[0][0]<=sq[1][0] else sq[1][0],
        py = sq[0][1] if sq[0][1]<=sq[1][1] else sq[1][1],
        width = abs(sq[0][0]-sq[1][0]), height=abs(sq[0][1]-sq[1][1])
        ))


print("----================----")

