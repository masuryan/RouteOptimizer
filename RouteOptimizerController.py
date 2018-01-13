import json
from bottle import route, run, request, response, template, static_file, get
import threads

import numpy as np
import ast

# Static Routes
@get("/StaticFiles/Styles/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="StaticFiles/Styles")

@get("/StaticFiles/fonts/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
def font(filepath):
    return static_file(filepath, root="StaticFiles/fonts")

@get("/StaticFiles/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="static/img")

@get("/StaticFiles/Scripts//<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="StaticFiles/Scripts")


@route('/RouteOptimizer', method='PUT')
def do_RouteOptimizer():
    choice = request.json['Choice']
    numberOfDesinations = int(request.json['numberOfDesinations'])
    pref = int(request.json['preference'])
    nclus = int(request.json['nclus'])
    DesinationRoutes = ast.literal_eval(request.json['DesinationRoutes'])

    names = []
    for i in range(1, numberOfDesinations + 1):
        names.append(str(i))
    SourceRoutes = ast.literal_eval(request.json['SourceRoutes'])

    SourceRoutesNames = ast.literal_eval(request.json['sourcepointsnames'])
    response.headers['Access-Control-Allow-Origin'] = '*'

    try:
        x = threads.totalTSP(choice, numberOfDesinations, pref, data=DesinationRoutes, names=names, depo=SourceRoutes, deponame=SourceRoutesNames)
        return str(x)
    except Exception as e:
        return  str(e)

@route('/RouteOptimizer')
def get_RouteOptimizer():
    return template('StaticFiles/RouteOptimizer.html', name=request.environ.get('REMOTE_ADDR'))


run(host='localhost', port=8185, debug=True)