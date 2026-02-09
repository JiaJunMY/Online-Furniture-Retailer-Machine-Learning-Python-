import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import seaborn as sns
import os

df = pd.read_csv('online_furniture_retailer.csv')

#Clean Data Here:
df.drop_duplicates(subset=['order_id'], inplace=True)
df.dropna(inplace=True)
edited_df = pd.read_csv('online_furniture_retailer_cleaned.csv')

sns.set_style("whitegrid")

#Guide
guide = """
-------------------------Main Menu--------------------------
Hi! This is a program for Online Furniture Retailer Sales dataset.

Here are the options you can input here:
1 - Search ID (Order_ID, Customer_ID)
2 - Add new data
3 - View top brands
4 - Predict Total Amount
5 - View Chart
6 - Filter by Category
0 - Exit application
------------------------------------------------------------"""

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

new_data_list = {
    "product_category": "",
    "product_subcategory": "",	
    "brand": "",
    "delivery_status": "",
    "assembly_service_requested": "",	
    "payment_method": "",
    "order_id":	(edited_df["order_id"].max() + 1),
    "customer_id": (edited_df["customer_id"].max() + 1),	
    "product_price": 0.0,	
    "shipping_cost": 0.0,
    "assembly_cost": 0.0,
    "total_amount":	0.0,
    "delivery_window_days":	0,
    "customer_rating": 0.0
}

#Main Menu
def Main():
    while True:
        option_input = 0
        
        try:
            print(guide)
            option_input = int(input("\nWhich number would you like to choose?: "))
        except Exception as e:
            clear_console()
            print("Error, please put in a value number between 1 to 6.")
            continue
        
        clear_console()
        #Option value check here
        if option_input == 1:
            search_records()
        elif option_input == 2:
            try:
                add_new_data(new_data_list, edited_df)
            except Exception as e:
                print(f"Error: {e}")
        elif option_input == 3:
            view_top_items()
        elif option_input == 4:
            predict_outcome()
        elif option_input == 5:
            view_chart()
        elif option_input == 6:
            filter_selections()
        elif option_input == 0:
            print("Qutting the program now.")
            break
        else:
            print("Error, please put in a value number between 1 to 6.")
            continue

#Search Specific Records
def search_records():
    while True:
        try:
            print("""
---------------------Search Records----------------------
Which records would you like to search?
1. Order ID
2. Customer ID
0. Quit
---------------------------------------------------------""")
            
            option = int(input("Enter the number here: "))
        except Exception as e:
            print(f"Error: {e}.")
            return
        else:
            if option == 0:
                clear_console()
                return
            elif option == 1:
                try:
                    orderid_input = int(input("Enter the order ID here (Example: 10053): "))
                    if orderid_input == 0:
                        clear_console()
                        return
                except Exception as e:
                    print(f"Error: {e}")
                    return
                result_df = edited_df[edited_df['order_id'] == orderid_input]
                if result_df.empty:
                    clear_console()
                    print("\nResult is empty.")
                    continue
                print(f"\n{result_df}")
            elif option == 2:
                try:
                    customerid_input = int(input("Enter the customer ID here (Example: 5978): "))
                    if customerid_input == 0:
                        clear_console()
                        return
                except Exception as e:
                    print(f"Error: {e}")
                    return
                result_df = edited_df[edited_df['customer_id'] == customerid_input]
                if result_df.empty:
                    clear_console()
                    print("\nResult is empty.")
                    continue
                clear_console()
                print(f"\n{result_df}")
            else:
                print("Please enter a number between 0-2.")
        continue_search = input("\nWould you like to search again? (Y/N): ").upper()
        if continue_search == 'Y' or continue_search == "YES":
            clear_console()
            continue
        else:
            clear_console()
            break

def new_value(category_selection, new_data_list, edited_df):
    while True:
        try:
            print(f"Option: {category_selection}")
            if category_selection == "price":
                    print("Tip: Ensure the price is above 0!")
                    product_price = float(input("Enter the product price here: "))
                    shipping_cost = float(input("Enter the shipping cost here: "))
                    assembly_cost = 0
                    if str(new_data_list['assembly_service_requested']).strip().lower() == "false":
                        print("Assembly Request is False so default value will be 0.")
                        assembly_cost = 0
                    else:
                        assembly_cost = float(input("Enter the assembly cost here: "))
                        new_data_list["assembly_cost"] = assembly_cost
                    if product_price < 0 or shipping_cost < 0 or assembly_cost < 0:
                        clear_console()
                        print("Error: The price is less than 0. Please input the price above 0.")
                        return
                    total_amount = sum([product_price, shipping_cost, assembly_cost])
                    new_data_list["product_price"] = product_price 
                    new_data_list["shipping_cost"] = shipping_cost
                    new_data_list["total_amount"] = total_amount
                    clear_console()
                    return
            elif category_selection == "delivery_window_days":
                print("Tip: Ensure the days is more than 0!")
                delivery_window_days = int(input("Enter the delivery window days here: "))
                if delivery_window_days < 1:
                    clear_console()
                    print("Error: The delivery window days must be at least a day!")
                    return
                new_data_list["delivery_window_days"] = delivery_window_days
                clear_console()
                return
            elif category_selection == "customer_rating":
                print("Tip: Ensure the rating is between 1 - 5")
                rating = float(input("Enter the rating here: "))
                if rating < 1 or rating > 5:
                    clear_console()
                    print("Error: Rating must be between 1 and 5.")
                    return
                new_data_list["customer_rating"] = rating
                clear_console()
                return
            else:
                x = 1
                unique_list = edited_df[category_selection].unique()
                for i in unique_list:
                    print(f"{x} - {i}")
                    x += 1
                select = int(input(f"Enter the value between 1 - {len(unique_list)}: "))
                if 1 <= select <= len(unique_list):
                    value = unique_list[select - 1]
                    if value in unique_list:
                        new_data_list[category_selection] = value

                        if category_selection == "assembly_service_requested":
                            if str(value).strip().lower() == "false":
                                new_data_list["assembly_cost"] = 0.0
                                new_data_list["total_amount"] = (
                                    new_data_list["product_price"] +
                                    new_data_list["shipping_cost"] +
                                    new_data_list["assembly_cost"]
                                )
                        clear_console()
                        return
                    else:
                        print("Value is not found on the list.")
                else:
                    clear_console()
                    print("Error: Please select the number within the range.")
            if str(new_data_list['assembly_service_requested']).strip().lower() == "false":
                new_data_list['assembly_cost'] = 0.0
                new_data_list['total_amount'] = (
                    new_data_list['product_price'] +
                    new_data_list['shipping_cost'] +
                    new_data_list['assembly_cost'])
        except Exception as e:
            print(f"Error: {e}")

#Adding newly data
def add_new_data(new_data_list, edited_df):
    category_selection = {
        "Product Category": "product_category",
        "Product Subcategory": "product_subcategory",
        "Brand": "brand",
        "Delivery Status": "delivery_status",
        "Assembly Service Requested": "assembly_service_requested",
        "Payment Method": "payment_method",
        "Price": "price", #Product Price, Shipping Cost & Assembly Cost
        "Delivery Days": "delivery_window_days",
        "Customer Rating": "customer_rating"
    }
    while True:
        try:
            x = 1
            print("Tip: Ensure all data is filled up before saving!")
            print("-----------------------Add Items---------------------------")
            print("0 - Back to Main Menu")
            for i in category_selection:
                print(f"{x} - {i}")
                x += 1
            print("10 - Remove all inputs\n11 - Check inputs\n12 - Save inputs")
            print("-----------------------------------------------------------")
            picked_item = int(input("Enter the number here: "))
            clear_console()
            if picked_item == 0:
                clear_console()
                return
            elif 1 <= picked_item <= len(category_selection):
                clear_console()
                new_value(list(category_selection.values())[picked_item - 1], new_data_list, edited_df)
            elif picked_item == 10: #Clearing all data
                    new_data_list.clear()
                    new_data_list.update({
                            "product_category": " ",
                            "product_subcategory": " ",  
                            "brand": " ",
                            "delivery_status": " ",
                            "assembly_service_requested": " ",   
                            "payment_method": " ",
                            "order_id": edited_df["order_id"].max() + 1,
                            "customer_id": edited_df["customer_id"].max() + 1, 
                            "product_price": 0.0,   
                            "shipping_cost": 0.0,
                            "assembly_cost": 0.0,
                            "total_amount": 0.0,
                            "delivery_window_days": 0,
                            "customer_rating": 0.0
                        })
                    print("Data has been resetted!")
                    return
            elif picked_item == 11: #Checking data
                try:
                    clear_console()
                    for i, j in new_data_list.items():
                        print(f"{i}: {j}")
                except Exception as e:
                    print(f"Error: {e}")
                    return
            elif picked_item == 12: #Saving data
                clear_console()
                invalid_fields = [key for key, value in new_data_list.items()
                                if value == "" or 
                                (key == "product_price" and value == 0) or
                                (key == "delivery_window_days" and value == 0) or 
                                (key == "customer_rating" and value == 0)]
                if invalid_fields:
                    print("The following fields are unable to save due to invalid/missing inputs:")
                    for field in invalid_fields:
                        print(f" - {field}")
                    print("Please complete all fields before saving.\n")
                else:
                    try:
                        new_entry_df = pd.DataFrame([new_data_list])
                        edited_df = pd.concat([edited_df, new_entry_df], ignore_index=True)
                        edited_df.to_csv("online_furniture_retailer_cleaned.csv", index=False)
                        print("New data has been saved successfully!")
                        edited_df = pd.read_csv("online_furniture_retailer_cleaned.csv")
                        new_data_list.update({
                                "product_category": "",
                                "product_subcategory": "",	
                                "brand": "",
                                "delivery_status": "",
                                "assembly_service_requested": "",	
                                "payment_method": "",
                                "order_id":	(edited_df["order_id"].max() + 1),
                                "customer_id": (edited_df["customer_id"].max() + 1),	
                                "product_price": 0.0,	
                                "shipping_cost": 0.0,
                                "assembly_cost": 0.0,
                                "total_amount":	0.0,
                                "delivery_window_days":	0,
                                "customer_rating": 0.0})
                    except Exception as e:
                        print(f"Error saving new data: {e}")
        except Exception as e:
            print(f"Error: {e}")

#View Top items
def view_top_items():
    try:
        descending_total_price = edited_df.sort_values(by='total_amount', ascending=False)
        try:
            filter_amount = int(input(f"How much would you like to check? (Max is: {len(descending_total_price)} | '0' to Exit)\nInput here: "))
            clear_console()
        except Exception as e:
            print("Error, please put a value.")

        edited_df_top_items = descending_total_price.head(filter_amount)

        if filter_amount > len(descending_total_price):
            print("Amount has exceeded the value. Please insert an amount less than max.")
        elif filter_amount == 0:
            return ""
        else:
            print(f"\n{edited_df_top_items}")

            chart_confirm = input("Do you want a visualization bar chart? (Y/N): ").upper()
            if chart_confirm == "Y":
                sns_dataset = edited_df.sort_values(by='total_amount', ascending=False).head(filter_amount)
                plt.figure(figsize=(10, 8))
                sns.barplot(x='product_subcategory',
                            y='total_amount',
                            hue='brand',
                            data=sns_dataset,
                            palette='Set2')
                num_brands = len(edited_df_top_items['brand'].unique())
                plt.legend(bbox_to_anchor=(0., 1.05, 1., .102), ncol=(num_brands // 2))
                plt.xlabel("Product Subcategory")
                plt.ylabel("Total Amount (RM)")
                plt.tick_params(axis='x', labelrotation=45)
                plt.tight_layout()
                plt.show()
                clear_console()
            elif chart_confirm == "N":
                clear_console()
                return
            else:
                print("Error.")
    except Exception as e:
        clear_console()
        print(f"Error: Please input a value.")
        return

#Predict sales
def predict_outcome():
    X = edited_df[['product_price', 'shipping_cost', 'assembly_cost']]
    y = edited_df['total_amount']

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    #print(f"Intercept: {model.intercept_:.2f}")
    #for feature, coef in zip(X.columns, model.coef_):
        #print(f"Coefficient for {feature}: {coef:.2f}")
    #print(f"R² value: {r2_score(y, y_pred)}")

    try:
        user_product_price = float(input("Enter product price (RM): "))
        user_shipping_cost = float(input("Enter shipping cost (RM): "))
        user_assembly_cost = float(input("Enter assembly cost (RM): "))

        if user_product_price < 0:
            print("\nError: Product price must be 0 or more.")
            return

        input_edited_df = pd.DataFrame([[user_product_price, user_shipping_cost, user_assembly_cost]],
                                 columns=['product_price', 'shipping_cost', 'assembly_cost'])
        user_predict = model.predict(input_edited_df)[0]
        print(f"\nPredicted Total Amount: RM{user_predict:.2f}")
    except Exception as e:
        print(f"Input error: {e}")
        return
    else:
        plt.figure(figsize=(10, 6))
        plt.scatter(range(len(y)), y, label="Actual", color='blue', marker=".")
        plt.scatter(len(y), user_predict, label="User Predicition", color="green", marker="*")
        plt.xlabel("Transaction Index")
        plt.ylabel("Total Amount (RM)")
        plt.title("Transaction Index vs Total Amount (RM)")
        plt.legend()
        plt.grid(True)
        plt.show()
        clear_console()

#View chart
def view_chart():
    options = (
        #[0, 1, 2, 3, 4, 5]
        ["bar", "product_category", "total_amount", "Average Total Amount (RM) by Product Category", "Product Category", "Total Amount (RM)"],
        ["bar", "product_subcategory", "total_amount", "Average Total Amount (RM) by Product Subcategory", "Product Subcategory", "Total Amount (RM)"],
        ["bar", "brand", "customer_rating", "Average Customer Rating by Brand", "Brand", "Average Rating"],
        ["bar", "delivery_status", "assembly_cost", "Average Total Assembly Cost by Delivery Status", "Delivery Status", "Assembly Cost (RM)"],
        ["scatter", "product_price", "shipping_cost", "Product Price vs Shipping Cost", "Product Price (RM)", "Shipping Cost (RM)"]
    )
    while True:
        try:
            clear_console()
            print("""
-----------------------View Chart---------------------------
1 - Average Total Amount by Product Category/Subcategory (Barplot)
2 - Average Total Amount by Product Subcategory (Barplot)
3 - Average Customer Rating by Brand (Barplot)
4 - Total Assembly Cost by Delivery Status (Barplot)
5 - Product Price vs Shipping Cost (Scatter)
0 - Exit to Previous Page 
------------------------------------------------------------""")
            chart_option = int(input("Enter the number: "))
        except Exception as e:
            print("Invalid input, please enter a number between 0-5.")
            continue
        else:
            if chart_option == 0:
                clear_console()
                break
            elif 1 <= chart_option <= len(options):
                number = chart_option - 1
                palette = sns.color_palette('pastel', n_colors=len(edited_df[options[number][1]].unique()))
                if options[number][0] == "bar":
                    plt.figure(figsize=(10, 6))
                    grouped_edited_df = edited_df.groupby(options[number][1])[options[number][2]].mean().reset_index()
                    sns.barplot(
                        x=grouped_edited_df[options[number][1]],
                        y=grouped_edited_df[options[number][2]],
                        palette=palette,
                        hue=grouped_edited_df[options[number][1]],
                        data=edited_df,
                    )
                    #sns.barplot(x=edited_df[options[number][1]], y=edited_df[options[number][2]], palette=palette, hue=edited_df['brand'], data=edited_df, errorbar=None)
                elif options[number][0] == "scatter":
                    plt.figure(figsize=(15, 10))

                    plt.grid(True, linestyle="--", alpha=0.5)
                    filtered_edited_df = edited_df[edited_df[options[number][2]] < edited_df[options[number][2]].quantile(0.95)]

                    sns.scatterplot(
                        x=filtered_edited_df[options[number][1]],
                        y=filtered_edited_df[options[number][2]], 
                        hue=filtered_edited_df['brand'],
                        alpha=0.75,
                        s=60,
                        data=filtered_edited_df)
                    #num_brand = len(edited_df[options[number][1]].unique())
                    #plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=min(num_brand, 6))

                plt.title(options[number][3])
                plt.xlabel(options[number][4])
                plt.ylabel(options[number][5])
                plt.tick_params(axis='x', labelrotation=45)
                plt.tight_layout()
                plt.show()
            else:
                print("Please input a number between 0-5.")
                continue
    
#Search Category Function Here
def filter_category_function(category_name):
    number = 0
    unique_category = edited_df[category_name].unique()
    print("\n-----------------------Category Names-----------------------")
    for i in unique_category:
        print(f"{number+1} - {i}")
        number += 1
    
    print("0 - Exit to previous page.")
    print("------------------------------------------------------------\n")
    category_search = int(input("Enter the subcategory number to filter: "))
    clear_console()
    selected_category = unique_category[category_search - 1]
    if 1 <= category_search <= len(unique_category):
        result = edited_df[edited_df[category_name].str.contains(selected_category, case=False)]
        print(f"\n{result}")
    elif category_search == 0:
        return ""
    else:
        print(f"Error, try put between 1 and {len(unique_category)}.")

#Filtering
def filter_selections():
    while True:
        try:
            print("""
---------------------Filter Categories----------------------
Which categories would you like to search?

1 - Product Category (Bedroom, Office)
2 - Product Subcategory (Bookshelf, Desk)
3 - Brand (IKEA, Overstock)              
4 - Delivery (In Transit, Pending, Cancelled)              
5 - Payment (Google Pay, PayPal)
0 - Back to Main Menu
------------------------------------------------------------""")    
            option_input = int(input("\nWhich number would you like to search? "))
            clear_console()
        except Exception as e:
            print("Error")

        categories = ['product_category', 'product_subcategory', 'brand', 'delivery_status', 'payment_method']
        selected_option = categories[option_input - 1]
        if option_input == 0:
            break
        elif 1 <= option_input <= len(categories):
            filter_category_function(selected_option)
        else:
            print("Please input the number between 1 to 6.")

#Main here
Main()