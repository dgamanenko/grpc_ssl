import grpc

import service_pb2
import service_pb2_grpc


def main():
    host = 'localhost'
    port = '50051'

    channel = grpc.insecure_channel('{}:{}'.format(host, port))

    stub_prod = service_pb2_grpc.ProdServerStub(channel)
    data_prod = service_pb2.ProdRootData(message='hi prod!')
    response_prod = stub_prod.ProdRoot(data_prod)
    print(response_prod.message)

    stub_stage = service_pb2_grpc.StageServerStub(channel)
    data_stage = service_pb2.ProdRootData(message='hi stage!')
    response_stage = stub_stage.StageRoot(data_stage)
    print(response_stage.message)

if __name__ == '__main__':
    main()
