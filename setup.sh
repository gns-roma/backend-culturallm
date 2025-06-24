
if [ ! -d "mariadb/data" ] && mkdir -p mariadb/data; then
    echo "created mariadb/data/ folder"
elif [ ! -d "mariadb/data" ]; then
    echo "ERROR: while creating mariadbdata/ folder"
    exit 1
fi
if sudo chmod 777 mariadb/data; then
    echo "changed mode for mariadb_data/folder"
else 
    echo "ERROR: while changing mode for mariadb_data/ folder"
    echo "the Mariadb container may not work properly"
fi