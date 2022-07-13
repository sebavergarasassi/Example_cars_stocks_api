

#                https://cars-stock-api.herokuapp.com/docs


from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import  random 

cars_api=FastAPI(title="API para el Control de stock de Autos",description="API de registro de autos, nuevos, usados y aleatorios")

CARS=[]

class car_class(BaseModel):
    mark:str
    manufacture_year:int
    color:str
    register_num :Optional [int]
    
class used_car(car_class):
    km:int
    tires_status:str
    observation:str

@cars_api.get("/")
def home_root():
    return {"Message":"This is the root, please visit /docs"}

@cars_api.post("/newcar")
def new_incoming(car:car_class):
    "register number will be reassigned by the api "
    car.register_num=random.randrange(0,999999)
    CARS.append(car)
    return {"Message":"New car "+car.mark +" has been received and register number is "+str(car.register_num)}

@cars_api.post("/usedcar")
def used_incomming(car:used_car):
    "register number will be reassigned by the api "
    car.register_num=random.randrange(0,999999)
    CARS.append(car)
    return {"Message":"Used car "+car.mark +" has been received and register number is "+str(car.register_num)}

@cars_api.post("/randomcar")
def CREATE_A_RANDOM_CAR():
    mark_list=["toyota","volkswagen","fiat","peugeot","citroen","honda"]
    color_list=["red","blue","green","white","black","grey"]
    myea=random.randrange(1990,2022)
    car=car_class(mark=random.choice(mark_list),manufacture_year=myea,color=random.choice(color_list))
    car.register_num=random.randrange(0,999999)
    CARS.append(car)
    return {"Message":"Random car with register number: "+str(car.register_num)+" has been received"}
    
@cars_api.get("/cars")
def stock():
    return CARS


#Observacion:
#al no estar incluido como parametro de la funcion "delete_car" el objeto "car", perteneciente a la clase "car_class"
#al citarlo dentro de la funcion del endpoint, los campos que lo componen (que definen al objeto) no pueden ser llamados de manera directa
#como pej: car.mark o car.color, para solucionar, recurrimos a los metodos disponibles (dentro de los que nos muestra visual code)
#entre ellos encontramos el metodo __getattribute__ que nos permite acceder a los campos del objeto, de manera que en lugar de
#usar car.register_num (que no esta disponible por lo expuesto) usamos car.__getattribute__("register_num")
#Ademas usamos un contador auxiliar i, para poder citar al elemento a remover de la lista


@cars_api.delete("/cars/{register_to_erase}")
async def delete_car(register_to_erase:int):
    initial_len=len(CARS)
    #condicion de lista CARS no vacia
    if initial_len>0:
        i=0
        for car in CARS:
            #condicion de registro encontrado
            if int(car.__getattribute__("register_num"))==register_to_erase:
                CARS.pop(i)
                return {"Message":"The Car whit register number "+str(register_to_erase)+" has been deleted"}
            i=i+1
    #condicion de registro no encontrado       
    return {"Message":"The Car whit register number "+str(register_to_erase)+" was not found, try to enter other register number"}
        

@cars_api.put("/cars/{register_to_update}")
def car_data_update(register_to_update:int,update_car:car_class):
    initial_len=len(CARS)
    #condicion de lista CARS no vacia
    if initial_len>0:
        i=0
        for car in CARS:
            #condicion de registro encontrado
            if int(car.__getattribute__("register_num"))==register_to_update:
                CARS.pop(i)
                update_car.register_num=register_to_update
                CARS.append(update_car)
                return {"Message":"The Car whit register number "+str(register_to_update)+" has been updated"}
            i=i+1
    #condicion de registro no encontrado       
    return {"Message":"The Car whit register number "+str(register_to_update)+" was not found, please check the  number of register"}












