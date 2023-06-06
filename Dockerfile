# FROM python:3.11.3-bullseye

# WORKDIR /app

# COPY requirements.txt requirements.txt

# RUN pip install -r requirements.txt

# COPY . .

# EXPOSE 8080

FROM python:3.9-slim

# Define o locale como "en_US.UTF-8"
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# Atualiza os pacotes do sistema
RUN apt-get update && apt-get install -y locales

# Configura o locale
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte para o contêiner
COPY app.py .

# Define o comando padrão a ser executado quando o contêiner for iniciado
CMD ["python", "app.py"]
