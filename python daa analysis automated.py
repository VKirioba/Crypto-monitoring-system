import pandas as pd
import matplotlib.pyplot as plt
from powerbiclient import QuickVisualize, get_dataset_config, Report
from powerbiclient.authentication import DeviceCodeLoginAuthentication

# Step 1: Load the Data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Step 2: Data Cleaning
def clean_data(data):
    # Drop missing values
    data = data.dropna()
    
    # Remove duplicates
    data = data.drop_duplicates()
    
    # Convert columns to appropriate data types
    data['Date'] = pd.to_datetime(data['Date'])
    
    return data

# Step 3: ETL (Extract, Transform, Load)
def transform_data(data):
    # Example: Create a new column 'Profit' as 'Revenue' - 'Cost'
    data['Profit'] = data['Revenue'] - data['Cost']
    
    # Aggregate data by 'Category'
    aggregated_data = data.groupby('Category').agg({
        'Revenue': 'sum',
        'Cost': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    return aggregated_data

# Step 4: Data Analysis and Visualization
def analyze_and_visualize(data):
    # Plotting Revenue by Category
    plt.figure(figsize=(10, 6))
    plt.bar(data['Category'], data['Revenue'], color='skyblue')
    plt.title('Revenue by Category')
    plt.xlabel('Category')
    plt.ylabel('Revenue')
    plt.show()
    
    # Plotting Profit by Category
    plt.figure(figsize=(10, 6))
    plt.bar(data['Category'], data['Profit'], color='lightgreen')
    plt.title('Profit by Category')
    plt.xlabel('Category')
    plt.ylabel('Profit')
    plt.show()

# Step 5: Export Data to Power BI
def export_to_powerbi(data):
    # Authenticate with Power BI
    device_auth = DeviceCodeLoginAuthentication()
    
    # Create a Power BI dataset
    dataset_config = get_dataset_config(data)
    dataset = QuickVisualize.get_dataset_config(data)
    
    # Create a Power BI report
    report = Report()
    report.add_dataset(dataset)
    
    # Add visualizations to the report
    report.add_visualization('Revenue by Category', 'bar', x='Category', y='Revenue')
    report.add_visualization('Profit by Category', 'bar', x='Category', y='Profit')
    
    # Publish the report to Power BI
    report.publish(device_auth)

# Main Function
def main():
    # Load the data
    file_path = 'data.csv'
    data = load_data(file_path)
    
    # Clean the data
    cleaned_data = clean_data(data)
    
    # Transform the data
    transformed_data = transform_data(cleaned_data)
    
    # Analyze and visualize the data
    analyze_and_visualize(transformed_data)
    
    # Export the data to Power BI
    export_to_powerbi(transformed_data)

if __name__ == "__main__":
    main()