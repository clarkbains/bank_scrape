import mysql.connector
class Database:
    def __init__(self,opts):
        self.db = mysql.connector.connect(**opts)
        self.cursor = self.db.cursor()
    
    
    def describeAccounts(self,key):
        self.cursor.execute("select * from account_info")
        return self._makeLookup(self.cursor.fetchall(),key,"account_info")
    def describeValues(self,key):
        self.cursor.execute("select * from investments")
        return self._makeLookup(self.cursor.fetchall(),key,"investments")
    def describeHistoricValues(self,account):
        self.cursor.execute("select value,time from historic_investments where account_id = %s",[account])
        return self._makeLookup(self.cursor.fetchall(),"time",headers = ["value","time"])
    
    def _expandSql(self,data,headers):
        expanded = []
        for row in data:
            currentRow = {}
            if len(row)>len(headers):
                raise ValueError('There must be an equal or greater number of headers than columns. Given row {0} with headers {1}'.format(str(row),str(headers)))
            for rowIndex in range(len(row)):
                currentRow[headers[rowIndex]]=row[rowIndex]
            expanded.append(currentRow)
        return expanded

    def _getAllHeaders(self,table):
        headers = []
        self.cursor.execute("select `COLUMN_NAME` from information_schema.columns where TABLE_NAME like %s",[table])
        for header in self.cursor.fetchall():
            if len(header)==1:
                headers.append(header[0])
        return headers

    def _makeLookup(self,data,key,database="",headers=[]):
        lookup = {}
        if (len(database)>0):
            headers = self._getAllHeaders(database)
        elif (len(headers)>0):
            pass
        else:
            raise ValueError('You must include either a datebase name or a header list')
        if key not in headers:
            raise KeyError("Could not find key inside headers")
        for elm in self._expandSql(data,headers):
            lookup[elm[key]] = elm
        return lookup
            