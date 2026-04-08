
# 🐍 Stack Overflow Python Assistant

Чат-бот для семантического поиска ответов на вопросы Python по базе данных Stack Overflow.

## 📌 О проекте

Бот использует **embedding-модель** `all-MiniLM-L6-v2` из библиотеки `sentence-transformers` для поиска наиболее релевантных вопросов из датасета Stack Overflow. По выбранному вопросу выводится **лучший ответ** (с максимальным рейтингом).

### Особенности
- 🔍 **Семантический поиск** — ищет по смыслу, а не по ключевым словам
- ⚡ **Быстрая работа** — модель легковесная, работает даже на CPU
- 💾 **Предварительно закэшированные эмбеддинги** — ускоряет поиск
- 🎨 **Удобный интерфейс** на Streamlit с настройками и историей

## 🛠️ Используемые технологии

- **Python 3.11**
- **Streamlit** — веб-интерфейс
- **Sentence Transformers** — эмбеддинги текста
- **Pandas / NumPy** — обработка данных
- **scikit-learn** — косинусное сходство

## 📦 Установка и запуск

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/Iandlama/stackoverflow-qa-bot/blob/main/README.md
cd stackoverflow-qa-chatbot
```

### 2. Установите зависимости
```bash
pip install -r requirements.txt
```

**`requirements.txt`** (создайте этот файл):
```txt
streamlit
pandas
numpy
sentence-transformers
scikit-learn
```

### 3. Подготовьте данные

Скачайте датасеты с Kaggle:
- [Questions.csv](https://www.kaggle.com/datasets/stackoverflow/pythonquestions) (или StatsQuestions)
- [Answers.csv](https://www.kaggle.com/datasets/stackoverflow/stacksample)

Поместите файлы `Questions.csv` и `Answers.csv` в корневую папку проекта.

### 4. Создайте поисковый индекс

Запустите Jupyter Notebook `solution_ml.ipynb` и выполните все ячейки. Будут созданы файлы:
- `questions_small.pkl` — 5000 отфильтрованных вопросов
- `question_embeddings.pkl` — векторные представления вопросов
- `filtered_answers.pkl` — лучшие ответы для каждого вопроса

> ⚠️ Файлы CSV весят ~1.8 ГБ, но в итоговую выборку попадает только 5000 вопросов. На создание эмбеддингов уходит **10–15 минут** на CPU.

### 5. Запустите веб-интерфейс

```bash
streamlit run app.py
```

После запуска в браузере откроется `http://localhost:8501`

## 🎯 Как пользоваться

1. Введите вопрос в текстовое поле (например, *"How to merge two dictionaries?"*)
2. Нажмите **Search**
3. Бот покажет **3 самых похожих вопроса** с оценкой релевантности
4. Разверните блок **Answer** — увидите лучший ответ из датасета

### Настройки (левая панель)
- **Number of results** — количество выдаваемых вопросов (1–5)
- **Relevance threshold** — порог релевантности (0.25 = показывать только похожие)

## 📋 Примеры работы

| Вопрос пользователя | Найденный вопрос | Релевантность |
|---------------------|------------------|---------------|
| *How to merge two dictionaries?* | *How do I merge two dictionaries in a single expression?* | 78% |
| *Difference between list and tuple* | *What's the difference between lists and tuples?* | 92% |
| *What is a decorator?* | *How to make a decorator in Python?* | 71% |

## 📁 Структура проекта

```
.
├── app.py                      # Веб-интерфейс (Streamlit)
├── solution_ml.ipynb           # Ноутбук для подготовки данных
├── questions_small.pkl         # DataFrame с вопросами (создаётся автоматически)
├── question_embeddings.pkl     # Эмбеддинги вопросов (создаётся автоматически)
├── filtered_answers.pkl        # Словарь ответов (создаётся автоматически)
├── requirements.txt            # Зависимости Python
└── README.md                   # Этот файл
```

## 🧠 Как это работает

1. **Предобработка** — очистка HTML-тегов, inline-кода, склеивание `Title + Body`
2. **Эмбеддинги** — каждый вопрос превращается в вектор размером 384
3. **Поиск** — вопрос пользователя тоже превращается в вектор, считается косинусное сходство с вопросами из базы
4. **Выдача** — берутся топ-K вопросов, по ним из словаря достаются лучшие ответы

## ⚠️ Возможные проблемы

### Ошибка `MemoryError` при чтении CSV
**Решение:** В ноутбуке уже реализована чанковая загрузка (по 50 000 строк). Если нужно больше вопросов — уменьшите `chunksize`.

### Медленный запуск Streamlit
**Решение:** Файлы `.pkl` должны быть заранее созданы ноутбуком. Первый запуск может быть медленным из-за кэширования.

### Нет ответа на вопрос
**Решение:** В датасете не на все вопросы есть ответы с рейтингом >0. Бот показывает только те вопросы, для которых есть ответ в `filtered_answers.pkl`.

## 📄 Лицензия

Проект создан в рамках тестового задания. Данные Stack Overflow распространяются по лицензии CC BY-SA.

## ✍️ Автор

Ваше Имя — [GitHub](https://github.com/your-username)
```

---

## 🚀 Краткая инструкция по запуску (в консоли)

```bash
# 1. Установка зависимостей
pip install streamlit pandas numpy sentence-transformers scikit-learn

# 2. Запуск ноутбука (создание .pkl файлов)
jupyter notebook solution_ml.ipynb   # или просто откройте в VS Code / PyCharm

# 3. Запуск веб-приложения
streamlit run app.py
