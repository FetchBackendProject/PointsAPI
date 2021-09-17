# PointsAPI
Project for Fetch Rewards backend engineer opportunity

## Start Using
1. Ensure your device has python3 installed
```

2. Install Django on device if not installed already
```
pip3 install Django
```

3. Install Django rest framework
```
pip3 install djangorestframework
```

4. Navigate into folder and start server
```
python3 manage.py runserver
```

## Routes
The following routes are now active:
```

1. Method: POST | http://localhost:8000/add/
```
Accepts JSON object with the following 3 values:
- 'payer': string
- 'points': int
- 'timestamp': string
```

2. Method: PUT | http://localhost:8000/spend/
Accepts JSON object with the following value:
- 'points' int
```

3. Method: GET | http://localhost:8000/balances/
```
Does not require parameters
```
