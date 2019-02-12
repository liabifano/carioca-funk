FROM python:3.6.7

COPY setup.py /carioca-funk/
COPY requirements.txt /carioca-funk/
COPY src/ /carioca-funk/src/

RUN find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
RUN pip install -U -r carioca-funk/requirements.txt
RUN pip install carioca-funk/.
