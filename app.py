from flask import Flask, jsonify
from flask_restx import Api, Resource, fields

# Goal of project: Create API where I can create and manage a dictionary of family members

# Create flask object
app = Flask(__name__)

api = Api(
    app,
    version='1.0',
    title="Family API",
    description="This api allows you to generate and store family data"
)

# Create namespace
ns = api.namespace('family', description='Name space for family api')


# Create class and methods to interact with dictionary

class Family:
    def __init__(self):
        self.family_count = 0
        self.family_dict = {}

    def get(self, member_title=None, member_name=None):
        if self.family_count == 0:
            return "No family dictionary exists. Please create one"
        if (member_title is None and member_name is None) or (member_name is not None and member_title is not None):
            return self.family_dict
        else:
            if member_title is not None:
                return self.family_dict[member_title]
            else:
                temp_key_list = []
                for k, v in self.family_dict.items():
                    if v == member_name:
                        temp_key_list.append(k)
                return self.family_dict[temp_key_list]

    def create(self, member_title, member_name):
        if member_title in self.family_dict.keys():
            return f"The member title: {member_title} is already populated"
        else:
            self.family_dict[member_title] = member_name
            self.family_count = self.family_count + 1
            return self.family_dict, self.family_count

    def delete(self, member_title):
        if member_title in self.family_dict.keys():
            self.family_dict.pop(member_title)
            self.family_count = self.family_count - 1
            return self.family_dict, self.family_count
        else:
            return f"The title {member_title} does not exist. Cannot delete!"

    def update(self, member_title, member_name):
        if member_title in self.family_dict.keys():
            self.family_dict[member_title] = member_name
            return self.family_dict, self.family_count
        else:
            return f"The title {member_title} does not exist. Cannot update!"


# Creating a test family
titles = ['mother', 'father', 'sister',  'brother']
names = ['x', 'y', 'z',  'a']
zipped = zip(titles, names)
fam = Family()
for i, j in zipped:
    fam.create(member_title=i, member_name=j)

# Creating the API

@ns.route('/')
class All(Resource):
    """Get all family members"""
    @ns.doc('List family members')
    def get(self):
        """List all family members"""
        return fam.family_dict


@ns.route('/<string:member_title>/<string:member_name>')
class Some(Resource):
    """Work with single family members"""
    @ns.doc('Get single family member')
    def get(self, member_title):
        return fam.get(member_title=member_title)

    @ns.doc('Add to family dictionary')
    def post(self, member_title, member_name):
        return fam.create(member_title=member_title, member_name=member_name)

    @ns.doc('Delete family members')
    @ns.response(204, 'Family member deleted')
    def delete(self, member_title):
        return fam.delete(member_title=member_title)

    @ns.doc('Update family member in specific title')
    def put(self, member_title, member_name):
        return fam.update(member_title=member_title, member_name=member_name), 200


if __name__ == '__main__':
    app.run(debug=True)