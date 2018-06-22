import pymongo

MONGODB_CONFIG = {
    'host': '10.131.69.180',
    'port': 27017,
    'db_name': 'qbot',
    'username': 'qbot',
    'password': 'qbot'
}
class MongoConn(object):
    def __init__(self):
        # connect db
        try:
            self.conn = pymongo.MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
            self.db = self.conn[MONGODB_CONFIG['db_name']]  # connect db
            self.username=MONGODB_CONFIG['username']
            self.password=MONGODB_CONFIG['password']
            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
        except Exception as e:
            print(e)