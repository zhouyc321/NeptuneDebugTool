from util import Util
import json

class Selfsold:

    @staticmethod
    def getDocId(data, id):
        cmd = "grep -nP \"\t" + str(id) + "\t\" /home/xad/neptune/logs/index/merge/current/adgroupdetails.index | awk -F '\t' '{print $1}'"
        output = Util.call(cmd)
        if not output:
            data['msg'] = 'Not found in selfsold'
            data['doc_id'] = -1
            return -1

        docIdHashPair = output.split(":")
        docId = docIdHashPair[0]
        data['msg'] = 'Found in selfsold'
        data['doc_id'] = int(docId) - 1
        adgroupHash = docIdHashPair[1]
        return adgroupHash;

    @staticmethod
    def getFwdIdxFields(data, adgroupHash):
        cmd = "sudo /home/xad/neptune/bin/nise_forward_index_reader -i /home/xad/neptune/data/index/current/adgrpfwdidx -k " + str(adgroupHash) + " -d -t -m /home/xad/neptune/data/index/current/adgrpid2doc"
        output = Util.call(cmd)
        lines = output.split('\n')
        line1 = lines[0].split('\t')
        line2 = lines[1].split('\t')
        fwdFields = {}
        for i in range(0, len(line1)):
            fwdFields[line1[i]] = line2[i]
        data['fwdFields'] = fwdFields

    @staticmethod
    def getBooleanExp(data, id):
        cmd = "cat /home/xad/neptune/logs/index/merge/current/adgroupdetails.schema"
        output = Util.call(cmd)
        fieldNum = output.count(',')
        cmd = "grep -nP \"\t" + str(id) + "\t\" /home/xad/neptune/logs/index/merge/current/adgroupdetails.index | awk -F '\t' '{print $" + str(fieldNum) + "}'"
        output = Util.call(cmd)
        fields = output.split(' AND ');
        booleanList = []
        for string in fields:
            obj = {}
            firstBlank = string.find(' ')
            lastBlank = string.rfind(' ')
            obj['key'] = string[:firstBlank]
            obj['type'] = string[firstBlank:lastBlank]
            obj['value'] = string[lastBlank+2:-1]
            booleanList.append(obj)
        data['booleanExp'] = booleanList

    @staticmethod
    def getErrorLog(data, id):
        cmd = "grep 'adgroupId: " + str(id) + " ' /home/xad/neptune/logs/index/selfsold/current/*.log"
        output = Util.call(cmd)
        sqlQuery = "SELECT campaign_id FROM adgroup WHERE id = " + str(id) + ";";
        result = Util.runSqlQuery(sqlQuery)
        campaign_id = -1;
        for row in result:
            campaign_id = row[0]
        cmd = "grep 'campaignId: " + str(campaign_id) + " ' /home/xad/neptune/logs/index/selfsold/current/*.log"
        output += Util.call(cmd)
        data['errorlog'] = output

    @staticmethod
    def selfsold(id):
        data = {}
        adgroupHash = Selfsold.getDocId(data, id)
        Selfsold.getErrorLog(data, id)
        if data['doc_id'] != -1:
            Selfsold.getFwdIdxFields(data, adgroupHash)
            Selfsold.getBooleanExp(data, id)
        return json.dumps(data)
