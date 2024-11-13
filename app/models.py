from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

#TODO probably delete but keep here in case i need a many to many table
#followers = sa.Table(
#    'followers',
#    db.metadata,
#    sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'),
#              primary_key=True),
#    sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'),
#              primary_key=True)
#)

class Band(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(25))
    band_picture: so.Mapped[Optional[str]] = so.mapped_column(sa.String(150))

    releases: so.WriteOnlyMapped['Release'] = so.relationship(back_populates='band')

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    reviews: so.WriteOnlyMapped['Review'] = so.relationship(back_populates='author')

class Release(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    #have length in seconds?
    length: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer())
    art: so.Mapped[Optional[str]] = so.mapped_column(sa.String(150))
    release_type: so.Mapped[str] = so.mapped_column(sa.String(10))

    band_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Band.id), index=True)

    band: so.Mapped[Band] = so.relationship(back_populates='releases')

    tracks: so.WriteOnlyMapped['Track'] = so.relationship(back_populates='release')

    reviews: so.WriteOnlyMapped['Review'] = so.relationship(back_populates='release')

class Track(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    length: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer())
    lyrics: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    release_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Release.id), index=True)
    
    release: so.Mapped[Release] = so.relationship(back_populates='tracks')

class Review(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    score: so.Mapped[int] = so.mapped_column(sa.Integer())
    review_text: so.Mapped[str] = so.mapped_column(sa.String(500))

    release_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Release.id), index=True)

    release: so.Mapped[Release] = so.relationship(back_populates='reviews')

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='reviews')
