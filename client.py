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

    deadline = Timestamp()
    deadline.GetCurrentTime()

    todo = todo_pb2.AddTodoRequest(title=title, details = details, deadline=deadline)
    response = stub.AddTodo(todo)

    return MessageToJson(response)


@app.route('/deletetodo', methods=['POST'])
def delete_todo():
    uuid = request.form.get('uuid')

    inp = todo_pb2.DeleteTodoRequest(uuid=uuid)
    response = stub.DeleteTodo(inp)

    return MessageToJson(response)



@app.route('/gettodos', methods=['GET'])
def get_todos():
    todos = todo_pb2.GetTodosRequest()
    response = stub.GetTodos(todos)

    return MessageToJson(response)



if __name__ == '__main__':
    app.run(debug=True)




