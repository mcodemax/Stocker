"""Seed file for App"""

from models import User, Portfolio, PortfolioUser, StocksPortfolio
from app import db

db.drop_all()
db.create_all()

User.query.delete()
Portfolio.query.delete()
PortfolioUser.query.delete()
StocksPortfolio.query.delete()

User.register(username='Fname1',password='passy1',email='polka@dot.com',first_name='Polka',last_name='Luiza',image_url='https://media.wired.com/photos/593261cab8eb31692072f129/master/pass/85120553.jpg')
User.register(username='Fname2',password='babyboo5',email='pol@g.com',first_name='Dino',last_name='',image_url='https://ca-times.brightspotcdn.com/dims4/default/b82ff0d/2147483647/strip/true/crop/3200x2134+0+0/resize/840x560!/quality/90/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2F9c%2F24%2F3f451bd6416db701a27794ade9fd%2Fla-et-st-tbe-zoo-san-diego-animal-planet-series.jpg')
User.register(username='Fname3',password='ieatedit3',email='pog@dog.com',first_name='Kol',last_name='Burr')
User.register(username='Fname4',password='somethingt5t',email='mog@gro.com',first_name='Monkey',last_name='Boon')

db.session.commit()

