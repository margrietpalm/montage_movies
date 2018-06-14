# Combine multiple movies into one

This script automates the procedure for combining movies described [here](https://incenp.org/notes/2012/combining-movies.html).

## Installation

### Dependencies
- Python (2.7 or later)
- Python library future
- [imagemagick](https://www.imagemagick.org/)
- [mplayer](http://www.mplayerhq.hu/design7/news.html)
- [montage_movies](https://github.com/margrietpalm/montage_movies)

### Set up as command line program
1. Make script executable:
    ```chmod +x montage_movies.py```
2. Create a link to `https://github.com/margrietpalm/https://github.com/margrietpalm/montage_movies` in a folder in your `PATH`. For example, when you have a `bin` folder in your home
 that is in your `PATH`: `ln -s /path/to/https://https://github.com/margrietpalm/montage_movies.com/margrietpalm/montage_movies/montage_movies.py /home/USERNAME/bin/montage_movies`
3. Now you can run the script with `montage_movies`


## Usage

Example: combine movies `1.avi`, `2.avi`, `3.avi` and `4.avi` in a 2x2 montage and create a 5fps movie:

```montage_movies -x 2 -y 2 -f 5 1.avi 2.avi 3.avi 4.avi```

More help:

```
montage_movies -h
usage: montage_movies.py [-h] [-q] [-x NCOL] [-y NROW] [--dx DCOL] [--dy DROW]
                         [--name NAME] [-f FPS] [-v VQSCALE] [-w] [--mp4]
                         [movies [movies ...]]

Combine multiple movies into one using ImageMagick's montage and im2movie

positional arguments:
  movies                list of movies to combine

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           suppress output
  -x NCOL, --ncol NCOL  number of columns
  -y NROW, --nrow NROW  number of rows
  --dx DCOL             horizontal spacing
  --dy DROW             vertical spacing
  --name NAME           movie name
  -f FPS, --fps FPS     frame rate
  -v VQSCALE, --vqscale VQSCALE
                        quality, lower is better (but file size is larger)
  -w, --win             make windows compatible movie
  --mp4                 make mp4

```


