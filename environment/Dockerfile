# hash:sha256:b47eb9da32e34263f1820e60ebd5441fc894d9a5b8a58ca5f07da3a794f6627f
FROM registry.codeocean.com/codeocean/miniconda3:4.9.2-cuda11.7.0-cudnn8-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN pip3 install -U --no-cache-dir \
    nltk==3.8.1 \
    openai==1.33.0 \
    praw==7.7.1 \
    scipy==1.10.1 \
    spacy-fastlang==2.1.0 \
    tqdm==4.66.4 \
    transformers==4.41.2
