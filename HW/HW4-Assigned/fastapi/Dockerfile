FROM continuumio/miniconda3

WORKDIR /API_SERVER
RUN pwd

COPY environment.yml .
RUN conda env create -f environment.yml -n hw3
RUN conda install -n hw3 fastapi[standard] 

COPY *.py .

EXPOSE 8000

CMD ["conda", "run", "--no-capture-output", "-n", "hw3", "fastapi", "run", "extract_save_data.py", "--port=8000", "--host=0.0.0.0"]