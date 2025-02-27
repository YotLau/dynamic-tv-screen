import logging
from samsungtvws import SamsungTVWS

def test_tv_connection(tv_ip):
    """Test the connection to a Samsung TV.
    
    Args:
        tv_ip (str): The IP address of the TV to test.
        
    Returns:
        bool: True if connection is successful, False otherwise.
    """
    try:
        # Validate IP address format
        if not tv_ip or not isinstance(tv_ip, str):
            logging.error("Invalid TV IP address provided")
            return False

        logging.info(f"Attempting to connect to TV at {tv_ip}...")
        
        # Initialize TV connection with explicit port
        tv = SamsungTVWS(host=tv_ip, port=8002)
        
        # Try to get API version to test connection
        logging.info("Testing TV connection by requesting API version...")
        api_version = tv.art().get_api_version()
        logging.info(f"Successfully connected to TV. API Version: {api_version}")
        return True
        
    except ConnectionError as e:
        logging.error(f"Network connection error to TV at {tv_ip}: {str(e)}")
        return False
    except TimeoutError as e:
        logging.error(f"Connection timeout to TV at {tv_ip}: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"Failed to connect to TV at {tv_ip}: {str(e)}")
        return False