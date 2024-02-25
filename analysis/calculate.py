import requests

def send_data_to_website(mpbbc, bsp):
    url = 'https://example.com/submit-form'  # Replace this with the actual URL of the website's form submission endpoint
    
    # Data to be sent to the website
    data = {
        'mpbbc': mpbbc,
        'bsp': bsp
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            # Request successful
            print("Data sent successfully!")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
mpbbc = 100
bsp = 20
send_data_to_website(mpbbc, bsp)
