# model-card-demo

![img](assets/cartoon-model-card.jpeg)

How to use Google's model card toolkit and add your own custom fields.

If you find any of this useful, I always appreciate contributions to my Saturday morning [fancy coffee fund](https://github.com/sponsors/mtpatter)!

This repo provides a Docker environment and instructions on how to generate a model card (outside of a Jupyter notebook or colab) using the tensorflow [model card toolkit](https://github.com/tensorflow/model-card-toolkit).

The repo also shows one way to update the model card template in order to add your own fields.  Custom fields require modifications to the protobuf schema, the model card toolkit class, the model card class, and the jinja template used to render the card.  The Dockerfile shows explicitly which files are overwritten in this example.  These changes need to be made *before* the toolkit is setup and installed because the toolkit compiles the protobuf schema during installation, which can make it difficult to make any updates to the template yourself.

Requires Docker.

## Usage

Clone repo and cd into directory.

```
git clone https://github.com/mtpatter/model-card-demo.git
cd model-card-demo
```

### Build a Docker image

This image is based on a TensorFlow Docker image.  Whenever changes are made to the proto fields, the image needs to be regenerated to reinstall the model card toolkit.

```
docker build -t "cards" .
```

### Generate the model card

Note well: the following command will run a Docker container that is mounted locally with write access to the local directory in order to produce the model card html.

```
docker run -u $(id -u):$(id -g) --rm -v $PWD/:/user/cards cards python make_card.py
```

The results are written locally to an html file in the `model_cards` directory.
