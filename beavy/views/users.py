from beavy.blueprints import users
from beavy.schemas.user import UserProfile
from beavy.utils import fallbackRender

profile = UserProfile()


@users.route("/<user:user>/")
@fallbackRender('home.html', key='user')
def user_index(user):
    return profile.dump(user).data
