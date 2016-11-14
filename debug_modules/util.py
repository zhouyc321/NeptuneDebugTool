import subprocess
import yaml
import mysql.connector

class Util:
    conf_file = "/home/xad/neptune/conf/index/normandy/indexgen.conf"
    dbconfig = {}

    @staticmethod
    def call(cmd):
        process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
        output,err = process.communicate()
        output = output.rstrip()
        return output

    @staticmethod
    def getDBConf():
        stream = open(Util.conf_file, "r")
        conf = yaml.load(stream)
        hostAndPortStr = conf["dbconfig"]["server"]
        hostAndPort = hostAndPortStr.split(':')
        Util.dbconfig["host"] = hostAndPort[0]
        Util.dbconfig["database"] = str(conf["dbconfig"]["db"])[2:-2]
        Util.dbconfig["user"] = conf["dbconfig"]["user"]
        Util.dbconfig["password"] = conf["dbconfig"]["pass"]
        Util.dbconfig["port"] = hostAndPort[1]
        stream.close()

    @staticmethod
    def runSqlQuery(query):
        conn = mysql.connector.connect(**Util.dbconfig)
        cursor = conn.cursor()
        data = None
        try:
            cursor.execute(query)
            data = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
            return data
