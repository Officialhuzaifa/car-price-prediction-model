import pandas as pd
import numpy as np
import pickle as pk
import streamlit as st
import base64

# Function to set a background image
def set_background_image(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Call the function with the image file path
set_background_image('huzaifa.jpg')

st.header("Car Price Prediction Model 🚗")

# Load the model
with open('model.pkl', 'rb') as model_file:
    model = pk.load(model_file)

# Load dataset
cars_Data = pd.read_csv('Cardetails.csv')

# Extract brand and model names from car name
def get_brand_name(car_name):
    return car_name.split(' ')[0]  # Extract the brand (first word)

def get_car_model(car_name):
    return ' '.join(car_name.split(' ')[1:])  # Extract the model (rest of the name)

# Add columns for brand and model in the DataFrame
cars_Data['brand'] = cars_Data['name'].apply(get_brand_name)
cars_Data['model'] = cars_Data['name'].apply(get_car_model)

# Create a dictionary to map car brands to their numerical values
brand_mapping = {
    'Maruti': 1, 'Skoda': 2, 'Honda': 3, 'Hyundai': 4, 'Toyota': 5, 'Ford': 6, 'Renault': 7,
    'Mahindra': 8, 'Tata': 9, 'Chevrolet': 10, 'Datsun': 11, 'Jeep': 12, 'Mercedes-Benz': 13,
    'Mitsubishi': 14, 'Audi': 15, 'Volkswagen': 16, 'BMW': 17, 'Nissan': 18, 'Lexus': 19,
    'Jaguar': 20, 'Land': 21, 'MG': 22, 'Volvo': 23, 'Daewoo': 24, 'Kia': 25, 'Fiat': 26,
    'Force': 27, 'Ambassador': 28, 'Ashok': 29, 'Isuzu': 30, 'Opel': 31
}

# Replace car brands with numerical values using the mapping dictionary
cars_Data['brand'].replace(brand_mapping, inplace=True)

# Create a list of brands with their numeric values to display in the selectbox
brand_options = [f"{brand} ({value})" for brand, value in brand_mapping.items()]

# Select car brand and extract numeric value from the selection
selected_brand_option = st.selectbox('Select Car Brand', brand_options)
selected_brand = int(selected_brand_option.split('(')[-1].strip(')'))  # Extract the numeric value

# Filter models based on the selected brand
filtered_models = cars_Data[cars_Data['brand'] == selected_brand]['model'].unique()
selected_model = st.selectbox('Select Car Model', filtered_models)

# Add a color dropdown
colors = ['Red 🔴', 'Blue 🔵', 'Black ⚫', 'White ⚪', 'Gold 🌕', 'Purple 🟣', 'Green 🟢', 'Yellow 🟡', 'Orange 🟠', 'Brown 🟤']
selected_color = st.selectbox('Select Car Color 🔴🟠🟡🟢🔵🟣', colors)

# Add a tire dropdown
tire_types = ['Summer Tires', 'Winter Tires', 'All-Season Tires', 'Performance Tires', 'Off-Road Tires']
selected_tire = st.selectbox('Select Tire Type', tire_types)

accessories = ['GPS Navigation', 'Sunroof', 'Leather Seats', 'Backup Camera', 'Bluetooth', 'Parking Sensors', 
               'Heated Seats', 'Alloy Wheels', 'Fog Lights', 'Airbags', 'Remote Start']

# Add an accessory selection option
selected_accessories = st.multiselect('Select Car Accessories', accessories)

# Convert accessories into a numerical value (optional)
# Here, we simply count the number of selected accessories as a simple example
# Adjust this to reflect more complex pricing changes if desired
num_accessories = len(selected_accessories)

# Other inputs
year = st.slider('Car Manufacture Year', 1994, 2024)
km_driven = st.slider('KM Driven', 1, 2000000)
fuel = st.selectbox('Fuel Type', cars_Data['fuel'].unique())
seller_type = st.selectbox('Seller Type', cars_Data['seller_type'].unique())
transmission = st.selectbox('Transmission Type', cars_Data['transmission'].unique())
owner = st.selectbox('Owner Type', cars_Data['owner'].unique())
mileage = st.slider('Car Mileage (km/l)', 10, 40)
engine = st.slider('Engine Capacity (cc)', 700, 5000)
max_power = st.slider('Maximum Power (bhp)', 0, 200)
seats = st.slider('Seats', 4, 10)

# Add an input field for Old Showroom Price
old_showroom_price = st.number_input('Enter old showroom  Price (when you buy this car thar price) in ₹', min_value=0, value=0, step=1000)

# Combine brand and model into 'name' as expected by the model
# Here 'name' is the numeric value assigned to the selected brand
combined_name = selected_brand

# Predict the price when the button is clicked
if st.button("Predict"):
    input_data_model = pd.DataFrame(
        [[0, combined_name, year, km_driven, fuel, seller_type, transmission, owner, mileage, engine, max_power, seats]],
        columns=['index', 'name', 'year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner', 'mileage', 'engine', 'max_power', 'seats']
    )
    
    # Data transformation: Encode categorical features (ensure encoding matches training data)
    input_data_model['owner'].replace(['First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner', 'Test Drive Car'], [1, 2, 3, 4, 5], inplace=True)
    input_data_model['fuel'].replace(['Diesel', 'Petrol', 'LPG', 'CNG'], [1, 2, 3, 4], inplace=True)
    input_data_model['seller_type'].replace(['Individual', 'Dealer', 'Trustmark Dealer'], [1, 2, 3], inplace=True)
    input_data_model['transmission'].replace(['Manual', 'Automatic'], [1, 2], inplace=True)

    try:
    # Predict car price
        car_price = model.predict(input_data_model)

    # Ensure the predicted price is not negative
        predicted_price = max(car_price[0], 0)  # Set negative prices to 0 or set a minimum threshold
    
    # Displaying the predicted price in a big and centered format
        st.markdown(
        f'<h1 style="text-align: center; color: #4CAF50;">Predicted Car Price: ₹{predicted_price:.2f}</h1>', unsafe_allow_html=True )
        
        st.markdown(
        """
         ### Factors Affecting Car Price:
         - **Make and Model**: Some brands and models retain value better.
        - **Year**: Newer cars typically cost more, but depreciation affects price.
        - **Mileage**: High mileage can lower the car’s value.
        - **Fuel Type**: Diesel cars might be more expensive than petrol cars in some regions.
        - **Transmission Type**: Automatic Cars May Cost more comparing to manual cars.
        """)
         # Display selected accessories
        st.markdown("### Selected Accessories:")
        if selected_accessories:
            st.write(", ".join(selected_accessories))
        else:
            st.write("No accessories selected.")
            
    # Display clickable link to buy a second-hand car
        st.markdown(
        f'<h3 style="text-align: center; color: #4CAF51;">For Sell Your Used  Car <a href="https://www.cardekho.com/sell-used-car" target="_blank">click here</a>,</h3>'
        f'<h3 style="text-align: center; color: #4CAF51;">For Buy Used Cars <a href="https://www.cardekho.com/usedCars" target="_blank">click here</a>.</h3>', 
        unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error in prediction: {e}")
