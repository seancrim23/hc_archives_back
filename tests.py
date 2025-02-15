#TODO build this out with unit tests
import unittest
from app import create_app, db
from app.models import Band, User, Release, Review, Track
from config import Config
from flask import jsonify,url_for
import sqlalchemy as sa
import json

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class BandModelCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #get band includes list of all releases and aggregates reviews correctly
    def test_get_band(self):
        b = Band(name='test band', status='active', band_picture='test_band_pic_url.png')
        db.session.add(b)
        db.session.commit()

        u1 = User(username='test_user_1', email='testuser1@gmail.com')
        u2 = User(username='test_user_2', email='testuser2@gmail.com')
        u3 = User(username='test_user_3', email='testuser3@gmail.com')
        db.session.add_all([u1,u2,u3])
        db.session.commit()

        r1 = Release(name='release 1', length=123, art='release_1_art.png', release_type='LP', band=b)
        r2 = Release(name='release 2', length=123, art='release_2_art.png', release_type='EP', band=b)
        r3 = Release(name='release 3', length=123, art='release_3_art.png', release_type='LP', band=b)
        db.session.add_all([r1,r2,r3])
        db.session.commit()

        rev1 = Review(score=10, review_text='very good', release=r1, author=u1)
        rev2 = Review(score=4, review_text='no good', release=r1, author=u2)
        rev3 = Review(score=8, review_text='ok :)', release=r1, author=u3)
        rev4 = Review(score=2, review_text='no good', release=r2, author=u1)
        rev5 = Review(score=10, review_text='very good', release=r2, author=u2)
        rev6 = Review(score=5, review_text='ok', release=r2, author=u3)
        rev7 = Review(score=1, review_text='bad :(', release=r3, author=u1)
        rev8 = Review(score=4, review_text='very good', release=r3, author=u2)
        rev9 = Review(score=10, review_text='very good', release=r3, author=u3)
        db.session.add_all([rev1,rev2,rev3,rev4,rev5,rev6,rev7,rev8,rev9])
        db.session.commit()

        releases = db.session.scalars(b.releases.select()).all()
        release_list = []
        for release in releases:
            review_count = release.reviews_count()
            avg_review = release.avg_review_score()
            release_list.append({
                'release': release.as_dict(),
                'review_count': review_count,
                'avg_review': avg_review
            })
        print({'band': b.as_dict(), 'releases': release_list})

    def test_get_band_endpoint(self):
        b = Band(name='test band', status='active', band_picture='test_band_pic_url.png')
        db.session.add(b)
        db.session.commit()

        u1 = User(username='test_user_1', email='testuser1@gmail.com')
        u2 = User(username='test_user_2', email='testuser2@gmail.com')
        u3 = User(username='test_user_3', email='testuser3@gmail.com')
        db.session.add_all([u1,u2,u3])
        db.session.commit()

        r1 = Release(name='release 1', length=123, art='release_1_art.png', release_type='LP', band=b)
        r2 = Release(name='release 2', length=123, art='release_2_art.png', release_type='EP', band=b)
        r3 = Release(name='release 3', length=123, art='release_3_art.png', release_type='LP', band=b)
        db.session.add_all([r1,r2,r3])
        db.session.commit()

        rev1 = Review(score=10, review_text='very good', release=r1, author=u1)
        rev2 = Review(score=4, review_text='no good', release=r1, author=u2)
        rev3 = Review(score=8, review_text='ok :)', release=r1, author=u3)
        rev4 = Review(score=2, review_text='no good', release=r2, author=u1)
        rev5 = Review(score=10, review_text='very good', release=r2, author=u2)
        rev6 = Review(score=5, review_text='ok', release=r2, author=u3)
        rev7 = Review(score=1, review_text='bad :(', release=r3, author=u1)
        rev8 = Review(score=4, review_text='very good', release=r3, author=u2)
        rev9 = Review(score=10, review_text='very good', release=r3, author=u3)
        db.session.add_all([rev1,rev2,rev3,rev4,rev5,rev6,rev7,rev8,rev9])
        db.session.commit()

        test_band = db.first_or_404(sa.select(Band).where(Band.name == 'test band'))
        assert test_band.as_dict()['name'] == 'test band'

        response = self.app.test_client().get('/band/' + str(test_band.as_dict()['id']))
        band_response = json.loads(response.data.decode('utf-8')).get('band')
        releases_response = json.loads(response.data.decode('utf-8')).get('releases')

        assert response.status_code == 200
        assert band_response['name'] == 'test band'
        assert releases_response[0]['release']['name'] == 'release 1'

    def test_get_all_bands(self):
        b1 = Band(name='test band 1', status='active', band_picture='test_band_pic_url1.png')
        b2 = Band(name='test band 2', status='active', band_picture='test_band_pic_url2.png')
        b3 = Band(name='test band 3', status='active', band_picture='test_band_pic_url3.png')
        b4 = Band(name='test band 4', status='active', band_picture='test_band_pic_url4.png')
        b5 = Band(name='test band 5', status='active', band_picture='test_band_pic_url5.png')
        b6 = Band(name='test band 6', status='active', band_picture='test_band_pic_url6.png')
        b7 = Band(name='test band 7', status='active', band_picture='test_band_pic_url7.png')
        b8 = Band(name='test band 8', status='active', band_picture='test_band_pic_url8.png')
        b9 = Band(name='test band 9', status='active', band_picture='test_band_pic_url9.png')
        db.session.add_all([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        db.session.commit()

        query = sa.select(Band)
        bands = db.paginate(query, page=1, per_page=3, error_out=False)
        #next_url = url_for('band.index', page=bands.next_num) if bands.has_next else None
        #prev_url = url_for('band.index', page=bands.prev_num) if bands.has_prev else None
        band_list = []
        for band in bands.items:
            band_list.append(band.as_dict())
        print({'bands': band_list})

    #TODO build out the pagination cases
    #get all bands pulls expected data
    def test_get_all_bands_endpoint(self):
        b1 = Band(name='test band 1', status='active', band_picture='test_band_pic_url1.png')
        b2 = Band(name='test band 2', status='active', band_picture='test_band_pic_url2.png')
        b3 = Band(name='test band 3', status='active', band_picture='test_band_pic_url3.png')
        b4 = Band(name='test band 4', status='active', band_picture='test_band_pic_url4.png')
        b5 = Band(name='test band 5', status='active', band_picture='test_band_pic_url5.png')
        b6 = Band(name='test band 6', status='active', band_picture='test_band_pic_url6.png')
        b7 = Band(name='test band 7', status='active', band_picture='test_band_pic_url7.png')
        b8 = Band(name='test band 8', status='active', band_picture='test_band_pic_url8.png')
        b9 = Band(name='test band 9', status='active', band_picture='test_band_pic_url9.png')
        b10 = Band(name='test band 5', status='active', band_picture='test_band_pic_url5.png')
        b11 = Band(name='test band 6', status='active', band_picture='test_band_pic_url6.png')
        b12 = Band(name='test band 7', status='active', band_picture='test_band_pic_url7.png')
        b13 = Band(name='test band 8', status='active', band_picture='test_band_pic_url8.png')
        b14 = Band(name='test band 9', status='active', band_picture='test_band_pic_url9.png')
        db.session.add_all([b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14])
        db.session.commit()

        response = self.app.test_client().get('/band/')
        res = json.loads(response.data.decode('utf-8')).get('bands')
        res2 = json.loads(response.data.decode('utf-8')).get('next')
        res3 = json.loads(response.data.decode('utf-8')).get('prev')

        assert response.status_code == 200

    def test_create_band_endpoint(self):
        band = Band(name='test band 1', status='active', band_picture='test_band_pic_url1.png')

        response = self.app.test_client().post('/band/new', json=band.as_dict())
        assert response.status_code == 200

        test_band = db.first_or_404(sa.select(Band).where(Band.name == 'test band 1'))
        assert test_band.as_dict()['name'] == 'test band 1'

    def test_update_band_endpoint(self):
        band = Band(name='test band 1', status='active', band_picture='test_band_pic_url1.png')
        db.session.add(band)
        db.session.commit()

        test_band = db.first_or_404(sa.select(Band).where(Band.name == 'test band 1'))
        assert test_band.as_dict()['name'] == 'test band 1'

        updated_band = Band(name='test band 1', status='inactive', band_picture='test_band_pic_url1.png')

        response = self.app.test_client().post('/band/' + str(test_band.as_dict()['id']) + '/update', json=updated_band.as_dict())
        assert response.status_code == 200

        test_band = db.first_or_404(sa.select(Band).where(Band.name == 'test band 1'))
        assert test_band.as_dict()['status'] == 'inactive'

    def test_delete_band_endpoint(self):
        band = Band(name='test band 1', status='active', band_picture='test_band_pic_url1.png')
        db.session.add(band)
        db.session.commit()

        test_band = db.first_or_404(sa.select(Band).where(Band.name == 'test band 1'))
        assert test_band.as_dict()['name'] == 'test band 1'

        response = self.app.test_client().delete('/band/' + str(test_band.as_dict()['id']) + '/delete')
        assert response.status_code == 200

        test_band = db.session.scalar(sa.select(Band).where(Band.name == 'test band 1'))
        assert test_band is None

class ReleaseModelCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_release_endpoint(self):
        b = Band(name='test band', status='active', band_picture='test_band_pic_url.png')
        db.session.add(b)
        db.session.commit()

        r1 = Release(name='release 1', length=123, art='release_1_art.png', release_type='LP', band=b)
        r2 = Release(name='release 2', length=123, art='release_2_art.png', release_type='EP', band=b)
        r3 = Release(name='release 3', length=123, art='release_3_art.png', release_type='LP', band=b)
        db.session.add_all([r1,r2,r3])
        db.session.commit()

        test_release = db.first_or_404(sa.select(Release).where(Release.name == 'release 1'))
        assert test_release.as_dict()['name'] == 'release 1'

        response = self.app.test_client().get('/release/' + str(test_release.as_dict()['id']))
        release_response = json.loads(response.data.decode('utf-8')).get('release')

        assert response.status_code == 200
        assert release_response['name'] == 'release 1'
    
    def test_create_release_endpoint(self):
        band = Band(name='test band', status='active', band_picture='test_band_pic_url.png')
        db.session.add(band)
        db.session.commit()

        r1 = Release(name='release 1', length=123, art='release_1_art.png', release_type='LP', band=band)

        test_band = db.first_or_404(sa.select(Band).where(Band.name == 'test band'))
        assert test_band.as_dict()['name'] == 'test band'

        response = self.app.test_client().post('/release/new?band=' + str(test_band.as_dict()['id']), json=r1.as_dict())
        assert response.status_code == 200

        test_release = db.first_or_404(sa.select(Release).where(Release.name == 'release 1'))
        assert test_release.as_dict()['name'] == 'release 1'

    def test_update_release_endpoint(self):
        band = Band(name='test band 1', status='active', band_picture='test_band_pic_url1.png')
        db.session.add(band)
        db.session.commit()

        r1 = Release(name='release 1', length=123, art='release_1_art.png', release_type='LP', band=band)
        db.session.add(r1)
        db.session.commit()

        test_release = db.first_or_404(sa.select(Release).where(Release.name == 'release 1'))
        assert test_release.as_dict()['name'] == 'release 1'

        updated_release = Release(name='release 1', length=123, art='release_1_art.png', release_type='demo', band=band)

        response = self.app.test_client().post('/release/' + str(test_release.as_dict()['id']) + '/update', json=updated_release.as_dict())
        assert response.status_code == 200

        test_release = db.first_or_404(sa.select(Release).where(Release.name == 'release 1'))
        assert test_release.as_dict()['release_type'] == 'demo'

    def test_delete_release_endpoint(self):
        band = Band(name='test band 1', status='active', band_picture='test_band_pic_url1.png')
        db.session.add(band)
        db.session.commit()

        r1 = Release(name='release 1', length=123, art='release_1_art.png', release_type='LP', band=band)
        db.session.add(r1)
        db.session.commit()

        test_release = db.first_or_404(sa.select(Release).where(Release.name == 'release 1'))
        assert test_release.as_dict()['name'] == 'release 1'

        response = self.app.test_client().delete('/release/' + str(test_release.as_dict()['id']) + '/delete')
        assert response.status_code == 200

        test_release = db.session.scalar(sa.select(Release).where(Release.name == 'release 1'))
        assert test_release is None

class ReviewModelCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_review_endpoint(self):
        b = Band(name='test band', status='active', band_picture='test_band_pic_url.png')
        db.session.add(b)
        db.session.commit()

        rel1 = Release(name='release 1', length=123, art='release_1_art.png', release_type='LP', band=b)
        db.session.add(rel1)
        db.session.commit()

        u = User(username='test user', email='testuser1@test.com')
        db.session.add(u)
        db.session.commit()

        test_release = db.first_or_404(sa.select(Release).where(Release.name == 'release 1'))
        assert test_release.as_dict()['name'] == 'release 1'

        test_user = db.first_or_404(sa.select(User).where(User.username == 'test user'))
        assert test_user.as_dict()['username'] == 'test user'

        rev1 = Review(score=5, review_text='test review 1', release_id=test_release.id, release=rel1, user_id=test_user.id, author=u)
        db.session.add(rev1)
        db.session.commit()

        test_review = db.first_or_404(sa.select(Review).where(Review.review_text == 'test review 1'))
        assert test_review.as_dict()['review_text'] == 'test review 1'

        response = self.app.test_client().get('/review/' + str(test_review.as_dict()['id']))
        review_response = json.loads(response.data.decode('utf-8')).get('review')

        assert response.status_code == 200
        assert review_response['review_text'] == 'test review 1'
    
    def test_create_review_endpoint(self):
        b = Band(name='test band', status='active', band_picture='test_band_pic_url.png')
        db.session.add(b)
        db.session.commit()

        rel1 = Release(name='release 1', length=123, art='release_1_art.png', release_type='LP', band=b)
        db.session.add(rel1)
        db.session.commit()

        u = User(username='test user', email='testuser1@test.com')
        db.session.add(u)
        db.session.commit()

        test_release = db.first_or_404(sa.select(Release).where(Release.name == 'release 1'))
        assert test_release.as_dict()['name'] == 'release 1'

        test_user = db.first_or_404(sa.select(User).where(User.username == 'test user'))
        assert test_user.as_dict()['username'] == 'test user'

        rev1 = Review(score=5, review_text='test review 1', release_id=test_release.id, release=rel1, user_id=test_user.id, author=u)

        response = self.app.test_client().post('/review/new?release=' + str(test_release.as_dict()['id']) + '&user=' + str(test_user.as_dict()['id']), json=rev1.as_dict())
        assert response.status_code == 200

        test_review = db.first_or_404(sa.select(Review).where(Review.review_text == 'test review 1'))
        assert test_review.as_dict()['review_text'] == 'test review 1'

    def test_update_review_endpoint(self):
        b = Band(name='test band', status='active', band_picture='test_band_pic_url.png')
        db.session.add(b)
        db.session.commit()

        rel1 = Release(name='release 1', length=123, art='release_1_art.png', release_type='LP', band=b)
        db.session.add(rel1)
        db.session.commit()

        u = User(username='test user', email='testuser1@test.com')
        db.session.add(u)
        db.session.commit()

        test_release = db.first_or_404(sa.select(Release).where(Release.name == 'release 1'))
        assert test_release.as_dict()['name'] == 'release 1'

        test_user = db.first_or_404(sa.select(User).where(User.username == 'test user'))
        assert test_user.as_dict()['username'] == 'test user'

        rev1 = Review(score=5, review_text='test review 1', release_id=test_release.id, release=rel1, user_id=test_user.id, author=u)
        db.session.add(rev1)
        db.session.commit()

        test_review = db.first_or_404(sa.select(Review).where(Review.review_text == 'test review 1'))
        assert test_review.as_dict()['review_text'] == 'test review 1'

        updated_rev1 = Review(score=5, review_text='updated test review 1')

        response = self.app.test_client().post('/review/' + str(test_review.as_dict()['id']) + '/update', json=updated_rev1.as_dict())
        assert response.status_code == 200

        test_review = db.first_or_404(sa.select(Review).where(Review.review_text == 'updated test review 1'))
        assert test_review.as_dict()['review_text'] == 'updated test review 1'

    def test_delete_review_endpoint(self):
        b = Band(name='test band', status='active', band_picture='test_band_pic_url.png')
        db.session.add(b)
        db.session.commit()

        rel1 = Release(name='release 1', length=123, art='release_1_art.png', release_type='LP', band=b)
        db.session.add(rel1)
        db.session.commit()

        u = User(username='test user', email='testuser1@test.com')
        db.session.add(u)
        db.session.commit()

        test_release = db.first_or_404(sa.select(Release).where(Release.name == 'release 1'))
        assert test_release.as_dict()['name'] == 'release 1'

        test_user = db.first_or_404(sa.select(User).where(User.username == 'test user'))
        assert test_user.as_dict()['username'] == 'test user'

        rev1 = Review(score=5, review_text='test review 1', release_id=test_release.id, release=rel1, user_id=test_user.id, author=u)
        db.session.add(rev1)
        db.session.commit()

        test_review = db.first_or_404(sa.select(Review).where(Review.review_text == 'test review 1'))
        assert test_review.as_dict()['review_text'] == 'test review 1'

        response = self.app.test_client().delete('/review/' + str(test_review.as_dict()['id']) + '/delete')
        assert response.status_code == 200

        test_review = db.session.scalar(sa.select(Review).where(Review.review_text == 'test review 1'))
        assert test_review is None

class TrackModelCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_track_endpoint(self):
        b = Band(name='test band', status='active', band_picture='test_band_pic_url.png')
        db.session.add(b)
        db.session.commit()

        rel1 = Release(name='release 1', length=123, art='release_1_art.png', release_type='LP', band=b)
        db.session.add(rel1)
        db.session.commit()

        test_release = db.first_or_404(sa.select(Release).where(Release.name == 'release 1'))
        assert test_release.as_dict()['name'] == 'release 1'

        t1 = Track(name='test track', track_number=1, length=123, lyrics='test lyrics', release=rel1)
        db.session.add(t1)
        db.session.commit()

        test_track = db.first_or_404(sa.select(Track).where(Track.name == 'test track'))
        assert test_track.as_dict()['name'] == 'test track'

        response = self.app.test_client().get('/track/' + str(test_track.as_dict()['id']))
        track_response = json.loads(response.data.decode('utf-8')).get('track')

        assert response.status_code == 200
        assert track_response['name'] == 'test track'
    
    def test_create_track_endpoint(self):
        b = Band(name='test band', status='active', band_picture='test_band_pic_url.png')
        db.session.add(b)
        db.session.commit()

        rel1 = Release(name='release 1', length=123, art='release_1_art.png', release_type='LP', band=b)
        db.session.add(rel1)
        db.session.commit()

        test_release = db.first_or_404(sa.select(Release).where(Release.name == 'release 1'))
        assert test_release.as_dict()['name'] == 'release 1'

        t = Track(name='test track', track_number=1, length=123, lyrics='test lyrics')

        response = self.app.test_client().post('/track/new?release=' + str(test_release.as_dict()['id']), json=t.as_dict())
        assert response.status_code == 200

        test_track = db.first_or_404(sa.select(Track).where(Track.name == 'test track'))
        assert test_track.as_dict()['name'] == 'test track'

    def test_update_track_endpoint(self):
        b = Band(name='test band', status='active', band_picture='test_band_pic_url.png')
        db.session.add(b)
        db.session.commit()

        rel1 = Release(name='release 1', length=123, art='release_1_art.png', release_type='LP', band=b)
        db.session.add(rel1)
        db.session.commit()

        test_release = db.first_or_404(sa.select(Release).where(Release.name == 'release 1'))
        assert test_release.as_dict()['name'] == 'release 1'

        t1 = Track(name='test track', track_number=1, length=123, lyrics='test lyrics', release=rel1)
        db.session.add(t1)
        db.session.commit()

        test_track = db.first_or_404(sa.select(Track).where(Track.name == 'test track'))
        assert test_track.as_dict()['name'] == 'test track'

        updated_t1 = Track(name='updated test track', track_number=1, length=123, lyrics='test lyrics')

        response = self.app.test_client().post('/track/' + str(test_track.as_dict()['id']) + '/update', json=updated_t1.as_dict())
        assert response.status_code == 200

        test_track = db.first_or_404(sa.select(Track).where(Track.name == 'updated test track'))
        assert test_track.as_dict()['name'] == 'updated test track'

    def test_delete_track_endpoint(self):
        b = Band(name='test band', status='active', band_picture='test_band_pic_url.png')
        db.session.add(b)
        db.session.commit()

        rel1 = Release(name='release 1', length=123, art='release_1_art.png', release_type='LP', band=b)
        db.session.add(rel1)
        db.session.commit()

        test_release = db.first_or_404(sa.select(Release).where(Release.name == 'release 1'))
        assert test_release.as_dict()['name'] == 'release 1'

        t1 = Track(name='test track', track_number=1, length=123, lyrics='test lyrics', release=rel1)
        db.session.add(t1)
        db.session.commit()

        test_track = db.first_or_404(sa.select(Track).where(Track.name == 'test track'))
        assert test_track.as_dict()['name'] == 'test track'

        response = self.app.test_client().delete('/track/' + str(test_track.as_dict()['id']) + '/delete')
        assert response.status_code == 200

        test_track = db.session.scalar(sa.select(Track).where(Track.name == 'test track'))
        assert test_track is None

class UserModelCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_user_endpoint(self):
        u = User(username='test user', email='testuser@gmail.com', password_hash='testuseriscool')
        db.session.add(u)
        db.session.commit()

        test_user = db.first_or_404(sa.select(User).where(User.username == 'test user'))
        assert test_user.as_dict()['username'] == 'test user'

        response = self.app.test_client().get('/user/' + str(test_user.as_dict()['id']))
        user_response = json.loads(response.data.decode('utf-8')).get('user')

        assert response.status_code == 200
        assert user_response['username'] == 'test user'
    
    def test_create_user_endpoint(self):
        user = User(username='test user', email='testuser@gmail.com', password_hash='testuseriscool')

        response = self.app.test_client().post('/user/new', json=user.as_dict())
        assert response.status_code == 200

        test_user = db.first_or_404(sa.select(User).where(User.username == 'test user'))
        assert test_user.as_dict()['username'] == 'test user'

    def test_update_user_endpoint(self):
        u = User(username='test user', email='testuser@gmail.com', password_hash='testuseriscool')
        db.session.add(u)
        db.session.commit()

        test_user = db.first_or_404(sa.select(User).where(User.username == 'test user'))
        assert test_user.as_dict()['username'] == 'test user'

        updated_user = User(username='test user 123', email='testuser@gmail.com', password_hash='testuseriscool')

        response = self.app.test_client().post('/user/' + str(test_user.as_dict()['id']) + '/update', json=updated_user.as_dict())
        assert response.status_code == 200

        test_user = db.first_or_404(sa.select(User).where(User.username == 'test user 123'))
        assert test_user.as_dict()['username'] == 'test user 123'

    def test_delete_user_endpoint(self):
        u = User(username='test user', email='testuser@gmail.com', password_hash='testuseriscool')
        db.session.add(u)
        db.session.commit()

        test_user = db.first_or_404(sa.select(User).where(User.username == 'test user'))
        assert test_user.as_dict()['username'] == 'test user'

        response = self.app.test_client().delete('/user/' + str(test_user.as_dict()['id']) + '/delete')
        assert response.status_code == 200

        test_user = db.session.scalar(sa.select(User).where(User.username == 'test user'))
        assert test_user is None
    
if __name__ == '__main__':
    unittest.main(verbosity=2)