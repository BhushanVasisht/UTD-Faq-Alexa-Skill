import pickle
import json
import os

questionSet={}
CLASS_SET=["alumni","housing","counseling"]
for className in CLASS_SET:
    pickle_off=open("{}/kb.p".format(className),"rb")
    temp = pickle.load(pickle_off)
    questions=list(temp.keys())
    questions = [x.split("?")[0] for x in questions]
    questionSet[className]=questions
    filename = 'dataset/{}.json'.format(className)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as outfile:
        json.dump(temp, outfile)
filename = 'dataset/{}.json'.format("questionSet")
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, 'w') as outfile:
    json.dump(questionSet, outfile)
