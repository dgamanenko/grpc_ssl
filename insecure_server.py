import signal
from concurrent import futures

import grpc

import service_pb2
import service_pb2_grpc

import handlers as handle

class ProdServerServicer(service_pb2_grpc.ProdServerServicer):

    def ProdRoot(self, request, context):
        response = service_pb2.ProdRootData()
        response.message = handle.ProdRequest(request.message)
        return response

class StageServerServicer(service_pb2_grpc.StageServerServicer):

    def StageRoot(self, request, context):
        response = service_pb2.StageRootData()
        response.message = handle.StageRequest(request.message)
        return response

def main():
    port = '50051'

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ProdServerServicer_to_server(ProdServerServicer(), server)
    service_pb2_grpc.add_StageServerServicer_to_server(StageServerServicer(), server)
    server.add_insecure_port('[::]:'+port)
    print('Starting server. Listening on port {}.'.format(port))
    server.start()
    try:
        while True:
            signal.pause()
    except KeyboardInterrupt:
        pass
    server.stop(0)

if __name__ == '__main__':
    main()
