from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import scoped_session
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update, delete, func, null, insert
from models import Client, Airport, Flight, Order, ClientSession, Base
from sqlalchemy import Column, Integer, String, MetaData
from settings import DATABASE_URL
from flask import jsonify   
import json

print(DATABASE_URL)
database_url = 'sqlite:///storage.db'
#database_url = 'postgresql+psycopg2://postgres:banco123@172.17.0.2/banco'

engine = create_engine(database_url)

db_session = scoped_session(sessionmaker(autocommit=True,
                                         autoflush=False,
                                         bind=engine))
                                         
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()    
    import models
    Base.metadata.create_all(bind=engine)

# METODOS DAS SESSOES

def validate_session(id_session):
    Session = sessionmaker(engine)
    session = Session()

    #query = (select(ClientSession).where(ClientSession))

    q2 = (select(func.max(ClientSession.id), ClientSession.status) .where(
    ClientSession.status != "closed").where(ClientSession.email_client == id_session['email']))

    conn = engine.connect()
    try:
        res1 = conn.execute(q2)
        #result = conn.execute(query)
        session.commit()
        #ret = {"status": "Cliente adicionado"}
        return json.dumps([(dict(row.items())) for row in res1])

    except Exception as e:
        print(e)
        ret = {"status": str(e)}
    return ret

# METODOS DOS CLIENTES

def find_client(cpf):
    Session = sessionmaker(engine)
    session = Session()

    s = select(Client).where(Client.cpf == cpf)
    conn = engine.connect()
    res = conn.execute(s)
    return json.dumps([(dict(row.items())) for row in res])
    

def add_client(json_client):
    Session = sessionmaker(engine)
    session = Session()

    query = (
            insert(Client).
            values(
                cpf = json_client['cpf'],
                name = json_client['name'],
                surname = json_client['surname'],
                adress = json_client['address'],
                birth = json_client['birth'],
                email = json_client['email'],
                password = json_client['password']
                )
    )

    q2 = (insert(ClientSession).values(email_client = json_client['email'], date = func.now(), status = 'online'))

    conn = engine.connect()
    try:
        res1 = conn.execute(q2)
        result = conn.execute(query)
        session.commit()
        ret = {"status": "Cliente adicionado"}

    except Exception as e:
        print(e)
        ret = {"status": str(e)}
    return ret

def up_client(json_client):
    Session = sessionmaker(engine)
    session = Session()

    query = (
            update(Client).
            where(Client.cpf == json_client['cpf'] and 
            Client.password == json_client['password']).
            values(
                name = json_client['name'],
                surname = json_client['surname'],
                adress = json_client['adress'],
                birth = json_client['birth'],
                email = json_client['email'],
                password = json_client['password']
                )
    )
    conn = engine.connect()
    try:
        result = conn.execute(query)
        session.commit()
        ret = {"status": "Cliente atualizado"}


    except Exception as e:
        print(e)
        ret = {"status": str(e)}
    return ret

def del_client(json_client):
    Session = sessionmaker(engine)
    session = Session()

    query = (
            delete(Client).
            where(Client.cpf == json_client['cpf'] and 
            Client.password == json_client['password'])
    )
    q2 = (delete(ClientSession).where(ClientSession.email_client == json_client['email']))
    conn = engine.connect()
    try:
        result = conn.execute(query)
        r2 = conn.execute(q2)
        session.commit()
        ret = {"status": "Cliente excluído"}


    except Exception as e:
        print(e)
        ret = {"status": str(e)}
    return ret

def login_client(json_client):

    Session = sessionmaker(engine)
    session = Session()

    #select.max(Client, Session).join(User.addresses).order_by(User.id, Address.id)

    operator = (select(Client.email).where(Client.password == json_client['password']).where(
    Client.email == json_client['email'])
    )
    
    query = (update(ClientSession).where(ClientSession.email_client == operator).where(
     ClientSession.status =='offline').
    values(status = 'online', date = func.now()))

    conn = engine.connect()
    try:
        result = conn.execute(query)
        session.commit()
        ret = {"status": "Você está logado"}
        
    except Exception as e:
        print(e)
        ret = {"status": str(e)}
    return ret

def logout_client(json_client):

    Session = sessionmaker(engine)
    session = Session()

    #select.max(Client, Session).join(User.addresses).order_by(User.id, Address.id)
    query = (update(ClientSession).where(ClientSession.email_client == json_client['email']
     and ClientSession.status =='online').
    values(status = 'offline', date = func.now()))

    conn = engine.connect()
    try:
        result = conn.execute(query)
        session.commit()
        ret = {"status": "Desconectando"}
        
    except Exception as e:
        print(e)
        ret = {"status": str(e)}
    return ret

# METODOS DOS AEROPORTOS

def find_airport(airport_json):
    Session = sessionmaker(engine)
    session = Session()

    # if(option == 'all' or option == 'ALL'):
    #     query = (select(Airport))
    
    # else: 
    #     query = (select(Airport).where(Airport.city == option))

    query = select(Flight.origin).where(Flight.company == airport_json['company'])
    conn = engine.connect()
    res = conn.execute(query)
    return json.dumps([(dict(row.items())) for row in res]) 


def add_airport(json_airport):
    Session = sessionmaker(engine)
    session = Session()

    query = (
            insert(Airport).
            values(
                iata = json_airport['iata'],
                name = json_airport['name'],
                city = json_airport['city'],
                state = json_airport['state']
                )
    )
    conn = engine.connect()
    try:
        result = conn.execute(query)
        session.commit()
        ret = {"status": "Aeroporto adicionado"}
        
    except Exception as e:
        print(e)
        ret = {"status": str(e)}
    return ret

def up_airport(json_airport):
    Session = sessionmaker(engine)
    session = Session()

    query = (
            update(Airport).
            where(Airport.iata == json_airport['iata']).
            values(
                iata = json_airport['iata'],
                name = json_airport['name'],
                city = json_airport['city'],
                state = json_airport['state'],
                )
    )
    conn = engine.connect()
    try:
        result = conn.execute(query)
        session.commit()
        ret = {"status": "Aeroporto atualizado"}


    except Exception as e:
        print(e)
        ret = {"status": str(e)}
    return ret

def del_airport(json_airport):
    Session = sessionmaker(engine)
    session = Session()

    query = (
            delete(Airport).
            where(Airport.iata == json_airport['iata'])
    )
    conn = engine.connect()
    try:
        result = conn.execute(query)
        session.commit()
        ret = {"status": "Aeroporto excluído"}


    except Exception as e:
        print(e)
        ret = {"status": str(e)}
    return ret

# METODOS DOS VOOS

def find_passengers(flight_json):
    Session = sessionmaker(engine)
    session = Session()

    min_price = select(func.min(Flight.price)).where(Flight.passengers == flight_json['pass'])
    query = (select(Flight).where(Flight.passengers == flight_json['pass'])).where(Flight.price == min_price)

    conn = engine.connect()
    res = conn.execute(query)
    return json.dumps([(dict(row.items())) for row in res]) 

def find_company(flight_json):
    Session = sessionmaker(engine)
    session = Session()

    filtercompany = (select(Flight).where(Flight.departure == flight_json['date']).where(Flight.company == flight_json['company']))
    #filterdate = select(filtercompany).where(filtercompany.departure == flight_json['date'])
    #filterdate = filtercompany.company
    conn = engine.connect()
    res = conn.execute(filtercompany)
    #res1 = conn.execute(filterdate)
    return json.dumps([(dict(row.items())) for row in res]) 

def find_destiny(flight_json):
    Session = sessionmaker(engine)
    session = Session()

    query = (select(Flight.destiny).where(Flight.origin == flight_json['origin']))

    conn = engine.connect()
    res = conn.execute(query)
    return json.dumps([(dict(row.items())) for row in res])

def find_date(flight_json):
    Session = sessionmaker(engine)
    session = Session()

    query = (select(Flight).where(Flight.departure == flight_json['departure']))

    conn = engine.connect()
    res = conn.execute(query)
    return json.dumps([(dict(row.items())) for row in res])
       
def add_flight(json_flight):
    Session = sessionmaker(engine)
    session = Session()

    query = (
            insert(Flight).
            values(
                origin = json_flight['origin'],
                destiny = json_flight['destiny'],
                company = json_flight['company'],
                passengers = json_flight['passengers'],
                departure = json_flight['departure'],
                arrival = json_flight['arrival'],
                price = json_flight['price']
                )
    )
    conn = engine.connect()
    try:
        result = conn.execute(query)
        session.commit()
        ret = {"status": "Vôo adicionado"}
        
    except Exception as e:
        print(e)
        ret = {"status": str(e)}
    return ret

def up_flight(json_flight):
    Session = sessionmaker(engine)
    session = Session()

    query = (
            update(Flight).
            where(Flight.id == json_flight['id']).
            values(
                origin = json_flight['origin'],
                destiny = json_flight['destiny'],
                company = json_flight['company'],
                passengers = json_flight['passengers'],
                departure = json_flight['departure'],
                arrival = json_flight['arrival'],
                price = json_flight['price']
                )
    )
    conn = engine.connect()
    try:
        result = conn.execute(query)
        session.commit()
        ret = {"status": "Aeroporto atualizado"}


    except Exception as e:
        print(e)
        ret = {"status": str(e)}
    return ret

def del_flight(json_flight):
    Session = sessionmaker(engine)
    session = Session()

    query = (
            delete(Flight).
            where(Flight.id == json_flight['id'])
    )
    conn = engine.connect()
    try:
        result = conn.execute(query)
        session.commit()
        ret = {"status": "Vôo excluído"}


    except Exception as e:
        print(e)
        ret = {"status": str(e)}
    return ret

# METODOS DOS PEDIDOS

def add_order2(json_order):
    Session = sessionmaker(engine)
    session = Session()

    validate = (select(ClientSession.status).where(ClientSession.id == json_order['id_session']))

    conn = engine.connect()

    res_session = conn.execute(validate)

    for row in res_session:
        res_session = dict(row.items())

    return res_session["status"]
    

def add_order(json_order):
    Session = sessionmaker(engine)
    session = Session()

    validate = (select(ClientSession.status).where(ClientSession.id == json_order['id_session']))

    conn = engine.connect()

    res_session = conn.execute(validate)

    for row in res_session:
        res_session = dict(row.items())


    if(res_session["status"] == "online"):

        cliente = select(ClientSession.email_client).where(ClientSession.id == json_order['id_session'])
        voo = select(Flight).where(Flight.id == json_order['id_flight'])
        client_info = select(Client).where(Client.email == cliente)
        conn = engine.connect()
        infoc = conn.execute(client_info)
        for row in infoc:
            infoc = dict(row.items())
        
        execvoo = conn.execute(voo)
        for row in execvoo:
            execvoo = dict(row.items())
        
        
        preco = select(Flight.price).where(Flight.id == json_order['id_flight'])
        origem = select(Airport).where(Airport.iata == execvoo['origin'])
        destino = select(Airport).where(Airport.iata == execvoo['destiny'])
        data = select(func.now())

        order = (
            insert(Order).
            values(
                id_session = json_order['id_session'],
                id_flight = json_order['id_flight'],
                date = data,
                price = preco
                ))

                
        #current_session = select(func.min(ClientSession.id)).where(client)
        close_currentsession = (update(ClientSession).
            where(ClientSession.id == json_order['id_session']).
            values(
                status = 'closed'
                ))
    
        newsession = insert(ClientSession).values(email_client = cliente, date = data, status = 'online')
        order_id = select(Order).where(Order.date == data)

        conn = engine.connect()
    
        place_order = conn.execute(order)
        close = conn.execute(close_currentsession)
        new = conn.execute(newsession)
        flight = conn.execute(voo)
        order = conn.execute(order_id)
        info_destino = conn.execute(destino)
        info_origem = conn.execute(origem)
        session.commit()
        info_flight = []
        info_order = []
        #relatorio = json.loads([(dict(row.items())) for row in info])
        for row in flight:
            info_flight = dict(row.items()) 
        for row in info_destino:
            info_destino = dict(row.items())
        for row in info_origem:
            info_origem = dict(row.items())
        for row in order:
            info_order = dict(row.items())
        
        return (f"Compra no valor de R${info_flight['price']} efetuada com sucesso.\n\n"
                f"Seu identificador é número {info_order['id']} para o vôo #{info_flight['id']}"
                f" da {info_flight['company']} linhas aéreas\n"
                f"Com origem em {info_origem['city']} no {info_origem['name']} e destino a {info_destino['city']}\n"
                f"no {info_destino['name']}. Embarque {info_flight['departure']} e previsão de chegada" 
                f" {info_flight['arrival']}\n\n"
                f"Tenha uma ótima viagem, {infoc['name']} {infoc['surname']}, nossa companhia agradece a preferência")
        
    else :
        return "Não foi possível atender a solitação, sessão expirada"
 
def up_order(json_order):
    Session = sessionmaker(engine)
    session = Session()

    query = (
            update(Order).
            where(Order.id == json_order['id']).
            values(
                id_client = json_order['id_client'],
                id_flight = json_order['id_flight'],
                date = json_order['date'],
                price = json_order['price'],
                )
    )
    conn = engine.connect()
    try:
        result = conn.execute(query)
        session.commit()
        ret = {"status": "Aeroporto atualizado"}


    except Exception as e:
        print(e)
        ret = {"status": str(e)}
    return ret

def del_order(json_order):
    Session = sessionmaker(engine)
    session = Session()

    query = (
            delete(Order).
            where(Order.id == json_order['id'])
    )
    conn = engine.connect()
    try:
        result = conn.execute(query)
        session.commit()
        ret = {"status": "Pedido excluído"}


    except Exception as e:
        print(e)
        ret = {"status": str(e)}
    return ret


