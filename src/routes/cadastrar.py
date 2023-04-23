from flask import Blueprint, jsonify, request
from sqlalchemy import select, exc

from ..constants.http_status_codes import (HTTP_200_OK, HTTP_201_CREATED,
                                           HTTP_400_BAD_REQUEST,
                                           HTTP_409_CONFLICT)
from ..models import Consumos, Usuarios,db, session
import json
from asyncpg.exceptions import UniqueViolationError


cadastrar = Blueprint("cadastrar", __name__, url_prefix="/api/cadastrar")

@cadastrar.post('/usuarios')
def usuarios():
    dados = request.get_json()
    usuarios = [Usuarios(**d) for d in dados['usuarios']]
    try:
        db.session.add_all(usuarios)
        db.session.commit()
        return jsonify({'message': 'Usuarios inseridos com sucessos'}), HTTP_200_OK
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), HTTP_400_BAD_REQUEST

@cadastrar.post('/consumos')
def consumos():
    dados = request.get_json()
    dados_python = json.loads(dados) if isinstance(dados, str) else dados
    consumos_enviado = [Consumos(**d) for d in dados_python['consumos']]
    try:
        db.session.add_all(consumos_enviado)
        db.session.commit()
        return jsonify({'message': 'Consumos inseridos com sucessos'}), HTTP_200_OK
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), HTTP_400_BAD_REQUEST