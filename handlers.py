def ProdRequest(x):
  y = 'client send: {} to Prod upstream'.format(x)
  return y

def StageRequest(x):
  y = 'client send: {} to Stage upstream'.format(x)
  return y

