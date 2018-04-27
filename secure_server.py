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

    with open('server.key', 'rb') as f:
        private_key = f.read()
    with open('server.crt', 'rb') as f:
        certificate_chain = f.read()

    server_credentials = grpc.ssl_server_credentials(
      ((private_key, certificate_chain,),))

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    service_pb2_grpc.add_ProdServerServicer_to_server(ProdServerServicer(), server)
    service_pb2_grpc.add_StageServerServicer_to_server(StageServerServicer(), server)
    server.add_secure_port('[::]:'+port, server_credentials)
    print('Starting server secure. Listening on port {}.'.format(port))
    server.start()
    try:
        while True:
            signal.pause()
    except KeyboardInterrupt:
        pass
    server.stop(0)

if __name__ == '__main__':
    main()
