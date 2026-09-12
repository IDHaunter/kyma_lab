# kyma-lab
Kyma runtime test 

## local python development

Prepare environment:
```
/usr/local/bin/python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run fastAPI service
```
debug: python3 -m app.app
uvicorn app.app:app --host 0.0.0.0 --port 3000
```