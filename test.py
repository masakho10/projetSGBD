import tkinter as tk
import mysql.connector

class OpenCartMonitor(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("OpenCart Monitor") 
        self.geometry("800x600")

        self.grid = tk.Frame(self)
        self.grid.pack(expand=True, fill=tk.BOTH)

        self.create_widgets()
        self.populate_data()

    def create_widgets(self):
        # Header
        header_label = tk.Label(self.grid, text="OpenCart Monitoring Dashboard", font=("Helvetica", 16, "bold"), fg="white", bg="blue")
        header_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20), sticky="ew")

        # Total Orders
        self.label_orders = tk.Label(self.grid, text="Total Orders: ", font=("Helvetica", 12, "bold"), fg="white", bg="green")
        self.label_orders.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # New Users
        self.label_new_users = tk.Label(self.grid, text="New Users: ", font=("Helvetica", 12, "bold"), fg="white", bg="orange")
        self.label_new_users.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Total Visits
        self.label_total_visits = tk.Label(self.grid, text="Total Visits: ", font=("Helvetica", 12, "bold"), fg="white", bg="purple")
        self.label_total_visits.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        # Conversion Rate
        self.label_conversion_rate = tk.Label(self.grid, text="Conversion Rate: ", font=("Helvetica", 12, "bold"), fg="white", bg="cyan")
        self.label_conversion_rate.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        # Top 10 Products
        self.label_top_products = tk.Label(self.grid, text="Top 10 Products: ", font=("Helvetica", 12, "bold"), fg="white", bg="brown")
        self.label_top_products.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        # Stock Status
        self.label_stock_status = tk.Label(self.grid, text="Stock Status: ", font=("Helvetica", 12, "bold"), fg="white", bg="teal")
        self.label_stock_status.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        # Server Errors
        self.label_server_errors = tk.Label(self.grid, text="Server Errors: ", font=("Helvetica", 12, "bold"), fg="white", bg="red")
        self.label_server_errors.grid(row=7, column=0, padx=10, pady=10, sticky="w")

    def populate_data(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="opencart",
            password="passer",
            database="opencart"
        )
        cursor = connection.cursor()

        # Execute SQL queries
        cursor.execute("SELECT COUNT(*) FROM oc_order;")
        total_orders = cursor.fetchone()[0]
        self.label_orders.config(text="Total Orders: {}".format(total_orders))

        cursor.execute("SELECT COUNT(*) FROM oc_customer WHERE date_added >= '2024-01-01 00:00:00' AND date_added <= '2024-03-31 23:59:59'")
        new_users = cursor.fetchone()[0]
        self.label_new_users.config(text="New Users: {}".format(new_users))

        cursor.execute("SELECT COUNT(*) FROM oc_customer_online WHERE date_added >= '2024-01-01 00:00:00' AND date_added <= '2024-03-31 23:59:59'")
        total_visits = cursor.fetchone()[0]
        self.label_total_visits.config(text="Total Visits: {}".format(total_visits))

        # Calculate conversion rate
        if total_visits > 0:
            conversion_rate = total_orders / total_visits
        else:
            conversion_rate = 0
        self.label_conversion_rate.config(text="Conversion Rate: {:.2f}%".format(conversion_rate * 100))

        cursor.execute("SELECT p.model, p.quantity, pd.name FROM oc_product p JOIN oc_product_description pd ON p.product_id = pd.product_id ORDER BY p.quantity DESC LIMIT 10")
        top_products = cursor.fetchall()
        products_text = "\n".join(["{} - {} - {}".format(product[0], product[1], product[2]) for product in top_products])
        self.label_top_products.config(text="Top 10 Products:\n{}".format(products_text))

        cursor.execute("SELECT p.model, p.quantity FROM oc_product p WHERE p.quantity <= 10;")
        low_stock_products = cursor.fetchall()
        low_stock_text = "\n".join(["{} - {}".format(product[0], product[1]) for product in low_stock_products])
        self.label_stock_status.config(text="Stock Status:\n{}".format(low_stock_text))

        cursor.execute("SELECT COUNT(*) FROM oc_order_history WHERE order_status_id = 0 AND date_added >= '2024-01-01 00:00:00' AND date_added <= '2024-03-31 23:59:59'")
        server_errors = cursor.fetchone()[0]
        self.label_server_errors.config(text="Server Errors: {}".format(server_errors))

        cursor.close()
        connection.close()

if __name__ == "__main__":
    app = OpenCartMonitor()
    app.mainloop()
