import mariadb


_pool: mariadb.ConnectionPool | None = None


def init_pool():
    global _pool
    _pool = mariadb.ConnectionPool(
        pool_name="mypool",
        pool_size=10,
        host="culturallm-db",
        port=3306,
        user="user",
        password="userpassword",
        database="culturallm_db",
    )


def get_pool() -> mariadb.ConnectionPool:
    if _pool is None:
        raise RuntimeError("Pool not initialized")
    return _pool