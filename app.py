import os
from flask import Flask, request, abort, jsonify
from models import setup_db, Actors, Movies, db
from flask_cors import CORS

from auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app, origins=['*']) #specifying origins arg here makes explicit but not necessary

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        print(excited)
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"
    
    @app.route('/lebowski')
    def lebowski():
        return '''Let me explain something to you. Um, I am not "Mr. Lebowski". You're Mr. Lebowski. I'm the Dude. So that's what you call me. You know, that or, uh, His Dudeness, or uh, Duder, or El Duderino if you're not into the whole brevity thing.'''
    
    @app.route('/thejesus')
    def thejesus():
        return '''Are you ready to be fucked, man? I see you rolled your way into the semis. Dios mio, man. Liam and me, we're gonna fuck you up.'''

    @app.route('/actors', methods=["GET"])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actors.query.order_by(Actors.id).all()
        formatted_actors = [actor.format() for actor in actors]
        return jsonify(
            {
                "success": True,
                "actors": formatted_actors,
                "total_actors": len(formatted_actors)
            }
        )

    @app.route('/movies', methods=["GET"])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movies.query.order_by(Movies.id).all()
        formatted_movies = [movie.format() for movie in movies]
        return jsonify(
            {
                "success": True,
                "movies": formatted_movies,
                "total_movies": len(formatted_movies)
            }
        )

    @app.route('/actors', methods=["POST"])
    @requires_auth('post:actors')
    def create_actors(payload):
        body = request.get_json()
        actor_name = body.get("name", None)
        actor_age = body.get("age", None)
        actor_gender = body.get("gender", None)
        try:
            actor = Actors(name=actor_name, age=actor_age, gender=actor_gender)
            actor.insert()

            actors = Actors.query.order_by(Actors.id).all()
            formatted_actors = [a.format() for a in actors]
            if len(formatted_actors) == 0:
                abort(404)
            return jsonify(
                {
                    "success": True,
                    "created": actor.id,
                    "actors": formatted_actors,
                    "total_actors": len(formatted_actors)
                }
            )
        except Exception as e:
            abort(422)

    @app.route('/movies', methods=["POST"])
    @requires_auth('post:movies')
    def create_movies(payload):
        body = request.get_json()
        movie_title = body.get("title", None)
        movie_release_date = body.get("release_date", None)
        try:
            movie = Movies(title=movie_title, release_date=movie_release_date)
            movie.insert()

            movies = Movies.query.order_by(Movies.id).all()
            formatted_movies = [m.format() for m in movies]
            if len(formatted_movies) == 0:
                abort(404)
            return jsonify(
                {
                    "success": True,
                    "created": movie.id,
                    "movies": formatted_movies,
                    "total_movies": len(formatted_movies)
                }
            )
        except Exception as e:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=["PATCH"])
    @requires_auth('patch:actors')
    def update_actors(payload, actor_id):
        body = request.get_json()
        if not body:
            abort(400)
        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        
        new_name = body.get("name", None)
        new_age = body.get("age", None)
        new_gender = body.get("gender", None)

        if not new_age and not new_name and not new_gender:
            abort(400)
        
        try:
            if new_name:
                actor.name = new_name
            if new_age:
                actor.age = new_age
            if new_gender:
                actor.gender = new_gender
            actor.update()
            return jsonify({
                "success": True,
                "actor": actor.id
            })
        except Exception as e:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=["PATCH"])
    @requires_auth('patch:movies')
    def update_movies(payload, movie_id):
        body = request.get_json()
        if not body:
            abort(400)
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        movie_title = body.get("title", None)
        release_date = body.get("release_date", None)
        if not movie_title and not release_date:
            abort(400)

        try:
            if movie_title:
                movie.title = movie_title
            if release_date:
                movie.release_date = release_date
            movie.update()
            return jsonify({
                "success": True,
                "movie": movie.id
            })
        except Exception as e:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=["DELETE"])
    @requires_auth('delete:actors')
    def delete_actors(payload, actor_id):
        try:
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            actor.delete()
            return jsonify({
                "success": True,
                "deleted": actor_id
            })
        except Exception as e:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movies(payload, movie_id):
        try:
            movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            movie.delete()
            return jsonify({
                "success": True,
                "deleted": movie_id
            })
        except Exception as e:
            abort(422)

    # Error Handlers Below:

    @app.errorhandler(AuthError)
    def auth_error_handler(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            "message": e.error['description']
        }), e.status_code

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
            }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422
    
    return app

app = create_app()

if __name__ == '__main__':
    app.debug = True
    app.run(port=3000)
