#!/bin/bash

args="$@"
command="php artisan $args"
echo "$command"
docker exec -it udea-conciliacion bash -c "sudo -u manueljurado /bin/bash -c \"$command\""