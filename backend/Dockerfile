# ===== STAGE 1: Build =====
FROM python:3.12-slim AS builder

WORKDIR /syncslot/backend

# Установка зависимостей для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем только зависимости
COPY requirements.txt .

# Устанавливаем зависимости в виртуальное окружение
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ===== STAGE 2: Runtime =====
FROM python:3.12-slim AS runtime

# Установка runtime-зависимостей (без компиляторов)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем виртуальное окружение из builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /syncslot/backend

# Копируем код приложения
COPY . .

# Создаем непривилегированного пользователя
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /syncslot/backend
USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:10004/health')" || exit 1

# Запуск (используем start.sh)
RUN chmod a+x ./start.sh
ENTRYPOINT ["sh", "/syncslot/backend/start.sh"]
