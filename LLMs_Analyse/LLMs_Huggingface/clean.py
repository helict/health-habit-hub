import gc
import torch

del pipeline

gc.collect()

torch.cuda.empty_cache()