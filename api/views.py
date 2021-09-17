# from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

people = {
    # 'KENT':{'points':500, 'transactions':[]},
    # 'WAYNE':{'points':20000, 'transactions':[]},
    # 'PARKER':{'points':100, 'transactions':[]},
    # 'STARK':{'points':5000, 'transactions':[]}
    }

transactions = {
    'next_id':3,
    'payments':[
    	{'id':0, 'points':500, 'timestamp':'2020-15-02T14:00:00Z'},
    	{'id':1, 'points':500, 'timestamp':'2020-13-02T14:00:00Z'},
    	{'id':2, 'points':500, 'timestamp':'2020-11-02T12:00:00Z'}
    ]
}

old_transactions = []

# Function to sort transactions by timestamps from oldest to newest
def sortTransactions():
    transactions['payments'].sort(key=lambda x:x['timestamp'])
sortTransactions()

# Add method
@csrf_exempt
def add(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        payment = json.loads(body_unicode)

        # Payload information checks
        if not payment.get('payer'):
            return HttpResponse('Error: No payer specified in payload')
        if type(payment.get('payer')) is not str:
            return HttpResponse('Error: Wrong value type for payer')
        if not payment.get('points'):
            return HttpResponse('Error: None points specified in payload')
        if  type(payment.get('points')) is not int:
            return HttpResponse('Error: Wrong value type for points')
        if not payment.get('timestamp'):
            return HttpResponse('Error: No timestamp specified in payload')
        if type(payment.get('timestamp')) is not str:
            return HttpResponse('Error: Wrong value type for timestamp')

        payer_name = payment.get('payer').upper()

        # If payer isnt in people dictionary, add them with 0 points
        if payer_name not in people:
            if payment.get('points') < 1:
                return HttpResponse('Error: This will bring this users points to or below zero')
            people[payer_name] = {'points':payment.get('points'), 'transactions':[]}
        # If payer is in people dictionary, add to their points
        else:
            if people[payer_name]['points'] + payment.get('points') < 1:
                return HttpResponse('Error: This will bring this users points to or below zero')
            people[payer_name]['points'] += payment.get('points')  

        # Add transaction id to persons transaction list
        people[payer_name]['transactions'].append(transactions['next_id'])

        # Add payment to transactions
        transactions['payments'].append({
            'id': transactions['next_id'],
            'points': payment.get('points'),
            'timestamp': payment.get('timestamp')
        })

        transactions['next_id'] += 1

        sortTransactions()

        return HttpResponse('Success: Payment added')
    else:
        return HttpResponse('Error: You are using is the wrong HTTP method This route is for POST requests')

@csrf_exempt
def spend(request):

    if request.method == 'PUT':
        body_unicode = request.body.decode('utf-8')
        points = json.loads(body_unicode).get('points')

        # Payload information checks
        if not points:
            return HttpResponse('Error: No points specified in payload')
        if type(points) is not int:
            return HttpResponse('Error: Wrong value type for points')

        sortTransactions()
        points_spent = []

        while points != 0:
            payments = transactions['payments']
            latest_payment = payments[0]

            if latest_payment['points'] > points:
                points_reduced = points

                # Reduce points from latest payment and set points to 0
                latest_payment['points'] -= points
                points = 0

               # Find person name using transaction number and subtract their points
                for person in people.keys():
                    if payments[0]['id'] in people[person]['transactions']:
                        people[person]['points'] -= points_reduced
                        break    

                # Add payment to points spent
                check = False
                for payer in points_spent:
                    if person == payer['payer']:
                        payer['points'] -= latest_payment['points']
                        check = True
                if not check:
                    points_spent.append({'payer':person, 'points': -points_reduced})

            else:
                points_reduced = latest_payment['points']

                # Reduce or add points from latest payment to points
                points -= latest_payment['points']

                # Find person name using transaction number and subtract their points
                for person in people.keys():
                    if payments[0]['id'] in people[person]['transactions']:
                        people[person]['points'] -= points_reduced
                        break

                # Add payment to points spent
                check = False
                for payer in points_spent:
                    if person == payer['payer']:
                        payer['points'] -= points_reduced
                        check = True
                if not check:
                    points_spent.append({'payer':person, 'points': -points_reduced})

                # Add old payment to old transactions
                old_transactions.append(payments.pop(0))

        return HttpResponse(points_spent)

    else:
        return HttpResponse('Error: You are using is the wrong HTTP method This route is for PUT requests')

@csrf_exempt
def balances(request):
    if request.method == 'GET':
        response = {}
        for person in people.keys():
            response[person] = people[person]['points']
        return HttpResponse(json.dumps(response))
    else:
        return HttpResponse('Error: You are using is the wrong HTTP method. This route is for GET requests')