#import database_utils
from flask import Blueprint, request, json, jsonify
from sqlalchemy import create_engine, select, update, func, null, insert
from sqlalchemy.orm.session import sessionmaker
import database, json
import logging

urls_blueprint = Blueprint('urls', __name__,)

@urls_blueprint.route('/')
def index():
    print('abc')
    return 'urls index route'

@urls_blueprint.route('/create_tables', methods = ['GET'])
def create_database():
    try:
        database.init_db()
        ret = {"status": "Tabelas Criadas!!"}

    except Exception as e:
        print(e)
        ret = {"status": "Tables are not created!!"}    
    return ret


# ROTAS DOS CLIENTES

@urls_blueprint.route('/client/<f1>/<f2>', methods = ['POST', 'GET'])
def client(f1,f2):
    if (f1 == 'get'):
        ret = database.find_client(f2)
        #return json.dumps([(dict(row.items())) for row in ret])
        return ret
         
    elif(f1 == 'crud'):
        req_data = request.get_json()
        client_json = {"cpf": req_data['cpf'], "name": req_data['name'],
        "surname": req_data['surname'], "address": req_data['address'],
        "birth": req_data['birth'], "email": req_data['email'], "password": req_data['password']}
        #ret = database.add_client(client_json)
        #dados = json.dumps(client_json)

        if (f2 == 'add'):
            ret = database.add_client(client_json)
            #send_prototype.main(func2,dados)
            return ret
        elif (f2 == 'up'):
            ret = database.up_client(client_json)
            #send_prototype.main(func2,dados)
            return ret
        elif (f2 == 'del'):
            ret = database.del_client(client_json)
            #send_prototype.main(func2,dados)
            return ret

    elif(f1 == 'session'):
        req_data = request.get_json()
        client_json = {"email": req_data['email'], "password": req_data['password']}
        #ret = database.add_client_json(client_json)
        #dados = json.dumps(client_json)

        if (f2 == 'validate'):
            ret = database.validate_session(client_json)
            #ret = {"status": "List of users"}
            return ret

        elif(f2 == 'login'):
            ret = database.login_client(client_json)
            #send_prototype.main(f2,dados)
            return ret
        elif (f2 == 'logout'):
            ret = database.logout_client(client_json)
            #send_prototype.main(f2,dados)
            return ret

# ROTAS DOS AEROPORTOS    

@urls_blueprint.route('/airport/<f1>/<f2>', methods = ['POST', 'GET'])
def airport(f1,f2):
    if (f1 == 'get'):
        if (f2 == 'company'):
            req_data = request.get_json()
            airport_json = {"company": req_data['company']}
            ret = database.find_airport(airport_json)
            #ret = {"status": "List of users"}
            return ret

        elif (f2 == 'origin'):
            req_data = request.get_json()
            airport_json = {"origin": req_data['origin']}
            ret = database.find_destiny(airport_json)
            #ret = {"status": "List of users"}
            return ret

    elif(f1 == 'crud'):
        req_data = request.get_json()
        airport_json = {"iata": req_data['iata'], "name": req_data['name'],
        "city": req_data['city'], "state": req_data['state']}
        #ret = database.add_airport_json(airport_json)
        #dados = json.dumps(airport_json)

        if (f2 == 'add'):
            ret = database.add_airport(airport_json)
            #send_prototype.main(func2,dados)
            return ret
        elif (f2 == 'up'):
            ret = database.up_airport(airport_json)
            #send_prototype.main(func2,dados)
            return ret
        elif (f2 == 'del'):
            ret = database.del_airport(airport_json)
            #send_prototype.main(func2,dados)
            return ret

# ROTAS DOS VÔOS

@urls_blueprint.route('/flight/<func1>/<func2>', methods = ['POST', 'GET'])

def flight(func1,func2):
    if (func1 == 'get'):
        #database.find_flight(func2)
        ret = {"status": "List of users"}
        #return ret

        if (func2 == 'companyondate'):
            req_data = request.get_json()
            flight_json = {"company": req_data['company'], "date": req_data['date']}
            ret = database.find_company(flight_json)
            #ret = {"status": "List of Companies"}
            return ret

        elif (func2 == 'origin'):
            req_data = request.get_json()
            flight_json = {"departure": req_data['departure']}
            ret = database.find_destiny(flight_json)
            #ret = {"status": "List of users"}
            return ret
    
        elif (func2 == 'date'):
            req_data = request.get_json()
            flight_json = {"departure": req_data['departure']}
            ret = database.find_date(flight_json)
            #ret = {"status": "List of users"}
            return ret

        elif (func2 == 'passengers'):
            req_data = request.get_json()
            flight_json = {"pass": req_data['pass']}
            ret = database.find_passengers(flight_json)
            #ret = {"status": "List of users"}
            return ret

    elif(func1 == 'crud'):
        req_data = request.get_json()
        flight_json = {"origin": req_data['origin'],
        "destiny": req_data['destiny'], "departure": req_data['departure'],
        "company": req_data['company'], "passengers": req_data['passengers'],
         "arrival": req_data['arrival'],  "price": req_data['price']}
       #ret = database.add_flight_json(flight_json)
        #dados = json.dumps(flight_json)

        if (func2 == 'add'):
            ret = database.add_flight(flight_json)
            #send_prototype.main(func2,dados)
            return ret
        elif (func2 == 'up'):
            ret = database.up_flight(flight_json)
            #send_prototype.main(func2,dados)
            return ret
        elif (func2 == 'del'):
            ret = database.del_flight(flight_json)
            #send_prototype.main(func2,dados)
            return ret

# ROTAS DOS PEDIDOS

@urls_blueprint.route('/order/<func1>/<func2>', methods = ['POST', 'GET'])
def order(func1,func2):
    if (func1 == 'get'):
        database.find_order(func2)
        ret = {"status": "List of users"}
        return ret

    elif(func1 == 'crud'):
        req_data = request.get_json()
        json_order = {"id_session": req_data['id_session'], "id_flight": req_data['id_flight'],}
        #ret = database.add_order_json(json_order)
        dados = json.dumps(json_order)

        if (func2 == 'add'):
            ret = database.add_order(json_order)
            #send_prototype.main(func2,dados)
            return ret
        elif (func2 == 'up'):
            ret = database.up_order(json_order)
            #send_prototype.main(func2,dados)
            return ret
        elif (func2 == 'del'):
            ret = database.del_order(json_order)
            #send_prototype.main(func2,dados)
            return ret

# ROTAS DAS SESSÕES

@urls_blueprint.route('/clientsession/<func1>/<func2>', methods = ['POST', 'GET'])
def clientsession(func1,func2):
    if (func1 == 'get_session'):
        database.find_session(func2)
        ret = {"status": "List of users"}
        return ret
    
    if (func1 == 'validate'):
        ret = database.validate_session(func2)
        #ret = {"status": "List of users"}
        return ret

    elif(func1 == 'crud_session'):
        req_data = request.get_json()
        session_json = {"id": req_data['id'], "id_client": req_data['id_client'],
        "date": req_data['date'], "status": req_data['status']}
        ret = database.add_session_json(session_json)
        dados = json.dumps(session_json)

        if (func2 == 'add'):
            ret = database.add_session(session_json)
            #send_prototype.main(func2,dados)
            return ret
        elif (func2 == 'up'):
            ret = database.up_session(session_json)
            #send_prototype.main(func2,dados)
            return ret
        elif (func2 == 'del'):
            ret = database.del_session(session_json)
            #send_prototype.main(func2,dados)
            return ret

@urls_blueprint.route('/<func1>/<func2>', methods = ['POST', 'GET'])
def aluno(func1,func2):
    if (func1 == 'get_aluno'):
        database.find_aluno(func2)
        ret = {"status": "List of users"}
        return ret

    elif(func1 == 'crud_aluno'):
        req_data = request.get_json()
        aluno_json = {"matricula": req_data['matricula'], "nome": req_data['nome'],
        "sobrenome": req_data['sobrenome'], "endereco": req_data['endereco'],
        "nascimento": req_data['nascimento'], "email": req_data['email'], "senha": req_data['senha']}
        ret = database.add_aluno_json(aluno_json)
        dados = json.dumps(aluno_json)

        if (func2 == 'add'):
            ret = database.add_aluno_json(aluno_json)
            #send_prototype.main(func2,dados)
            return ret
        elif (func2 == 'up'):
            ret = database.up_aluno_json(aluno_json)
            #send_prototype.main(func2,dados)
            return ret
        elif (func2 == 'del'):
            ret = database.del_aluno_json(aluno_json)
           # send_prototype.main(func2,dados)
            return ret
    
