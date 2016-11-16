from util import Util
import json

class Budget:

    autoBidFieldsName = ["adgroupId", "mult", "grad", "orgMult", "numUnsuccessfulImprovements", "initSPR", "finalSPR", "spentRateHistory", "winRateHistory"]

    @staticmethod
    def getDocId(data, id):
        cmd = "grep -nP \"\t" + str(id) + "\t\" /home/xad/neptune/logs/index/budget/current/adgroupbudgetdetails.index | awk -F '\t' '{print $1}'"
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
        return adgroupHash

    @staticmethod
    def getFwdIdxFields(data, adgroupHash):
        cmd = "sudo /home/xad/neptune/bin/nise_forward_index_reader -i /home/xad/neptune/data/budget/current/budgetadgroupfwdidx  -k " + str(adgroupHash) + " -d -t -m /home/xad/neptune/data/budget/current/budgetadgrpid2doc"
        output = Util.call(cmd)
        lines = output.split('\n')
        line1 = lines[0].split('\t')
        line2 = lines[1].split('\t')
        fwdFields = {}
        for i in range(0, len(line1)):
            fwdFields[line1[i]] = line2[i]
        data['fwdFields'] = fwdFields

    @staticmethod
    def getErrorLog(data, id):
        cmd = "grep 'adgroupId: " + str(id) + " ' /home/xad/neptune/logs/index/budget/current/*.log"
        output = Util.call(cmd)
        sqlQuery = "SELECT campaign_id FROM adgroup WHERE id = " + str(id) + ";";
        result = Util.runSqlQuery(sqlQuery)
        campaign_id = -1;
        for row in result:
            campaign_id = row[0]
        cmd = "grep 'campaignId: " + str(campaign_id) + " ' /home/xad/neptune/logs/index/budget/current/*.log"
        output += Util.call(cmd)
        data['errorlog'] = output

    @staticmethod
    def getAutoBidHistory(data, id):
        cmd = "grep '^" + str(id) + " ' /home/xad/neptune/logs/index/budget/current/multipliers.data"
        output = Util.call(cmd)
        fields = output.split(' ')
        fields = filter(None, fields)
        autoBidFields = {}
        for i in range(0, len(fields)):
            autoBidFields[Budget.autoBidFieldsName[i]] = fields[i]
        data['autobid'] = autoBidFields

    @staticmethod
    def getDailyImp(data, id):
        sqlQuery = "SELECT dailyImp FROM budget WHERE adGroup_id = " + str(id) + ";";
        result = Util.runSqlQuery(sqlQuery)
        imp = -1
        for row in result:
            imp = row[0]
        if imp != -1:
            data['dailyimp'] = imp


    @staticmethod
    def budget(id):
        data = {}
        data['adgroup_id'] = id
        adgroupHash = Budget.getDocId(data, id)
        Budget.getErrorLog(data, id)
        if data['doc_id'] != -1:
            Budget.getFwdIdxFields(data, adgroupHash)
        Budget.getAutoBidHistory(data, id)
        Budget.getDailyImp(data, id)
        return json.dumps(data)


