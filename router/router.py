from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.user_schema import Userschema, DataUser
from config.db import conexion
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
import datetime
user = APIRouter()


@user.get("/")
def root():
    return {"message": "Hola soy una api con ruta, jsjsjs"}


@user.get("/api/user", response_model=List[Userschema])
def get_users():
    cursor = conexion.cursor()
    result = []
    resultados = cursor.execute("select * from usuarios;")
    for row in resultados.fetchall():
        item_dict = {}
        item_dict["id"] = str(row[0])
        item_dict["name"] = row[1]
        item_dict["password"] = row[2]
        item_dict["fecha"] = row[3]
        result.append(item_dict)
    # print(result)

    return result
    cursor.close()
    conexion.close()


@user.get("/api/user/{user_id}", response_model=Userschema)
def get_user(user_id: str):
    cursor = conexion.cursor()
    resultados = cursor.execute(
        "select * from usuarios where id_usuario=" + user_id)
    usar = resultados.fetchmany(1)
    print(usar)
    for row in usar:
        item_dict = {}
        item_dict["id"] = str(row[0])
        item_dict["name"] = str(row[1])
        item_dict["password"] = str(row[2])
        item_dict["fecha"] = str(row[3])

    print(resultados)
    return item_dict
    cursor.close()
    conexion.close()


@user.post("/api/user", status_code=HTTP_201_CREATED)
def create_user(data_user: Userschema):
    print(data_user)
    new_user = data_user.dict()
    cursorInsert = conexion.cursor()
    consulta = "insert into usuarios(nombre, password, fecha_creacion) values(?,?,?)"

    fecha = datetime.date.today()
    fechahoy = str(fecha.year) + "-" + str(fecha.month)+"-" + str(fecha.day)
    contra = generate_password_hash(data_user.password, "pbkdf2:sha256:10", 10)

    #print(fechahoy)
   # print(new_user["id"])
    #print(new_user["name"])
    #print(new_user["password"])

    cursorInsert.execute(
        consulta, new_user["name"], contra, fechahoy)

    cursorInsert.commit()
    cursorInsert.close()
    conexion.close()
    return Response(status_code=HTTP_201_CREATED)
    # video minuto 40


@user.put("/api/user/{user_id}", response_model=Userschema)
def update_user(data_update: Userschema, user_id: str):
    pass_enc = generate_password_hash(
        data_update.password, "pbkdf2:sha256:10", 10)

    consulta = "update usuarios set nombre = ?, password = ? where id_usuario = ?; "
    cursor = conexion.cursor()

    resultado = cursor.execute(
        consulta, data_update.name, data_update.password, user_id)

    resultados = cursor.execute(
        "select * from usuarios where id_usuario=" + user_id)
    usar = resultados.fetchmany(1)

    for row in usar:
        item_dict = {}
        item_dict["id"] = str(row[0])
        item_dict["name"] = str(row[1])
        item_dict["password"] = str(row[2])
        item_dict["fecha"] = str(row[3])

    cursor.commit()
    cursor.close()
    conexion.close()
    return item_dict


@user.post("/api/user/login", status_code=200)
def user_login(data_user: DataUser):
    cursor = conexion.cursor()
    result = cursor.execute(
        "select * from usuarios where nombre='" + data_user.name + "'")
    usar = result.fetchmany(1)
    datos = ""
    for row in usar:
        datos = str(row[2])
    print(datos)
    if result != None:
        check_pass = check_password_hash(datos, data_user.password)
        if check_pass:
            return {
                "status": 200,
                "message": "Access success"
            }

        return {
            "status": HTTP_401_UNAUTHORIZED,
            "message": "Access Denied"
        }

    cursor.close()
    conexion.close()


@user.delete("/api/user/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    cursor = conexion.cursor()
    resultado = cursor.execute(
        "delete from usuarios where id_usuario = " + user_id)
    cursor.commit()
    cursor.close()
    conexion.close()
    return Response(status_code=HTTP_204_NO_CONTENT)
