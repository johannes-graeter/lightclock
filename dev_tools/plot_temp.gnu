#!/usr/bin/gnuplot

reset
set macros

# wxt
set terminal wxt 0 size 1200,800 enhanced font 'Verdana,10' persist

# csv import
set datafile separator comma

# colors
set style line 1 lt 1 lc rgb '#FB9A99' # light red
set style line 2 lt 1 lc rgb '#A6CEE3' # light blue

###unset key

# axes
set style line 11 lc rgb '#808080' lt 1
set border 3 front ls 11
set tics nomirror out scale 0.75

# grid
set style line 12 lc rgb'#808080' lt 0 lw 1
set grid back ls 12
set grid xtics ytics mxtics


#plot 'temp_log.csv'
plot 'tmp.csv'
