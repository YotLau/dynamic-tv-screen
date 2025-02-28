import sys
import logging
from samsungtvws import SamsungTVWS

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_tv_connection_direct(tv_ip):
    """Test the connection to a Samsung TV directly.
    
    Args:
        tv_ip (str): The IP address of the TV to test.
        
    Returns:
        bool: True if connection is successful, False otherwise.
    """
    try:
        print(f"Attempting to connect to TV at {tv_ip}...")
        
        # Initialize TV connection with explicit port
        tv = SamsungTVWS(host=tv_ip, port=8002)
        
        # Try to get API version to test connection
        print("Testing TV connection by requesting API version...")
        api_version = tv.art().get_api_version()
        print(f"Successfully connected to TV. API Version: {api_version}")
        return True
        
    except ConnectionError as e:
        print(f"Network connection error to TV at {tv_ip}: {str(e)}")
        return False
    except TimeoutError as e:
        print(f"Connection timeout to TV at {tv_ip}: {str(e)}")
        return False
    except Exception as e:
        print(f"Failed to connect to TV at {tv_ip}: {str(e)}")
        return False

# Example usage
if __name__ == "__main__":
    # Test with a valid TV IP
    TV_IP = "192.168.1.55"  # Replace with your actual TV IP
    print(f"Testing connection to {TV_IP}")
    result = test_tv_connection_direct(TV_IP)
    print(f"Connection test result: {result}")
    
    # Test with an invalid TV IP
    INVALID_IP = "1.2.3.4"  # This should fail
    print(f"\nTesting connection to invalid IP {INVALID_IP}")
    result = test_tv_connection_direct(INVALID_IP)
    print(f"Connection test result: {result}")
