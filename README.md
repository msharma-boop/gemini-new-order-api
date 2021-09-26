# Gemini API Automation
A simple pytest test automation framework for a Gemini API. pytest is a framework that makes building simple and scalable tests easy. Tests are expressive and readable—no boilerplate code required. Get started in minutes with a small unit test or complex functional test for your application or library.

Prerequisite : Basic understanding of the Python language and requests module.
```
https://docs.python-guide.org/starting/install3/osx/
```

Install:
```
pip install -U requests
pip install -U pytest
```

To run the tests:
```
python3 -m pytest tests/

```

## Goal
Create a series of black box tests for the new Order API located at:

https://docs.gemini.com/rest-api/#new-order 

## Test Strategy

### Scope

The new order API is tested for all the parameters available. The tests will ensure that the API is functional and can support all the required parameters.  Database and UI testing are out of scope. 

### Type

API testing.

### Framework

I will be using the [pytest](https://docs.pytest.org/en/6.2.x/contents.html) framework to conduct the tests. Pytest has a lot of built in [functionality](https://docs.pytest.org/en/6.2.x/example/index.html) to get to writing test cases quickly, consistently, and effectively.

### API Capabilities

New Order can be used by complex customer to fill in the orders for all the Gemini supported cryptocurrencies. 
This API functionality is divided in three majors capabilites:

- General Buy or Sale
- Stop limit Orders
- Several Order Execution Options 

Upon generating an API request, Following mandatory parameters are required in the HTTP POST body:
- request: "v1/order/new"
- Unique nonce integer value to differentiate multiple subsequent requests 
- Crypto symbol
- side: buy or sale
- options: []

The tests that will be written will cover these functionalities and verify that the API is working as expected.

## Configuration

```json
{
  "baseUrl": "https://api.sandbox.gemini.com",
  "env": {
    "API_KEY": " account-E0PPYQdV5TXAYbHL33np",
    "API_SECRET": "Aa4DAzh8z5g374Qen95bPkTTw12"
  }
}

```

## Known Issues for the Sandbox
Tests intermittently fails due to HTTP 400 error. Need access to the server side logs to troubleshoot.
``
E       assert 400 == 200
E        +  where 400 = <Response [400]>.status_code
``


## Considerations

If this API was serving 100s of thousands of customers, I would be sure to test performance under stress conditions. It would be necessary to test API response time when there are several connections at once. 

## Documents

Gemini API docs - https://docs.gemini.com
Please refer new-order-tests.xlsx for the test cases.
