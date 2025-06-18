from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with 
from flask_sqlalchemy import SQLAlchemy # Import necessary modules from Flask and Flask-RESTful to database

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def home():
    return {"message": "Video API is running!", "endpoints": ["/video/<id>"]}

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"

with app.app_context():
    db.create_all()
# Easier way to send a request with arguments
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True) #Type of argument needed and error message for what is needed
video_put_args.add_argument("views", type=int, help="Views of video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on video  is required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of video is required")
video_update_args.add_argument("likes", type=int, help="Likes on video  is required")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)  # Use marshalling to format the output
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()  # Query the database for the video with the given ID
        if not result:
            abort(404, message="Video not found")
        return result
    
    @marshal_with(resource_fields)  # Use marshalling to format the output
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()  # Check if the video already exists
        if result:
            abort(409, message= "Video id is taken ")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video,201  # Return the created video with a 201 status code
    
    @marshal_with(resource_fields)  # Use marshalling to format the output
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video not found, cannot update")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']    
        if args['likes']:
            result.likes = args['likes'] 
        db.session.commit()
        return result 
    
    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()  # Fixed: proper database query
        if not result:
            abort(404, message="Video not found")
        db.session.delete(result)  # Fixed: use db.session.delete()
        db.session.commit()
        return '', 204

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)