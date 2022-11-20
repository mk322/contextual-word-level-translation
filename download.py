from transformers import AutoTokenizer, AutoModelForCausalLM
import torch.nn.functional as F
import torch
import numpy as np
import json
import argparse

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model_name', type=str, default='gpt-neo', required=True)
parser.add_argument('-s', '--model_size', type=str, required=True)
args = parser.parse_args()


print(args.model_name, args.model_size)
