FROM continuumio/anaconda3

WORKDIR /STREAMLIT
RUN pwd

COPY environment.yml .
RUN conda env create -f environment.yml -n hw3

COPY *.py .

EXPOSE 8501

CMD ["conda", "run", "--no-capture-output", "-n", "hw3", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=true", "--server.enableXsrfProtection=false"]