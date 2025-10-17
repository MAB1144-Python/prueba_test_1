# Dockerfile para Website Design Evaluator
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Instalar Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Instalar ChromeDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
    ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# Crear usuario no-root
RUN useradd --create-home --shell /bin/bash evaluator
USER evaluator
WORKDIR /home/evaluator/app

# Copiar requirements y instalar dependencias Python
COPY --chown=evaluator:evaluator requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY --chown=evaluator:evaluator . .

# Crear directorios necesarios
RUN mkdir -p screenshots reports credentials logs

# Configurar variables de entorno para Chrome headless
ENV DISPLAY=:99
ENV CHROME_OPTIONS="--headless --no-sandbox --disable-dev-shm-usage --disable-gpu"

# Exponer puerto para API web (futuro)
EXPOSE 8000

# Comando por defecto
CMD ["python", "main.py", "--help"]