#!/bin/bash -e

for max_epochs in 10 100 1000 10000
do
    for i in {1..100}
    do
        ~/permve-ntnu-it3105/vi/vi/app/egg_carton/egg_carton.py  5  5 2 --max_epochs $max_epochs >> egg-scenario-1-${max_epochs}-epochs.txt
        ~/permve-ntnu-it3105/vi/vi/app/egg_carton/egg_carton.py  6  6 2 --max_epochs $max_epochs >> egg-scenario-2-${max_epochs}-epochs.txt
        ~/permve-ntnu-it3105/vi/vi/app/egg_carton/egg_carton.py  8  8 1 --max_epochs $max_epochs >> egg-scenario-3-${max_epochs}-epochs.txt
        ~/permve-ntnu-it3105/vi/vi/app/egg_carton/egg_carton.py 10 10 3 --max_epochs $max_epochs >> egg-scenario-4-${max_epochs}-epochs.txt
    done
done

