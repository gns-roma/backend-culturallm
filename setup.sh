
if [ ! -d "mariadb_data" ] && mkdir -p mariadb_data; then
    echo "created mariadb_data/ folder"
elif [ ! -d "mariadb_data" ]; then
    echo "ERROR: while creating mariadb_data/ folder"
    exit 1
fi
if sudo chmod 777 mariadb_data; then
    echo "changed mode for mariadb_data/folder"
else 
    echo "ERROR: while changing mode for mariadb_data/ folder"
    echo "the Mariadb container may not work properly"
fi