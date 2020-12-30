# py: Open-Source Neural Machine Translation

[![Build Status](https://travis-ci.org/py.svg?branch=master)](https://travis-ci.org/py)
[![Run on FH](https://img.shields.io/badge/Run%20on-FloydHub-blue.svg)](https://floydhub.com/run?template=https://github.com/py)

This is a [Pytorch](https://github.com/pytorch/pytorch)
port of [(https://github.com/,
an open-source (MIT) neural machine translation system. It is designed to be research friendly to try out new ideas in translation, summary, image-to-text, morphology, and many other domains. Some companies have proven the code to be production ready.

We love contributions. Please consult the Issues page for any [Contributions Welcome](https://github.com/py/issues?q=is%3Aissue+is%3Aopen+label%3A%22contributions+welcome%22) tagged post. 

<center style="padding: 40px"><img width="70%" src="http://github.io/simple-attn.png" /></center>

Before raising an issue, make sure you read the requirements and the documentation examples.

Unless there is a bug, please use the [Forum](http://forum.net) or [Gitter](https://gitter.im/py) to ask questions.


Table of Contents
=================
  * [Full Documentation](http://net/py/)
  * [Requirements](#requirements)
  * [Features](#features)
  * [Quickstart](#quickstart)
  * [Run on FloydHub](#run-on-floydhub)
  * [Acknowledgements](#acknowledgements)
  * [Citation](#citation)

## Requirements

All dependencies can be installed via:

```bash
pip install -r requirements.txt
```

Note that we currently only support PyTorch 1.0.0

## Features

- [data preprocessing](http://net/py/options/preprocess.html)
- [Inference (translation) with batching and beam search](http://net/py/options/translate.html)
- [Multiple source and target RNN (lstm/gru) types and attention (dotprod/mlp) types](http://net/py/options/train.html#model-encoder-decoder)
- [TensorBoard](http://net/py/options/train.html#logging)
- [Source word features](http://net/py/options/train.html#model-embeddings)
- [Pretrained Embeddings](http://net/py/FAQ.html#how-do-i-use-pretrained-embeddings-e-g-glove)
- [Copy and Coverage Attention](http://net/py/options/train.html#model-attention)
- [Image-to-text processing](http://net/py/im2text.html)
- [Speech-to-text processing](http://net/py/speech2text.html)
- ["Attention is all you need"](http://net/py/FAQ.html#how-do-i-use-the-transformer-model)
- [Multi-GPU](http://net/py/FAQ.html##do-you-support-multi-gpu)
- Inference time loss functions.
- [Conv2Conv convolution model]
- SRU "RNNs faster than CNN" paper
- FP16 training (mixed-precision with Apex)

## Quickstart

[Full Documentation](http://net/py/)


### Step 1: Preprocess the data

```bash
python preprocess.py -train_src data/src-train.txt -train_tgt data/tgt-train.txt -valid_src data/src-val.txt -valid_tgt data/tgt-val.txt -save_data data/demo
```

We will be working with some example data in `data/` folder.

The data consists of parallel source (`src`) and target (`tgt`) data containing one sentence per line with tokens separated by a space:

* `src-train.txt`
* `tgt-train.txt`
* `src-val.txt`
* `tgt-val.txt`

Validation files are required and used to evaluate the convergence of the training. It usually contains no more than 5000 sentences.


After running the preprocessing, the following files are generated:

* `demo.train.pt`: serialized PyTorch file containing training data
* `demo.valid.pt`: serialized PyTorch file containing validation data
* `demo.vocab.pt`: serialized PyTorch file containing vocabulary data


Internally the system never touches the words themselves, but uses these indices.

### Step 2: Train the model

```bash
python train.py -data data/demo -save_model demo-model
```

The main train command is quite simple. Minimally it takes a data file
and a save file.  This will run the default model, which consists of a
2-layer LSTM with 500 hidden units on both the encoder/decoder.
If you want to train on GPU, you need to set, as an example:
CUDA_VISIBLE_DEVICES=1,3
`-world_size 2 -gpu_ranks 0 1` to use (say) GPU 1 and 3 on this node only.
To know more about distributed training on single or multi nodes, read the FAQ section.

### Step 3: Translate

```bash
python translate.py -model demo-model_acc_XX.XX_ppl_XXX.XX_eX.pt -src data/src-test.txt -output pred.txt -replace_unk -verbose
```

Now you have a model which you can use to predict on new data. We do this by running beam search. This will output predictions into `pred.txt`.

!!! note "Note"
    The predictions are going to be quite terrible, as the demo dataset is small. Try running on some larger datasets! For example you can download millions of parallel sentences for [translation](http://www.statmt.org/wmt16/translation-task.html) or [summarization](https://github.com/harvardnlp/sent-summary).

## Alternative: Run on FloydHub

[![Run on FloydHub](https://static.floydhub.com/button/button.svg)](https://floydhub.com/run?template=https://github.com/py)

Click this button to open a Workspace on [FloydHub](https://www.floydhub.com/?utm_medium=readme&utm_source=py&utm_campaign=jul_2018) for training/testing your code.


## Pretrained embeddings (e.g. GloVe)

Go to tutorial: [How to use GloVe pre-trained embeddings in py](http://forum.net/t/how-to-use-glove-pre-trained-embeddings-in-py/1011)

## Pretrained Models

The following pretrained models can be downloaded and used with translate.py.

http://net/Models-py/

## Acknowledgements

py is run as a collaborative open-source project.
The original code was written by [Adam Lerer](http://github.com/adamlerer) (NYC) to reproduce Lua using Pytorch.

Major contributors are:
[Sasha Rush](https://github.com/srush) (Cambridge, MA)
[Vincent Nguyen](https://github.com/vince62s) (Ubiqus)
[Ben Peters](http://github.com/bpopeters) (Lisbon)
[Sebastian Gehrmann](https://github.com/sebastianGehrmann) (Harvard NLP)
[Yuntian Deng](https://github.com/da03) (Harvard NLP)
[Guillaume Klein](https://github.com/guillaumekln) (Systran)
[Paul Tardy](https://github.com/pltrdy) (Ubiqus / Lium)
[François Hernandez](https://github.com/francoishernandez) (Ubiqus)
[Jianyu Zhan](http://github.com/jianyuzhan) (Shanghai)
[Dylan Flaute](http://github.com/flauted (University of Dayton)
and more !

OpentNMT-py belongs to the project along with Lua and tf.

## Citation

[ Neural Machine Translation Toolkit](https://arxiv.org/pdf/1805.11462)

[technical report](https://doi.org/10.18653/v1/P17-4012)

```
@inproceedings{
  author    = {Guillaume Klein and
               Yoon Kim and
               Yuntian Deng and
               Jean Senellart and
               Alexander M. Rush},
  title     = {Open{NMT}: Open-Source Toolkit for Neural Machine Translation},
  booktitle = {Proc. ACL},
  year      = {2017},
  url       = {https://doi.org/10.18653/v1/P17-4012},
  doi       = {10.18653/v1/P17-4012}
}
```
