#! /usr/bin/env python3
import sys
#import argparse
from typing import Tuple
import imageio
import numpy
import matplotlib.pyplot as plt


def make_quads(im: imageio.core.util.Array) -> str:
    
    if im.shape[0] != im.shape[1]:
        sys.exit('Image is not square with power of 2 elements in each dimension')
        
    # If this quad has a single value, handle it
    if numpy.amax(im) == numpy.amin(im):
        return str(int(numpy.amax(im)))
    
    # Otherwise handle four pieces
    result ="("
    halfsize = int(im.shape[0]/2)
    
    result += make_quads(im[0:halfsize,0:halfsize]) + ","
    result += make_quads(im[0:halfsize,halfsize:]) + ","
    result += make_quads(im[halfsize:,halfsize:]) + ","
    result += make_quads(im[halfsize:,0:halfsize]) + ")"
        
    return result
    


def generate_quadtree(png_image: str) -> None:
    
    im = imageio.imread(png_image)
    print(im.shape)
    bigsize = int(2**numpy.ceil(numpy.log2(max(im.shape))))
    bim = numpy.zeros((bigsize,bigsize))
    
    #print(im.shape)
 
#    bigsize = (8)
#    bim = numpy.zeros((bigsize,bigsize))
#    lim=[[1,1,0,0,0,0,0,0],
#         [1,1,1,0,0,0,0,0],
#         [0,0,1,1,0,0,0,0],
#         [1,1,0,0,0,0,0,0],
#         [0,0,0,0,1,1,1,1],
#         [0,0,0,0,1,1,1,1],
#         [0,0,0,0,0,0,0,0],
#         [1,1,1,1,1,1,1,1]]
#    
#    im = numpy.zeros((8,8))
#    for i in range(8):
#        for j in range(8):
#            im[i,j] = lim[i][j]
            
    starti = int((bigsize - im.shape[0])/2)
    startj = int((bigsize - im.shape[1])/2)
    
    # binarize image
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if len(im.shape) > 2:
                bim[i+starti,j+startj] = 1.0*(sum(im[i,j,0:])>0)
            else:
                bim[i+starti,j+startj] = 1.0*(im[i,j]>0)
            
    # show binary imnage
    plt.imshow(bim)
    outfd = open('/Users/jnw/git/SwampCTF/swctf_misc1/quadt.out','w')
    outfd.write(make_quads(bim))

    
    # inject image into the smallest 2^n X 2^n image it will fit in
    

def quad_check(quad_string: str, ptr: int, check: str) -> None:
    if quad_string[ptr] != check:
        sys.exit('Bad character %s at offset %d' % (quad_string[ptr],ptr))
  

def show(quad_string,ptr):
    
    print('** %s' % quad_string[ptr:ptr+5])

def quad_reshape(im: imageio.core.util.Array, rightsize: int) -> imageio.core.util.Array:
    repeat_factor = int(rightsize/im.shape[0])
    newim = numpy.zeros((rightsize,rightsize))

    for i in range(im.shape[0]):
        index1 = 0
        for x in range(repeat_factor):
            for j in range (im.shape[1]):
                index2 = 0
                for k in range(repeat_factor):
                    newim[repeat_factor*i+index1,repeat_factor*j+index2] = im[i,j]
                    index2 += 1
            index1 += 1
    return newim
    
def make_image_parts(quad_string: str, ptr: int, checkim: imageio.core.util.Array) -> Tuple[imageio.core.util.Array, int]:
    
    #print('starting at %d'%(ptr))
    # if one part, handle it
    if quad_string[ptr] != '(':
        #if checkim[0,0] != int(quad_string[ptr]):
        #    print('Got a mismatch at %d: %s' % ptr, quad_string[ptr])
        return (int(quad_string[ptr])*numpy.ones((1,1),int),ptr+1)
        
    # otherwise handle the four parrts

    newsize = int(checkim.shape[0]/2)
    
    
    #try:
    quad_check(quad_string,ptr,'(')
    
    ptr += 1
    #show(quad_string,ptr)
    (ar1,ptr) = make_image_parts(quad_string, ptr,checkim[0:newsize,0:newsize])
    quad_check(quad_string, ptr, ',')

    ptr += 1
    #show(quad_string,ptr)
    (ar2, ptr) = make_image_parts(quad_string, ptr, checkim[0:newsize,newsize:])
    quad_check(quad_string, ptr, ',')
    

    ptr += 1
    #show(quad_string,ptr)
    (ar3, ptr) = make_image_parts(quad_string, ptr, checkim[newsize:,newsize:])
    quad_check(quad_string, ptr, ',')
    
    ptr += 1
    #show(quad_string,ptr)
    (ar4, ptr) = make_image_parts(quad_string, ptr, checkim[newsize:,0:newsize])
    quad_check(quad_string, ptr, ')')
    ptr += 1
    #except:
    #    print('Failed at character %d' % (ptr))
    #    print('Context: %s' % (quad_string[ptr-10:ptr+10]))
    #    print('                   ^')
    #    sys.exit()
    
    rightshape = tuple(map(max,ar1.shape,ar2.shape,ar3.shape,ar4.shape))
    
    rightsize = rightshape[0]
    if ar1.shape != rightshape:
        if numpy.amax(ar1) != numpy.amin(ar1):            
            #print('ar1 at %d, value was %s desired shape: %s' % (ptr,str(ar1), str(rightshape)))
            ar1 = quad_reshape(ar1,rightsize)
            #print('ar1 %s' % (str(ar1)))          
        else:
            ar1 = ar1[0,0]*numpy.ones(rightshape,int)
    if ar2.shape != rightshape:
        if numpy.amax(ar2) != numpy.amin(ar2):
            ar2 = quad_reshape(ar2,rightsize)
        else:            
            ar2 = ar2[0,0]*numpy.ones(rightshape,int)
    if ar3.shape != rightshape:
        if numpy.amax(ar3) != numpy.amin(ar3):
            ar3 = quad_reshape(ar3,rightsize)
        else:
            ar3 = ar3[0,0]*numpy.ones(rightshape,int)
    if ar4.shape != rightshape:
        if numpy.amax(ar4) != numpy.amin(ar4):
            ar4 = quad_reshape(ar4,rightsize)
        else:
            ar4= ar4[0,0]*numpy.ones(rightshape,int)
        
    #print(numpy.multiply(2,rightshape))

    try:
        img_array = numpy.zeros(numpy.multiply(2,rightshape),int)
        img_array[0:rightsize,0:rightsize] = ar1
        img_array[0:rightsize,rightsize:] = ar2
        img_array[rightsize:,rightsize:] = ar3
        img_array[rightsize:,0:rightsize] = ar4
    except:
        print('Something failed in making array result')
        print('Array shapes: %s, %s, %s, %s, %s' % (str(img_array.shape),str(ar1.shape),str(ar2.shape),str(ar3.shape),str(ar4.shape)))  

    
    return(img_array,ptr)
        
    
def generate_image(quad_file: str, imgfile: str) -> None:
    imfile = open(quad_file)
    check_im = imageio.imread(imgfile)    
    
    quad_string = imfile.read()
    (img_array,bogus) = make_image_parts(quad_string,0,check_im)
    
    print("Showing image")
    plt.imshow(1.0*img_array)
    plt.show()
    print("after show image")
    

    
    
    

#def main():
#   parser = argparse.ArgumentParser(description="Create or display quadtree version of an image")
#
#    parser.add_argument('--image',
#                        help='png image file')
#    parser.add_argument('--quadtree',
#                        help='quad tree file')
#
#    args = parser.parse_args()
#
#    if args.image and args.quadtree:
#        sys.exit('Specify only one of --image or --quadtree')
#
#    if args.image:
#        generate_quadtree(args.image)
#    elif args.quadtree:
#        generate_image(args.quadtree)
#    else:
#        parser.print_help()
#        
#    exit

#generate_quadtree("/Users/jnw/git/SwampCTF/swctf_misc1/flag1.pbm")
#generate_image("/Users/jnw/git/SwampCTF/swctf_misc1/quadt.out", "/Users/jnw/git/SwampCTF/swctf_misc1/flag1.pbm")
generate_image("../quadt.out", "./square-png-30.png")

#if __name__ == '__main__':
#    main()
