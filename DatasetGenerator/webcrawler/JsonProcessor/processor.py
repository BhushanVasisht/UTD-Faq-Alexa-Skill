
import pickle
import os
# import datetime
# import time
# import json
# import boto3
class DataSet:
  def __init__(self, dict):
    self.dict = dict
  def __storeDictionary__(self,url):

    # with open('dataset/kb_'+  datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S') + '.json', 'w') as f:
    #   json.dump(self.dict, f)
    # s3 = boto3.resource('s3')
    # s3.create_bucket(Bucket='utd-hackathon-kb-storage')
    # s3.Object('utd-hackathon-kb-storage', 'dataset/kb_'+  datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S') + '.json').put(Body=bytes(json.dumps(self.dict, indent=2).encode('UTF-8')))
    #   # pickle.dump(self.dict, f, pickle.HIGHEST_PROTOCOL)
    className = url.split('/')[3]
    filename = '{className}/kb.p'.format(className=className)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'wb') as fp:
        pickle.dump(self.dict, fp, protocol=pickle.HIGHEST_PROTOCOL)



