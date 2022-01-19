from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with #rest api
from flask_sqlalchemy import SQLAlchemy #for database

app = Flask(__name__) 
api = Api(app) #wrap app in an API, init the fact that app is an API
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # define location of database to be, in relative path
db = SQLAlchemy(app) #wrap app 

class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True) #primary key true -> this field has to be unique
	name = db.Column(db.String(100), nullable=False) #nullable false -> this field has to have info
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	def __repr__(self): #wrapper method, so when print this out, get valid json format
		return f"Video(name = {name}, views = {views}, likes = {likes})"

#############
# ONLY once
#############
#db.create_all() #only call once to instantiate, if keep calling, overrides what we alr have

####################################
# for GET, PUT, DELETE API requests
####################################
video_put_args = reqparse.RequestParser()
#below are the mandatory args
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)

#############################################################
# for PATCH API requests, notice arg fields aren't mandatory
#############################################################
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

##################
# PRE-db
##################
# videos = {}
# def abort_if_video_id_doesnt_exist(video_id):
# 	if video_id not in videos:
# 		abort(404, message = "Video is not valid...")

resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}

class Video(Resource):

	@marshal_with(resource_fields) # when we return, take the values with resource_fields and serialize it in json format
	def get(self, video_id):      # get overloaded in Video resource
		result = VideoModel.query.filter_by(id=video_id).first() #querying db
		if not result:
			abort(404, message="Could not find video with that id")
		return result #return an instance of VideoModel class with given video_id

	@marshal_with(resource_fields)
	def put(self, video_id):	#put overloaded in Video resource
		args = video_put_args.parse_args() #dict to store all the values we store in 
		result = VideoModel.query.filter_by(id=video_id).first()
		if result:
			abort(409, message="Video id taken...")

		video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
		db.session.add(video) #temp add to the current database session
		db.session.commit()   #commit changes made in the session & make them permanent in the db
		return video, 201

	@marshal_with(resource_fields)
	def patch(self, video_id):
		args = video_update_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first() #fileter by video_id and return first() response or "hit"
		if not result:
			abort(404, message="Video doesn't exist, cannot update")

		#check what to update & update
		if args['name']: #not a null val, since in video_update_args parser will auto fill "unfilled args" with null
			result.name = args['name']
		if args['views']:
			result.views = args['views']
		if args['likes']:
			result.likes = args['likes']
		
		#db.session.add(result) #if alr in db, no need to add it in agn
		db.session.commit()

		return result


	def delete(self, video_id):
		abort_if_video_id_doesnt_exist(video_id)
		del videos[video_id]
		return '', 204


api.add_resource(Video, "/video/<int:video_id>") #define root of the resource Video is at "/video/<int:video_id>"

@app.route("/")
def home():
    return "Test"

if __name__ == "__main__": 
	app.run(debug=True)   # debug info for logging, only run in development environment