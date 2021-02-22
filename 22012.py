import os
import redis
import json
from flask import Flask,request,jsonify

app = Flask(__name__)
db= redis.StrictRedis(
        host='10.100.2.135',
        port=6379,
        password='QLXmve62151',
        decode_responses=True
        )

#Get All
@app.route('/',methods=['GET'])
def Show_key():
    name=db.keys()
    name.sort()
    req = []
    for r in name :
        req.append(db.hgetall(r))
    return jsonify(req)


# Get Single
@app.route('/<Key>', methods=['GET'])
def Show_singel(Key):
    showSingel = db.hgetall(Key)
    return showSingel

#Update 
@app.route('/KPOP/<Key>', methods=['PUT'])
def Show_Update(Key):
    user = request.json['user']
    type = request.json['type']
    user = {"id":Key, "user":user, "type":type}
    db.hmset(Key,user)
    return "Create Success"

#Create
@app.route('/KPOP', methods=['POST'])
def Show_Create():
    id = request.json['id']
    user = request.json['user']
    type = request.json['type']
    user = {"id":id, "user":user, "type":type}
    db.hmset(id,user)
    return "Create Success"
    
#Delete
@app.route('/<Key>', methods=['DELETE'])
def Show_Del(Key):
    db.delete(Key)
    return "Delete Success"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)