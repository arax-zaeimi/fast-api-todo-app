# Create and Activate Virtual Environment

```
python -m venv venv

.venv/Scripts/activate
```

# Install dependecies

```
pip install -r requirements.txt
```

# Run the app

You can run the app using either `unicorn` or `fastapi`. The `fastapi` option genenrates api documentation as well.

```
uvicorn books:app --reload
```

```
fastapi run books.py --reload
fastapi dev books.py --reload
```
