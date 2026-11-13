import cv2,numpy as np
def cutout(c,vmax=168):
    h,w=c.shape[:2]
    mask=np.zeros((h,w),np.uint8);bg=np.zeros((1,65));fg=np.zeros((1,65))
    cv2.grabCut(c,mask,(20,4,w-40,h-8),bg,fg,6,cv2.GC_INIT_WITH_RECT)
    hsv=cv2.cvtColor(c,cv2.COLOR_BGR2HSV).astype(np.int32);H,S,V=hsv[...,0],hsv[...,1],hsv[...,2]
    g=cv2.cvtColor(c,cv2.COLOR_BGR2GRAY).astype(np.float32);mu=cv2.blur(g,(7,7));sd=np.sqrt(np.maximum(cv2.blur(g*g,(7,7))-mu*mu,0))
    halo=((H<=20)|(H>=150))&(V<vmax)&(S>60)&(S<175)&(sd<6.5)
    halo=cv2.morphologyEx(halo.astype(np.uint8),cv2.MORPH_OPEN,np.ones((5,5),np.uint8)).astype(bool)
    m2=mask.copy();m2[halo]=cv2.GC_BGD
    cv2.grabCut(c,m2,None,bg,fg,5,cv2.GC_INIT_WITH_MASK)
    m=((m2==1)|(m2==3)).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(m)
    if n>1:
        big=st[1:,cv2.CC_STAT_AREA];keep=1+np.where(big>=max(big)*0.05)[0];m=np.isin(lab,keep).astype(np.uint8)
    inv=(1-m).astype(np.uint8);n,lab,st,_=cv2.connectedComponentsWithStats(inv)
    for i in range(1,n):
        x,y,ww,hh,a=st[i]
        if x>0 and y>0 and x+ww<w and y+hh<h and a<400: m[lab==i]=1
    a=cv2.GaussianBlur(m.astype(np.float32),(3,3),0)
    return np.dstack([c,(np.clip(a,0,1)*255).astype(np.uint8)])
def white(o,col=(255,255,255)):
    a=o[...,3:]/255.;w=np.zeros(o[...,:3].shape)+np.array(col);return (o[...,:3]*a+w*(1-a)).astype(np.uint8)
if __name__=='__main__':
    outs=[]
    for f,(r,cc) in [('front.png',(0,0)),('front.png',(1,2)),('back.png',(0,1)),('poses.png',(0,2)),('poses.png',(1,0))]:
        im=cv2.imread(f);outs.append(white(cutout(im[r*512:(r+1)*512,cc*512:(cc+1)*512]),(120,200,140)))
    cv2.imwrite('t4w.png',np.hstack(outs))
