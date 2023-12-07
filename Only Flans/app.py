from flask import Flask,render_template,request,jsonify,abort,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS
from flask_migrate import Migrate
import datetime
from flask_bcrypt import Bcrypt
from functools import wraps

import jwt

def obtener_info(token):
    if token:
        try:
            resp = Usuario.decode_auth_token(token)
            print(resp)
            user = Usuario.query.get(resp['sub'])
            if user:
                usuario = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.correo,
                        'admin': user.administrador,
                        'registered_on': user.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
                    }
                }
                return usuario
            else:
                error = {
                    'status': 'fail',
                    'message': resp
                }
                return error
        except Exception as e:
            print(e)
            return {'status': 'fail', 'message': 'Error al decodificar el token'}
    else:
        return {'status': 'fail', 'message': 'Token no proporcionado'}

def token_check(f):
    @wraps(f)
    def verificar(*args, **kwargs):
        token=None
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:
            return jsonify({'message': 'Token no encontrado'})
        try:
            info = obtener_info(token)
            print(info)
            if info['status'] == 'fail':
                return jsonify({'message': 'Token invalido'})
        except Exception as e:
            print(e)
            return jsonify({'message': 'Error'})
        return f(info['data'], *args, **kwargs)
    return verificar

def verificar(token):
    if not token:
        return jsonify({'message': 'Token no encontrado'})
    try:
        info = obtener_info(token)
        if info['status'] == 'fail':
            return jsonify({'message': 'Token invalido'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error'})
    return info


app = Flask(__name__)
USER_DB='postgres'
PASS_DB = 'contrasena1234'
URL_DB='localhost'
NAME_DB='onlyflans'
FULL_URL_DB=f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'
app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SECRET_KEY'] = 'hyperreal'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
bcrypt = Bcrypt()

secret_key = app.config.get('SECRET_KEY', 'default_secret_key')

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime(timezone=True), nullable=False)
    administrador = db.Column(db.Boolean, nullable=False, default=False)

    secret_key = app.config.get('SECRET_KEY', 'default_secret_key')

    def __init__(self, nombre, correo, contrasena, administrador=False) -> None:
        self.nombre=nombre
        self.correo = correo
        self.contrasena = bcrypt.generate_password_hash(contrasena).decode()
        self.fecha_registro = datetime.datetime.now()
        self.administrador = administrador

    def encode_auth_token(self, id_usuario):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=5),
                'iat': datetime.datetime.utcnow(),
                'sub': id_usuario
            }
            return jwt.encode(
                payload,
                secret_key, 
                algorithm='HS256'
            )
        except Exception as e:
            raise RuntimeError(f"Error al generar el token: {str(e)}")

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise RuntimeError('Firma del token expirada. Inicia sesión nuevamente.')
        except jwt.InvalidTokenError:
            raise RuntimeError('Token inválido.')


class Receta(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    dificultad = db.Column(db.String(100), nullable=False)
    tiempo_preparacion = db.Column(db.String(100), nullable=False)
    ingredientes = db.Column(db.Text, nullable=False)
    instrucciones = db.Column(db.Text, nullable=False)
    aprobado=db.Column(db.Boolean, nullable=False, default=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('recetas', lazy=True))

class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('favoritos', lazy=True))
    receta = db.relationship('Receta', backref=db.backref('favoritos', lazy=True))

class ImagenPerfil(db.Model):
    __tablename__='imagenes_usuario'
    id_imagen = db.Column(db.Integer,primary_key=True)
    datos = db.Column(db.LargeBinary,nullable=False)
    renderizado_datos=db.Column(db.Text,nullable=False)
    id_usuario=db.Column(db.Integer,db.ForeignKey('usuario.id'))
    region=db.relationship('Usuario',backref='usuarios')

class ImagenReceta(db.Model):
    __tablename__='imagenes_receta'
    id_imagen = db.Column(db.Integer,primary_key=True)
    datos = db.Column(db.LargeBinary,nullable=False)
    datos_renderizados=db.Column(db.Text,nullable=False)
    id_receta=db.Column(db.Integer,db.ForeignKey('receta.id'))
    region=db.relationship('Receta',backref='recetas')

#abor 404
@app.route('/404')
def error_404():
    abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/500')
def error_500():
    abort(500)

@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/admin_home",methods=["GET"])
def admin():
    if request.method == "GET":
        recetas = Receta.query.filter_by(aprobado=True).all()
    return render_template("InicioAdmin.html",recetas=recetas)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        token = request.args.get('token')
        if token:
            info = verificar(token)
            if info['status'] != "fail":
                responseObject = {
                    'status': "success",
                    'message': 'valid token',
                    'info': info
                }
                return jsonify(responseObject)
        return render_template('login.html')
    else:
        email = request.json.get('email')
        password = request.json.get('password')

        usuario = Usuario.query.filter_by(correo=email).first()

        if usuario and bcrypt.check_password_hash(usuario.contrasena, password):
            auth_token = usuario.encode_auth_token(usuario.id)
            responseObject = {
                'status': "success",
                'login': 'Login exitoso',
                'auth_token': auth_token,
                'administrador':usuario.administrador,
                'id':usuario.id
            }
            return jsonify(responseObject)
        return jsonify({'message': "Datos incorrectos"})

@app.route('/registro', methods=["GET", "POST"])
def registro():
    if request.method == "GET":
        return render_template('Registro.html')
    else:
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        usuario = Usuario(nombre=name, correo=email, contrasena=password)
        user_exists = Usuario.query.filter_by(correo=email).first()

        if not user_exists:
            try:
                db.session.add(usuario)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': "Registro exitoso"
                }
            except exc.SQLAlchemyError as e:
                responseObject = {
                    'status': 'error',
                    'message': str(e)
                }
        else:
            responseObject = {
                'status': 'error',
                'message': 'Usuario existente'
            }

        return jsonify(responseObject)

# Ruta para agregar o modificar receta
@app.route('/agregar_receta', methods=["GET", "POST"])
def agregar_receta():
    if request.method == "GET":
        return render_template('AgregarReceta.html')
    else:
        try:
            # Obtener datos del formulario
            titulo = request.form.get('titulo')
            descripcion = request.form.get('descripcion')
            dificultad = request.form.get('dificultad')
            tiempo_preparacion = request.form.get('tiempo_preparacion')
            ingredientes = request.form.get('ingredientes')
            instrucciones = request.form.get('instrucciones')

            # Obtener el ID del usuario del formulario
            usuario_id = request.form.get('usuario_id')
            print(f"Datos del formulario: {titulo}, {descripcion}, {dificultad}, {tiempo_preparacion}, {ingredientes}, {instrucciones}, {usuario_id}")

            modificar_receta_id = request.form.get('modificar_receta_id')

            if modificar_receta_id:
                # Si hay un ID para modificar, actualizar la receta existente
                receta_existente = Receta.query.get(modificar_receta_id)

                receta_existente.titulo = titulo
                receta_existente.descripcion = descripcion
                receta_existente.dificultad = dificultad
                receta_existente.tiempo_preparacion = tiempo_preparacion
                receta_existente.ingredientes = ingredientes
                receta_existente.instrucciones = instrucciones

                db.session.commit()

                return jsonify({'message': 'Receta modificada correctamente', 'status': 'success'})
            else:
                # Si no hay ID para modificar, agregar una nueva receta
                nueva_receta = Receta(
                    titulo=titulo,
                    descripcion=descripcion,
                    dificultad=dificultad,
                    tiempo_preparacion=tiempo_preparacion,
                    ingredientes=ingredientes,
                    instrucciones=instrucciones,
                    usuario_id=usuario_id
                )

                db.session.add(nueva_receta)
                db.session.commit()

                return jsonify({'message': 'Receta agregada correctamente', 'status': 'success'})

        except Exception as e:
            print(e)
            return jsonify({'message': 'Error al procesar la receta', 'status': 'fail'})




@app.route('/usuario_home', methods=["GET", "POST"])
def usuarioHome():
    if request.method == "GET":
        recetas = Receta.query.filter_by(aprobado=True).all()
        return render_template('UsuarioHome.html', recetas=recetas)
    
@app.route('/ver_recetas', methods=["GET", "POST"])
def ver_recetas():
    usuario_id = request.args.get('usuario_id')
    # if usuario_id is not None:
    #     usuario_id = int(usuario_id)

    if usuario_id:
        recetas = Receta.query.filter_by(usuario_id=usuario_id).all()
        for receta in recetas:
            if receta.aprobado==False:
                receta.aprobado="no"
            else:
                receta.aprobado="si"
        return render_template('VerRecetas.html', recetas=recetas)
    else:
        return jsonify({'message': 'Se requiere un ID de usuario para obtener recetas.'}), 400
        

@app.route('/aprobar', methods=["GET", "POST"])
def aprobar():
    recetas_pendientes = Receta.query.filter_by(aprobado=False).all()
    return render_template('Aprobar.html', recetas=recetas_pendientes)

@app.route('/aprobar_receta/<int:receta_id>', methods=["POST"])
def aprobar_receta(receta_id):
    receta = Receta.query.get(receta_id)
    if receta:
        receta.aprobado = True
        db.session.commit()
        return jsonify({'message': 'Receta aprobada correctamente', 'status': 'success'})
    else:
        return jsonify({'message': 'Receta no encontrada', 'status': 'fail'}), 404

@app.route('/recetacompleta', methods=["GET", "POST"])
def receta():
    receta_id = request.args.get('receta_id')
    if receta_id is not None:
        receta_id = int(receta_id)

    if receta_id:
        receta = Receta.query.get(receta_id)
        return render_template('Receta.html', receta=receta)
    else:
        return jsonify({'message': 'Se requiere un ID de receta para ver los detalles.'}), 400
    
@app.route('/eliminar_receta/<int:receta_id>', methods=["POST"])
def eliminar_receta(receta_id):
    try:
        receta = Receta.query.get_or_404(receta_id)
        db.session.delete(receta)
        db.session.commit()
        return jsonify({'message': 'Receta eliminada correctamente'})
    except Exception as e:
        return jsonify({'message': f'Error al eliminar la receta: {str(e)}'}), 500
    
@app.route('/obtener_receta/<int:receta_id>', methods=['GET'])
def obtener_receta(receta_id):
    receta = Receta.query.get_or_404(receta_id)
    return jsonify({
        'id': receta.id,
        'titulo': receta.titulo,
        'descripcion': receta.descripcion,
        'dificultad': receta.dificultad,
        'tiempo_preparacion': receta.tiempo_preparacion,
        'ingredientes': receta.ingredientes,
        'instrucciones': receta.instrucciones,
        'usuario_id': receta.usuario_id,
    })


@app.route('/toggle_favorito/<int:usuario_id>/<int:receta_id>', methods=['POST'])
def toggle_favorito(usuario_id, receta_id):
    # Verificar si ya existe la relación en la tabla de Favoritos
    favorito_existente = Favorito.query.filter_by(usuario_id=usuario_id, receta_id=receta_id).first()

    if favorito_existente:
        # Si ya existe, eliminarlo
        db.session.delete(favorito_existente)
        db.session.commit()
        return jsonify({'message': 'Receta eliminada de favoritos correctamente', 'status': 'removido de favoritos'})
    else:
        # Si no existe, agregarlo
        nuevo_favorito = Favorito(usuario_id=usuario_id, receta_id=receta_id)
        db.session.add(nuevo_favorito)
        db.session.commit()
        return jsonify({'message': 'Receta agregada a favoritos correctamente', 'status': 'agregado a favoritos'})

@app.route('/ver_favoritos', methods=["GET"])
def ver_favoritos():
    usuario_id = request.args.get('usuario_id')
    
    if usuario_id is not None:
        usuario_id = int(usuario_id)
        recetas_favoritas = Receta.query.join(Favorito).filter(Favorito.usuario_id == usuario_id).all()
        return render_template('Favoritos.html', recetas_favoritas=recetas_favoritas)
    else:
        return jsonify({'message': 'Se requiere un ID de usuario para ver los favoritos.'}), 400

import csv
from flask import Response

@app.route('/generar_csv_usuarios')
def generar_csv_usuarios():
    usuarios = Usuario.query.all()

    # Encabezados del CSV
    fieldnames = ['ID', 'Nombre', 'Correo', 'Fecha de Registro', 'Administrador']

    # Crear una respuesta del CSV
    def generate_csv():
        yield ','.join(fieldnames) + '\n'
        for usuario in usuarios:
            data = [
                str(usuario.id),
                usuario.nombre,
                usuario.correo,
                str(usuario.fecha_registro),
                str(usuario.administrador),
            ]
            yield ','.join(data) + '\n'

    response = Response(generate_csv(), content_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=usuarios.csv'
    return response


from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

@app.route('/generatePdf/<int:receta_id>')
def generate_pdf(receta_id):
    receta = Receta.query.get(receta_id)
    
    if not receta:
        return render_template('error.html', message='Receta no encontrada'), 404

    doc = SimpleDocTemplate(f"receta_{receta_id}.pdf", pagesize=letter)

    # Contenido del PDF con la información de la receta y saltos de línea
    text = f"""
    <font size="16">{receta.titulo}</font><br/>
    <br/><br/><p><b>Descripción:</b><br/>{receta.descripcion}</p>
    <br/><br/><p><b>Dificultad:</b><br/>{receta.dificultad}</p>
    <br/><br/><p><b>Tiempo de Preparación:</b><br/>{receta.tiempo_preparacion}</p>
    <br/><br/><p><b>Ingredientes:</b><br/>{receta.ingredientes}</p>
    <br/><br/><p><b>Instrucciones:</b><br/>{receta.instrucciones}</p>
    """

    # Crear un objeto de párrafo con HTML
    style = getSampleStyleSheet()["BodyText"]
    paragraph = Paragraph(text, style)
    elements = [paragraph]
    
    doc.build(elements)

    # Crear una respuesta con el archivo PDF
    response = make_response(open(f"receta_{receta_id}.pdf", "rb").read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=receta_{receta_id}.pdf'
    return response