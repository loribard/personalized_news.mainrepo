users = {"user1":
            {"name":"lori","password":"hi there"}
            }
def seed_try(users):
	
    
    for key in users.keys():
        print "Key ", key
        print "Value", users[key]
        name = users[key]["name"]
        print "Name: ", name
        password = users[key]["password"]
        print "Password: ", password
       

        # user=User(name=name,password=password)

seed_try(users)