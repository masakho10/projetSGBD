import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mysql.connector


plt.rcParams["axes.prop_cycle"] = plt.cycler(
    color=["#4C2A85", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC"])

# Connexion à la base de données
# (Remplacer les paramètres par les vôtres)
connection = mysql.connector.connect(host='localhost',
                                    user='opencart',
                                    password='passer',
                                    database='opencart')

# Créer un curseur pour exécuter des requêtes SQL
cursor = connection.cursor()

# Requetes pour recuperer les donnees du nombre de commandes par jour
cursor.execute("SELECT COUNT(*) AS nombre_commandes, DATE(date_added,'%D') AS Jour_commande FROM oc_order GROUP BY DATE(date_added) ORDER BY date_commande ASC")
nombre_commandes = cursor.fetchone()[0]
Jour_commande = cursor.fetchone()[1]


# Requetes pour recuperer le nombre d'elements de chaque produits
cursor.execute("SELECT p.product_id, p.name, COUNT(*) AS quantity FROM oc_product p INNER JOIN oc_product_to_category pc ON p.product_id = pc.product_id GROUP BY p.product_id, p.name ORDER BY quantity ASC limit 5")
nom_produits = cursor.fetchone()[0]
quantite = cursor.fetchone()[1]



# Requetes pour recuperer le nombre de visites par heure 
cursor.execute("SELECT DATE_FORMAT(date_added, '%H') AS heure, COUNT(*) AS nombre_visites FROM `oc_customer_session` WHERE date_added BETWEEN '2023-03-30' AND '2023-03-30' GROUP BY heure ORDER BY heure ASC")
heure = cursor.fetchone()[0]
nombre_visites = cursor.fetchone()[1]

# Requetes pour recuperer le nombre d'erreurs serveurs par jour 
cursor.execute("SELECT DATE(error_date) AS date, COUNT(*) AS error_count FROM `oc_error_log` GROUP BY DATE(error_date) ORDER BY date ASC")
Date_error = cursor.fetchone()[0]
error_count = cursor.fetchone()[1]


#Requetes pour recuperer le statut des stock
cursor.execute("SELECT p.model, p.quantity FROM oc_product p WHERE p.quantity <= 10;")
low_stock_products = cursor.fetchall()
low_stock_text = "\n".join(["{} - {}".format(product[0], product[1]) for product in low_stock_products])


#Requetes pour recuperer le nombre de nouveaux utilisateurs par mois
cursor.execute("SELECT COUNT(*) AS new_users, MONTH(date_added) AS month FROM `oc_customer` WHERE date_added BETWEEN '2023-01-01' AND '2023-12-31' GROUP BY MONTH(date_added) ORDER BY month ASC;")
new_users=cursor.fetchone()[0]
mois=cursor.fetchone()[1]





# Chart 1: Bar chart of sales of top 5 prooducts
fig1, ax1 = plt.subplots()
ax1.bar(nom_produits, quantite)
ax1.set_title("Top 5 produits")
ax1.set_xlabel("Produit")
ax1.set_ylabel("quantite")
# plt.show()

# Chart 2: Horizontal bar chart of number of orders per day
fig2, ax2 = plt.subplots()
ax2.barh(list(nombre_commandes), Jour_commande)
ax2.set_title("Nombre de commandes par jours")
ax2.set_xlabel("Nombre de commandes")
ax2.set_ylabel("Jours")
# plt.show()

# Chart 3: Pie chart of product data
fig3, ax3 = plt.subplots()
ax3.pie(low_stock_text, labels="Stock statuts", autopct='%1.1f%%')
ax3.set_title("Statuts des stocks")
# plt.show()

# Chart 4: Line chart of number of visit per hour
fig4, ax4 = plt.subplots()
ax4.plot(list(heure), list(nombre_visites))
ax4.set_title("Nombre de visites par heures")
ax4.set_xlabel("Heures")
ax4.set_ylabel("Nombre de visites")
# plt.show()

# Chart 5: Area chart of inventory by month
fig5, ax5 = plt.subplots()
ax5.fill_between(new_users,mois)
ax5.set_title("Nombre d'utilisateurs par mois")
ax5.set_xlabel("Mois")
ax5.set_ylabel("Nombre d'utilisateurs")
# plt.show()

# Create a window and add charts
root = tk.Tk()
root.title("Dashboard")
root.state('zoomed')

side_frame = tk.Frame(root, bg="#4C2A85")
side_frame.pack(side="left", fill="y")

label = tk.Label(side_frame, text="Dashboard", bg="#4C2A85", fg="#FFF", font=25)
label.pack(pady=50, padx=20)

charts_frame = tk.Frame(root)
charts_frame.pack()

upper_frame = tk.Frame(charts_frame)
upper_frame.pack(fill="both", expand=True)

canvas1 = FigureCanvasTkAgg(fig1, upper_frame)
canvas1.draw()
canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

canvas2 = FigureCanvasTkAgg(fig2, upper_frame)
canvas2.draw()
canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)

canvas3 = FigureCanvasTkAgg(fig3, upper_frame)
canvas3.draw()
canvas3.get_tk_widget().pack(side="left", fill="both", expand=True)

lower_frame = tk.Frame(charts_frame)
lower_frame.pack(fill="both", expand=True)

canvas4 = FigureCanvasTkAgg(fig4, lower_frame)
canvas4.draw()
canvas4.get_tk_widget().pack(side="left", fill="both", expand=True)

canvas5 = FigureCanvasTkAgg(fig5, lower_frame)
canvas5.draw()
canvas5.get_tk_widget().pack(side="left", fill="both", expand=True)

root.mainloop()
