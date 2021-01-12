def test_mysql_process(host):
    assert host.service("my_db-mysql").is_running
    assert host.service("my_db-mysql").is_enabled

def test_check_mysql_access(host):
    assert host.run("mysql --protocol=tcp -h 127.0.0.1 -u u1 -P 13306 -ppassword1 db1").succeeded
    assert host.run("mysql --protocol=tcp -h 127.0.0.1 -u u1 -P 13306 -ppassword1 db2").failed
    assert host.run("mysql --protocol=tcp -h 127.0.0.1 -u u1 -P 13306 -ppassword2 db1").failed

    assert host.run("mysql --protocol=tcp -h 127.0.0.1 -u u3 -P 13306 -ppassword3 db1").succeeded
    assert host.run("mysql --protocol=tcp -h 127.0.0.1 -u u3 -P 13306 -ppassword3 db2").succeeded
    assert host.run("mysql --protocol=tcp -h 127.0.0.1 -u u3 -P 13306 -ppassword3 db3").failed

def test_db_encoding(host):
    assert host.run("""echo "SELECT DEFAULT_CHARACTER_SET_NAME FROM information_schema.SCHEMATA where SCHEMA_NAME='db1';" | mysql --protocol=tcp -h 127.0.0.1 -u u1 -P 13306 -ppassword1 db1 -N""").stdout.strip() == "utf8"
