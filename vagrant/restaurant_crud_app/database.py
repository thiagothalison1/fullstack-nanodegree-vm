from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db') # Creates an SQLite database connection with the restaurantmenu database
Base.metadata.bind = engine # Binds the engine with the database objects model
DBSession = sessionmaker(bind = engine) # Opens a section with the dataase
session = DBSession() # Creates an instance of the database section

def get_restaurants():
    restaurants = session.query(Restaurant).all()
    return restaurants

def create_restaurant(restaurant_name):
    new_restaurant = Restaurant(name = restaurant_name)
    session.add(new_restaurant)
    session.commit()

def edit_restaurant(restaurant_id, new_name):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    restaurant.name = new_name
    session.add(restaurant)
    session.commit()

def delete_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    session.delete(restaurant)
    session.commit()  

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
# spinachIC = session.query(MenuItem).filter_by(name =  'Spinach Ice Cream').one()
# session.delete(spinachIC)
# session.commit()



