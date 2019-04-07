from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Creates an SQLite database connection with the restaurantmenu database
engine = create_engine('sqlite:///restaurantmenu.db')
# Binds the engine with the database objects model
Base.metadata.bind = engine
# Opens a section with the dataase
DBSession = sessionmaker(bind = engine)
# Creates an instance of the database section
session = DBSession()

### Create
# # Creates an entity Restaurant
# myFirstRestaurant = Restaurant(name = "Pizza Palace")
# # Puts the Restaurant entity into a "staging" zone on the database
# session.add(myFirstRestaurant)
# # Stores the entity into the database
# session.commit()
# # Finds a table called Restaurant and retrieves all the instances in that table.
# session.query(Restaurant).all()

# # Creates a menu item menu entity
# cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with all\
#     natural ingredients and fresh muzzarella", course="Entree", price="$8.99",
#     restaurant = myFirstRestaurant)
# # Puts the menu item entity into the database
# session.add(cheesepizza)
# # Stores the menu item entity into the database
# session.commit()
# # Finds a table called MenuItem and retrieves all the instances in that table.
# session.query(MenuItem).all()

# Iterate over database items
# results = session.query(MenuItem).all()

# for menuItem in results:
#     print menuItem.__dict__.values()[1:]

### Update an existing entity from the database
# veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
# for veggieBurger in veggieBurgers:
#     print veggieBurger.__dict__.values()[1:]

# UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 11).one()
# print UrbanVeggieBurger.__dict__.keys()[:]
# print UrbanVeggieBurger.__dict__.values()[1:]

# UrbanVeggieBurger.price = '$2.99'
# session.add(UrbanVeggieBurger)
# session.commit()

# UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 11).one()
# print UrbanVeggieBurger.__dict__.keys()[:]
# print UrbanVeggieBurger.__dict__.values()[1:]

### Delete an item from the database
spinachIC = session.query(MenuItem).filter_by(name =  'Spinach Ice Cream').one()
session.delete(spinachIC)
session.commit()



