try:
    import theano
    print('theano: %s' % theano.__version__)
except:
    print('load theano failed')

# tensorflow
try:
    import tensorflow
    print('tensorflow: %s' % tensorflow.__version__)
except:
    print('load tensorflow failed')

# keras
try:
    import keras
    print('keras: %s' % keras.__version__)
except:
    print('load keras failed')
