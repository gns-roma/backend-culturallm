echo "removing mariadb_data/ content..."
if rm -rf mariadb_data/*; then
    echo "everything has been cleaned up!"
else
    echo "something went wrong while executing: rm -rf mariadb_data/*"
fi