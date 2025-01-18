# API_Client

This repository provides a basic Python client for connecting to any API that includes an authentication endpoint.
The client automatically handles authentication and token refreshing, making it easier to work with RESTful APIs.

## Features

- Simplified API connection setup
- Automatic token-based authentication
- Optional Token refresh functionality
- Easy-to-use methods for CRUD operations
- Lightweight and dependency minimal (only requires `requests`)
- In the future: put endpoint + put authentication

## Installation

You can install the package via pip:

    ```bash
    pip install API_Client
    ```

Or install directly from the source:

    ```bash
    git clone https://github.com/tj0vtj0v/API_Client.git
    cd API_Client
    pip install .
    ```

## Usage

Here's an example of how to use the `API_Client`:

```python
from API_Client.api_client import APIClient, Client_Exception

# Initialize the client
client = APIClient(
    base_url='https://example.com/api',
    auth_endpoint='/auth',
    username='your-username',
    password='your-password',
    refresh_endpoint='/refresh' # optional
)

# Make a GET request - authentication will be implicitly done
response = client.get('some/endpoint')
print(response) # is always the response json

# Make a POST request
data = {'key': 'value'}
response = client.post('another/endpoint', data=data)
print(response)

# Make a faulty url request
try:
    client.get('faulty/endpoint')
except Client_Exception as e:
    print(e) # server response
```

Using the `API_Client` with a Context Manager:

```python
from API_Client.api_client import APIClient

# Initialize the client
with APIClient(
    base_url='https://example.com/api',
    auth_endpoint='/auth',
    username='your-username',
    password='your-password',
    refresh_endpoint='/refresh' # optional
) as client:

   # Make a GET request - authentication will be implicitly done
   response = client.get('some/endpoint')
   print(response) # is always the response json
```

## Requirements

- Python 3.6 or higher
- `requests` library

## Installation from Source

To install the package from the source repository:

1. Clone the repository:
    ```bash
    git clone https://github.com/tj0vtj0v/API_Client.git
       ```
2. Navigate to the project directory:
    ```bash
    cd API_Client
       ```
3. Install the package:
    ```bash
    pip install .
       ```

## Contributing

Contributions are welcome! If you'd like to contribute, please:

1. Fork the repository.
2. Create a feature branch:
    ```bash
    git checkout -b feature-name
       ```
3. Commit your changes:
    ```bash
    git commit -m 'Add new feature'
       ```
4. Push to the branch:
    ```bash
    git push origin feature-name
       ```
5. Open a pull request.

## License

This project is licensed under the [GNU General Public License v3.0 (GPLv3)](LICENSE.txt).

## Author

- **Tjorven Burdorf**
- GitHub: [tj0vtj0v](https://github.com/tj0vtj0v)
- Website: [unfinished](http://80.209.200.73)
- Email: [burdorftjorven@gmail.com](mailto:burdorftjorven@gmail.com)

## Links

- [Repository](https://github.com/tj0vtj0v/API_Client)
- [PyPI Package](https://pypi.org/project/API_Client/)

## Issues

If you encounter any problems, please open an issue on the [GitHub Issues](https://github.com/tj0vtj0v/API_Client/issues) page.
