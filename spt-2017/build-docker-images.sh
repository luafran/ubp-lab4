#!/bin/bash
root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

user="luafran"
version="1.0.0"

# echo "building worker..."
# cd img-proc-worker-svc
# gradle jar
# cd ..

echo "root_dir: $root_dir"
dirs="frontend mysql-svc auth-svc"

for dir in ${dirs}; do
    image_name=$(basename $dir)
    echo "############ ${image_name}"
    cd ${dir}
    docker build -t ${user}/${image_name}:${version} .
    cd ${root_dir}
done
