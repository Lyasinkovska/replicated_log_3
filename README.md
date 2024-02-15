# Replicated Log
Client-Server application that includes primary node and two secondary nodes. 

![Architecture](replicated_log_3.png)

# How to use
To run application use the following command:
```
docker compose up --build
```
# How to test
To test application use:
```
curl -H "Content-Type: application/json" -X POST -d '{"message":"test 4", "write_concern":2}' http://127.0.0.1:5000/add_message
```
```
curl -H "Content-Type: application/json" -X GET  http://127.0.0.1:5000/get_messages
```
To check messages saved on secondary node use:
```
curl -H "Content-Type: application/json" -X GET  http://127.0.0.1:5001/get_messages
```
```
curl -H "Content-Type: application/json" -X GET  http://127.0.0.1:5002/get_messages
```
