from beavy.blueprints import lists_bp
from beavy.models.object import Object
from beavy.schemas.object import objects_paged
from beavy.utils import fallbackRender, as_page

from sqlalchemy import desc


@lists_bp.route("latest/")
@fallbackRender('home.html')
def latest():
    query = Object.query.by_capability('listed', aborting=False
                  ).with_my_activities(
                  ).order_by(desc('objects.created_at'))
    return objects_paged.dump(as_page(query, error_out=False)).data
