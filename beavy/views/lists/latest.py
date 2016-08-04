from beavy.blueprints import lists_bp
from beavy.models.object import Object
from beavy.schemas.object import objects_paged
from beavy.utils import fallbackRender, as_page
from beavy.common.rate_limits import rate_limit
from sqlalchemy import desc


@lists_bp.route("latest/")
@rate_limit("2/second; 100/minute; 1000/hour; 1000/day")
@fallbackRender('home.html', 'list')
def latest():
    query = Object.query.by_capability('listed', aborting=False  # noqa
            ).with_my_activities(
            ).order_by(desc('objects.created_at'))
    return objects_paged.dump(as_page(query, error_out=False)).data
