import grpc, sys

import service_pb2
import service_pb2_grpc

def main():
    host = 'lms-hawthorn-rg.raccoongang.com'
    port = '1443'

    with open('server.crt', 'rb') as f:
        trusted_certs = f.read()

    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    channel = grpc.secure_channel('{}:{}'.format(host, port), credentials)

    stub_stage = service_pb2_grpc.StageServerStub(channel)
    data_stage = service_pb2.ProdRootData(message=' '.join(sys.argv[1:]))
    response_stage = stub_stage.StageRoot(data_stage)
    print(response_stage.message)

if __name__ == '__main__':
    main()
