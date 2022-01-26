FROM tensorflow/tensorflow:2.7.0-jupyter

RUN apt-get update
RUN apt-get -y install git
RUN apt-get -y install nodejs npm

RUN mkdir -p /user/cards/
WORKDIR /user/cards/
RUN git clone https://github.com/tensorflow/model-card-toolkit.git
WORKDIR /user/cards/model-card-toolkit
RUN git checkout tags/v1.2.0

# Add my custom proto
WORKDIR /user/cards/model-card-toolkit/model_card_toolkit/proto
RUN cp model_card.proto model_card.proto_orig
ADD data/custom_card_template.proto model_card.proto

# Add my custom model card
WORKDIR /user/cards/model-card-toolkit/model_card_toolkit/
RUN cp model_card.py model_card.py_orig
ADD custom_model_card.py model_card.py

# Add my custom toolkit
RUN cp model_card_toolkit.py model_card_toolkit.py_orig
ADD custom_model_card_toolkit.py model_card_toolkit.py

WORKDIR /user/cards/model-card-toolkit
ADD requirements.txt .
RUN pip install -r requirements.txt

RUN npm install -g @bazel/bazelisk

RUN python3 setup.py sdist bdist_wheel
RUN pip install --upgrade ./dist/*.whl

WORKDIR /user/cards/
#  docker run -u $(id -u):$(id -g) -it --rm -v $PWD/:/user/cards cards /bin/bash
#  docker run -u $(id -u):$(id -g) --rm -v $PWD/:/user/cards cards python make_card.py
