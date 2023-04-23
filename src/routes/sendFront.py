
from flask import Blueprint, jsonify, request
from sqlalchemy import select, exc, func
import random
import numpy as np
from sqlalchemy import text

from ..constants.http_status_codes import (HTTP_200_OK, HTTP_201_CREATED,
                                           HTTP_400_BAD_REQUEST,
                                           HTTP_409_CONFLICT)
from ..models import Consumos, Usuarios,db, session
import json
from asyncpg.exceptions import UniqueViolationError


sendFront = Blueprint("sendFront", __name__, url_prefix="/api/sendFront")

@sendFront.route('/consumosMensal', methods=['GET'])
def get_consumos():
    query = db.session.query(
        func.date_trunc('month', Consumos.Data).label('mes_ano'),
        Usuarios.TU.label('TU'),
        func.sum(Consumos.consumo).label('total_consumo')
    ).join(
        Usuarios, Consumos.FK == Usuarios.id
    ).group_by(
        func.date_trunc('month', Consumos.Data),
        Usuarios.TU
    ).order_by(
        func.date_trunc('month', Consumos.Data).asc()
    )
    data = {'consumos': [{'mes_ano': str(mes_ano), 'TU': TU, 'total_consumo': total_consumo}
                          for mes_ano, TU, total_consumo in query.all()]}
    return jsonify(data)

from sqlalchemy.sql import text

@sendFront.route('/consumoBarChartByYear', methods=['GET'])
def get_consumos_by_year_2():
    query = text("""
    SELECT
        DATE_TRUNC('year', "main"."consumos"."Data") AS "ano",
        "main"."usuarios"."TU" AS "categoria",
        SUM("main"."consumos"."consumo") AS "total_consumo"
    FROM
        "main"."consumos"
        INNER JOIN "main"."usuarios" ON "main"."usuarios"."id" = "main"."consumos"."FK"
    GROUP BY
        DATE_TRUNC('year', "main"."consumos"."Data"),
        "main"."usuarios"."TU"
    ORDER BY
        "ano" ASC
""")

    result = db.session.execute(query)

    categories = {
        "INDUSTRIAL": "#5EDB6A",
        "SOCIAL": "#791CDC",
        "COMERCIAL": "#E6A23C",
        "DOMESTICO BAJA": "#909399",
        "DOMESTICO MEDIO": "#67C23A",
        "DOMESTICO RESIDENCIAL": "#909399",
        "ESPECIAL": "#c4c4c4"
    }

    data = {}
    for row in result:
        print(row)
        ano = row[0]
        categoria = row[1]
        total_consumo = row[2]
        if ano.year not in data:
            data[ano.year] = {
                "ANO": ano.year,
            }
        data[ano.year][categoria] = total_consumo
        data[ano.year][categoria + "color"] = categories[categoria]

    response = list(data.values())

    return jsonify(response)




@sendFront.route('/pizza', methods=['GET'])
def send_data_to_front():
    # Query para somar o consumo agrupado por TU
    consumo_query = db.session.query(
        Usuarios.TU.label('id'),
        func.sum(Consumos.consumo).label('value')
    ).join(Consumos, Usuarios.id == Consumos.FK)\
     .group_by(Usuarios.TU)

    # Converter o resultado em um dicionário que segue o formato esperado
    data = []
    for consumo in consumo_query:
        data.append({
            'id': consumo.id,
            'label': consumo.id,
            'value': consumo.value,
            'color': 'hsl(360, 70%, 50%)'  # Pode definir uma cor padrão aqui
        })

    return jsonify(data)
