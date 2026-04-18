# hr_interrao_api

API для HR-портала на Flask.

## Требования

- Python 3.11+
- `uv` или `pip`

## Установка зависимостей через `uv`

### 1. Установить `uv`

Если `uv` ещё не установлен:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Либо через `pip`:

```bash
pip install uv
```

### 2. Создать виртуальное окружение

```bash
uv venv
```

### 3. Активировать окружение

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Установить зависимости проекта

Только production-зависимости:

```bash
uv sync
```

С dev-зависимостями:

```bash
uv sync --dev
```

## Установка зависимостей через `pip`

### 1. Создать виртуальное окружение

```bash
python -m venv .venv
```

### 2. Активировать окружение

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Установить зависимости

Только production-зависимости:

```bash
pip install -r requirements/prod.txt
```

С dev-зависимостями:

```bash
pip install -r requirements/dev.txt
```

## Запуск проекта

После установки зависимостей:

```bash
python main.py
```

## Запуск тестов

Если установлены dev-зависимости:

```bash
pytest
```
