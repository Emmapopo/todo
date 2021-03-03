import grpc 
from concurrent import futures
import time
import uuid

#import the generated class
import todo_pb2
import todo_pb2_grpc

todos = []

todos = todo_pb2.GetTodosResponse()

class TodoServicer(todo_pb2_grpc.TodoServicer):

    def AddTodo (self, request, context):
        response = todo_pb2.AddTodoResponse()       
        response.uuid = str(uuid.uuid4())
        response.title = request.title
        response.details = request.details
        response.deadline.seconds = request.deadline.seconds
        response.deadline.nanos = request.deadline.nanos

        todos.todos.append(response)
 
        return response

    def DeleteTodo(self, request, context):
        response = todo_pb2.DeleteTodoResponse()
        uuid = request.uuid
        status = 'fail'
        try:
            index = -1
            for i in todos.todos:
                index = index + 1
                
                if i.uuid == uuid:
                    if index >= 0:
                        del todos.todos[index]     
                        status = 'success'
                    break
                 
        except:
            status = 'fail'

        response.status = status
        return response


    def GetTodos(self, request, context):  
        
        return todos

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_TodoServicer_to_server`
# to add the defined class to the server

todo_pb2_grpc.add_TodoServicer_to_server(TodoServicer(),server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)

