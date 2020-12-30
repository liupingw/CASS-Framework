
.. toctree::
:maxdepth: 2

index.md
quickstart.md
extended.md


This portal provides a detailled documentation of the toolkit. It describes how to use the PyTorch project and how it works.



## Installation

1\. [Install PyTorch](http://pytorch.org/)

2\. Clone the py repository:

```bash
git clone https://github.com/py
cd py
```

3\. Install required libraries

```bash
pip install -r requirements.txt
```

And you are ready to go! Take a look at the [quickstart](quickstart.md) to familiarize yourself with the main training workflow.

Alternatively you can use Docker to install with `nvidia-docker`. The main Dockerfile is included
in the root directory.

## Citation

When using for research please cite our
[technical report](https://doi.org/10.18653/v1/P17-4012)

```
@inproceedings{
  author    = {Guillaume Klein and
               Yoon Kim and
               Yuntian Deng and
               Jean Senellart and
               Alexander M. Rush},
  title     = { Open-Source Toolkit for Neural Machine Translation},
  booktitle = {Proc. ACL},
  year      = {2017},
  url       = {https://doi.org/10.18653/v1/P17-4012},
  doi       = {10.18653/v1/P17-4012}
}
```

## Additional resources

You can find additional help or tutorials in the following resources:

* [Gitter channel](https://gitter.im/openmt-py)
