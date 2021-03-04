import os
import grpc
from flask import Flask, jsonify, request, flash, request, redirect, url_for, abort, send_from_directory
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.json_format import MessageToJson
import datetime
import json


#import the generated class
import todo_pb2
import todo_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = todo_pb2_grpc.TodoStub(channel)
#App flask configuration

app = Flask(__name__)

#Add Todo
@app.route('/addtodo', methods=['POST'])

def add_todo():

    title = request.form.get('title')
    details = request.form.get('details')
    time = request.form.get('deadline')

    # deadline = Timestamp()
    # deadline.GetCurrentTime()

    date_time_str = time
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

    deadline = Timestamp()
    deadline.FromDatetime(date_time_obj)

    
    add_todo_request = todo_pb2.AddTodoRequest(title=title, details = details, deadline=deadline)
    response = stub.AddTodo(add_todo_request)

    return MessageToJson(response)


@app.route('/deletetodo', methods=['POST'])
def delete_todo():
    id = request.form.get('id')

    delete_todo_request = todo_pb2.DeleteTodoRequest(uuid=id)
    response = stub.DeleteTodo(delete_todo_request)

    return MessageToJson(response)



@app.route('/gettodos', methods=['GET'])
def get_todos():
    get_todos_request = todo_pb2.GetTodosRequest()
    response = stub.GetTodos(get_todos_request)

    return MessageToJson(response)



if __name__ == '__main__':
    app.run(debug=True)




