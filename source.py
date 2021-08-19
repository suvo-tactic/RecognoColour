import cv2 as cv
import numpy as np
import pandas as pd 


img = cv.imread("temp.jpeg")
def rescaleFrame(frame, scale=.4):
    width = int(frame.shape[1]*scale)
    height=int(frame.shape[0]*scale)

    dimensions =(width,height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

rez = rescaleFrame(img)

# cv.imshow("Color",rez)
# cv.waitKey(0)

index =["color","color_name","hex","R","G","B"]
df = pd.read_csv('colors.csv',names=index,header=None)


clicked = False
r=g=b=xpos=ypos=0

def click(event, x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = rez[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
cv.namedWindow('World-of-colors')
cv.setMouseCallback('World-of-colors',click)


def colName(R,G,B):
    min = 10000
    for i in range(len(df)):
        d = abs(R- int(df.loc[i,"R"])) + abs(G- int(df.loc[i,"G"]))+ abs(B- int(df.loc[i,"B"]))
        if(d<=min):
            min = d
            cname = df.loc[i,"color_name"]
    return cname


while(1):
    cv.imshow("World-of-colors",rez)
    if(clicked):
        cv.rectangle(rez,(20,20), (750,60), (b,g,r), -1)
        
        text = colName(r,g,b) + ' R='+ str(r) + ' G='+ str(g) + ' B='+ str(b)

        cv.putText(rez, text,(50,50),2,0.8,(255,255,255),2,cv.LINE_AA)

        if(r+g+b>=480):
            cv.putText(rez, text,(50,50),2,0.8,(0,0,0),2,cv.LINE_AA)

        clicked=False

    if cv.waitKey(20) & 0xFF==27:
        break
cv.destroyAllWindows()