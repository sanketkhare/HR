#FROM python
#COPY . /usr/app/
#EXPOSE 5000
#WORKDIR /usr/app/
#RUN pip install -r requirements.txt
#CMD python form_enduser.py


FROM python
WORKDIR /hrproject
COPY requirements.txt /hrproject
EXPOSE 8000
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt
COPY . /hrproject
ENTRYPOINT ["python3"]
CMD ["end_user.py"]