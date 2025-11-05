import os

# Desabilitar OneDNN/MKL-DNN ANTES de qualquer import do PaddleOCR
os.environ['FLAGS_use_mkldnn'] = '0'
os.environ['PADDLE_USE_MKLDNN'] = '0'
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
