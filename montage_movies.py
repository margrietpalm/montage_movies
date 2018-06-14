#!/usr/bin/env python
"""Combine multiple movies into one"""

import argparse
import sys
import os
import glob
import shutil
import future
from im2movie import makeMovie


__author__ = "Margriet Palm"
__copyright__ = "Copyright 2018"
__credits__ = "Margriet Palm"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Margriet Palm"

def parse_args():
    parser = argparse.ArgumentParser(description="Combine multiple movies into one using ImageMagick's montage and im2movie")
    parser.add_argument('-q','--quiet',dest="quiet",action="store_true",help="suppress output")
    parser.add_argument("-x","--ncol",type=int,dest="ncol",help="number of columns")
    parser.add_argument("-y","--nrow",type=int,dest="nrow",default=1,help="number of rows")
    parser.add_argument("--dx",dest="dcol",type=int,default=0,help="horizontal spacing")
    parser.add_argument("--dy",dest="drow",type=int,default=0,help="vertical spacing")
    parser.add_argument("--name",dest="name",default="combined",help="movie name")
    parser.add_argument("-f","--fps",dest="fps",type=float,default=1,help="frame rate")
    parser.add_argument("-v","--vqscale",dest="vqscale",type=int,default=12,help="quality, lower is better (but file size is larger)")
    parser.add_argument("-w","--win",dest="win",action="store_true",help="make windows compatible movie")
    parser.add_argument("--mp4",dest="tomp4",action="store_true",help="make mp4")
    parser.add_argument('movies', nargs='*',help="list of movies to combine")
    return parser.parse_args()


def montage_movies(movies,ncol,nrow,name,drow=0,dcol=0,fps=1,
                   win=False,vqscale=12,tomp4=False):
    """
    Args:
        movies: list of movies
        ncol: number of movies on the horizontal axis
        nrow: number of movies on the vertical axis
        name: movie name
        dcol: horizontal distance between movies
        drow: vertical distance between movies
        fps: frame rate
        win: make windows compatible movie
        tomp4: make mp4 movie
        vqscale: video quality
    """
    # 1) create temp folder
    tempdir = 'temp_montage/'
    if os.path.isdir(tempdir):
        sys.exit("Tried to create temporary directory '{}', but this directory already exists.".format(tempdir))
    os.mkdir(tempdir)
    # 2) For each movie:
    #   a. create subtemp folder
    #   b. extract frames
    for i,movie in enumerate(movies):
        outdir = '{}/frames_{}'.format(tempdir,i)
        if os.path.isdir(outdir):
            continue
        os.mkdir(outdir)
        os.system('mplayer -vo png:outdir={} {} > /dev/null 2>&1'.format(outdir,movie))
    nframes_all = [len(os.listdir('temp_montage/frames_{}/'.format(i))) for i in range(len(movies))]
    nframes = nframes_all[0]
    if len(set(nframes_all)) != 1:
        print("Not all movies have the same number of frames. I'll skip the last frames of the longer movies.")
        nframes = min(nframes_all)
    # 3) Create montage per frame
    cmdbase = 'montage -geometry +{}+{} -tile {}x{}'.format(ncol,nrow,drow,dcol)
    for i in range(1,nframes+1):
        cmd = cmdbase+' '+' '.join(['{}/frames_{}/{:08d}.png'.format(tempdir,j,i)
                                for j in range(len(movies))])+' {}/frame_{:08d}.png'.format(tempdir,i)
        os.system(cmd)
    # 4) Create new movie
    makeMovie('frame_', 'png', name, tempdir, './', fps, quiet=True,
              win=win, vqscale=vqscale, suffix='.avi', tomp4=tomp4)
    # 5) Clean up
    shutil.rmtree(tempdir)

def main():
    opt = parse_args()
    if opt.ncol is None:
        opt.ncol = len(opt.movies)
    montage_movies(opt.movies,opt.ncol,opt.nrow,opt.name,opt.drow,opt.dcol,
                   opt.fps,opt.win,opt.vqscale,opt.tomp4)



# # get command-line arguments
    # opt = parse_args()
    # # check arguments
    # if not opt.inputpath.endswith('/'):
    #     opt.inputpath += '/'
    # if not opt.outputpath.endswith('/'):
    #     opt.outputpath += '/'
    # makeMovie(opt.id, opt.imtype, opt.moviename, opt.inputpath, opt.outputpath, opt.fps, nx=opt.nx, ny=opt.ny,
    #           bitrate=opt.bitrate, scale=opt.scale, quiet=opt.quiet, win=opt.win, vqscale=opt.vqscale, tomp4=opt.mp4,
    #           postfix=opt.postfix)


if __name__ == "__main__":
    main()