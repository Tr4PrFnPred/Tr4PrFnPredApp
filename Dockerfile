FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /usr/src/app

COPY . ./

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && cd src/Tr4PrFnPredApp

CMD ["uvicorn", "src.Tr4PrFnPredApp.app:app", "--host", "0.0.0.0", "--port", "8000"]