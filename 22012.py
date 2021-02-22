import os
import redis
import json
from flask import Flask,request,jsonify

#db คือตัวแปรที่ใช้เก็บค่าเพื่อเชื่อต่อฐานข้อมูล redis
app = Flask(__name__)
db= redis.StrictRedis(
        host='10.100.2.135', # IP ที่ได้จาก Ruk-Com
        port=6379,           # Port จาก Ruk-Com
        password='QLXmve62151', #pass ของ ฐานข้อมูล Redis
        decode_responses=True 
        )

#Get All คือการเเสดงข้อทั้งหมดในตาราง
@app.route('/',methods=['GET'])
def Show_idAll(): #Show_idAll() คือชื่อฟังก์ชัน
    name=db.keys() #name เป็นตัวเเปรที่ใช้เก็บข้อมูล db.keys คืออ้างอิงฐานข้อมูล Redis
    name.sort() #sort คือการเรียงข้อมูล
    req = [] #req คือตัวแปร array ที่ใช้เก็บค่าข้อมูล
    for r in name : #ใช้ตัวเเปร r ในการเก็บข้อมูลใน name
        req.append(db.hgetall(r)) #ใช้ตัวเเปร req มาเก็บค่าที่จะดึงออกมาจากฐานข้อมูล
    return jsonify(req) #รีเทิร์นค่า req ไปแสดงผล


# Get Single เเสดงเฉพาะข้อมูลในตาราง
@app.route('/<Key>', methods=['GET']) 
def Show_singel(Key): #Show_singel คือชื่อฟังก์ชัน
    showSingel = db.hgetall(Key) 
    return showSingel

#Update คือการเเก้ไขข้อมูลในตาราง
@app.route('/KPOP/<Key>', methods=['PUT'])
def Update(Key): #Update คือชื่อฟังก์ชัน
    user = request.json['user']
    type = request.json['type']
    user = {"id":Key, "user":user, "type":type} #ให้ตัว user เก็บข้อมูลของ id,user,type
    db.hmset(Key,user) #set ข้อมูลใน user โดยให้ user ชี้ไปตำแหน่งของ key 
    return "Update Success" 

#Create คือการาสร้างข้อมูลเพิ่มในตาราง
@app.route('/KPOP', methods=['POST'])
def Create(): #Create() คือชื่อฟังก์ชัน
    id = request.json['id']
    user = request.json['user']
    type = request.json['type']
    user = {"id":id, "user":user, "type":type} #ให้ตัว user เก็บข้อมูลของ id,user,type
    db.hmset(id,user) #set ข้อมูลใน user โดยให้ user ชี้ไปตำแหน่งของ id
    return "Create Success"
    
#Delete คือการลบข้อมูลในตาราง
@app.route('/<Key>', methods=['DELETE'])
def Del(Key): #Del คือชื่อฟังก์ชัน
    db.delete(Key) #การลบข้อมูลที่ตำเเหน่งของ key
    return "Delete Success"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)