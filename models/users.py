from config.database import Base

# Map it to the class
Customer = Base.classes.customer # Assurez-vous que 'customers' est le nom exact de la table dans la base de données
Administrator = Base.classes.administrator
UserLogin = Base.classes.userlogin
AdminLogin = Base.classes.adminlogin