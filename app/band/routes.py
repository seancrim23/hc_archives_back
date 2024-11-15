#TODO build out routes for band functionality
#create band
#update band
#get band
#delete band
#get list of bands
#think about subquery endpoints...

from flask import current_app, url_for, request
import sqlalchemy as sa
from app import db
from app.models import Band
from app.band import bp

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Band)
    bands = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('band.index', page=bands.next_num) if bands.has_next else None
    prev_url = url_for('band.index', page=bands.prev_num) if bands.has_prev else None
    return {'bands': bands, 'next': next_url, 'prev': prev_url}

#TODO finish building out band endpoints
@bp.route('/band/<id>')
def band(id):
    #get band -> get all releases -> get reviews
    band = db.first_or_404(sa.select(Band).where(Band.id == id))
    releases = db.session.execute(band.releases.select()).scalars()
    release_list = []
    for release in releases:
        reviews = release.reviews.select()
        review_count = len(reviews)
        avg_review = sum(reviews.score) / review_count
        release_list.append({
            'release': release,
            'review_count': review_count,
            'avg_review': avg_review
        })
    return {'band': band, 'releases': release_list}
