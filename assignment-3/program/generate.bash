#!/bin/bash -e

mkdir -p ../report/images

for board in board-1-1 board-1-2 board-1-3 board-1-4
do
    ./a1.py ../problem/boards/${board}.txt
    rsvg-convert -f pdf -o ../report/images/${board}.pdf ${board}.svg
    rm ${board}.svg
done

for board in board-2-1 board-2-2 board-2-3 board-2-4
do
    ./a2.py ../problem/boards/${board}.txt
    rsvg-convert -f pdf -o ../report/images/${board}.pdf ${board}.svg
    rm ${board}.svg
done

for board in board-1-1 board-1-2 board-1-3 board-1-4
do
    for strategy in astar breadth_first dijkstra
    do
        ./a3-a.py ${strategy} ../problem/boards/${board}.txt
        rsvg-convert -f pdf -o ../report/images/${board}-${strategy}.pdf ${board}.svg
        rm ${board}.svg
    done
done

for board in board-2-1 board-2-2 board-2-3 board-2-4
do
    for strategy in astar breadth_first dijkstra
    do
        ./a3-b.py ${strategy} ../problem/boards/${board}.txt
        rsvg-convert -f pdf -o ../report/images/${board}-${strategy}.pdf ${board}.svg
        rm ${board}.svg
    done
done
