#base image
FROM tensorflow/tensorflow:latest-py3-jupyter as base



RUN apt-get install xvfb -y
RUN apt-get install python-opengl -y

RUN pip install 'gym==0.10.11'
RUN pip install imageio
RUN pip install PILLOW
RUN pip install pyglet
RUN pip install pyvirtualdisplay
RUN pip install tf-agents-nightly
RUN pip install tf-nightly
RUN pip install gmaps
RUN pip install pandas
RUN jupyter nbextension enable --py gmaps

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/tf --ip 0.0.0.0 --no-browser --allow-root"]