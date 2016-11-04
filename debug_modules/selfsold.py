import subprocess

class Selfsold:

    @staticmethod
    def getDocId(id):
        cmd = "grep -nP \"\t" + str(id) + "\t\" /home/xad/neptune/logs/index/merge/current/adgroupdetails.index | cut -d : -f 1"
        process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
        output,err = process.communicate()
        if not output:
            return {'msg' : 'Not found in selfsold', 'doc_id' : -1}
        else:
            return {'msg' : 'Found in selfsold', 'doc_id' : output}
