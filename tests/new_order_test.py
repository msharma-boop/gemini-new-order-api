import base64
import datetime
import hashlib
import hmac
import json
import time

import requests

base_url = "https://api.sandbox.gemini.com"
endpoint = "/v1/order/new"
url = base_url + endpoint

gemini_api_key = "account-E0PPYQdV5TXAYbHL33np"
gemini_api_secret = "Aa4DAzh8z5g374Qen95bPkTTw12".encode()


def set_payload_nonce():
    t = datetime.datetime.now()
    return str(int(time.mktime(t.timetuple()) * 1000))


def set_payload(symbol, amount, price, side, type, options):
    payload = {
        "request": "/v1/order/new",
        "nonce": set_payload_nonce(),
        "symbol": symbol,
        "amount": amount,
        "price": price,
        "side": side,
        "type": type,
        "options": options
    }
    return payload


def encode_payload(payload):
    encoded_payload = json.dumps(payload).encode()
    b64 = base64.b64encode(encoded_payload)
    return b64


def test_buy_request():
    payload = encode_payload(
        set_payload("btcusd", "5", "3633.00", "buy", "exchange limit", ["maker-or-cancel"]))
    signature = hmac.new(gemini_api_secret, payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)
    assert response.status_code == 200

    new_order_response = response.json()
    assert new_order_response['is_live'] == True
    assert new_order_response['symbol'] == "btcusd"


def test_sell_request():
    payload = encode_payload(
        set_payload("btcusd", "5", "3633.00", "sell", "exchange limit", ["maker-or-cancel"]))
    signature = hmac.new(gemini_api_secret, payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)
    assert response.status_code == 200
    new_order_response = response.json()
    assert new_order_response['symbol'] == "btcusd"


def test_exchange_limit_request():
    payload = encode_payload(
        set_payload("btcusd", "5", "40000.00", "sell", "exchange limit", ["maker-or-cancel"]))
    signature = hmac.new(gemini_api_secret, payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)
    assert response.status_code == 200
    new_order_response = response.json()
    assert new_order_response['symbol'] == "btcusd"
    assert new_order_response['type'] == "exchange limit"


def test_stop_limit_request():
    payload = {
        "request": "/v1/order/new",
        "nonce": set_payload_nonce(),
        "symbol": "btcusd",
        "amount": "5",
        "price": "40000.00",
        "stop_price": "35000.00",
        "side": "buy",
        "type": "exchange limit",
        "options": ["maker-or-cancel"]
    }

    encoded_payload = encode_payload(payload)
    signature = hmac.new(gemini_api_secret, encoded_payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': encoded_payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)
    assert response.status_code == 200
    new_order_response = response.json()
    assert new_order_response['symbol'] == "btcusd"
    assert new_order_response['type'] == "exchange limit"
    assert new_order_response['reason'] == "MakerOrCancelWouldTake"


def test_stop_limit_sell_request():
    payload = {
        "request": "/v1/order/new",
        "nonce": set_payload_nonce(),
        "symbol": "btcusd",
        "amount": "5",
        "price": "40000.00",
        "stop_price": "42000.00",
        "side": "sell",
        "type": "exchange limit",
        "options": ["maker-or-cancel"]
    }

    encoded_payload = encode_payload(payload)
    signature = hmac.new(gemini_api_secret, encoded_payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': encoded_payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)
    assert response.status_code == 200
    new_order_response = response.json()
    assert new_order_response['symbol'] == "btcusd"
    assert new_order_response['type'] == "exchange limit"


def test_empty_options_sell_request():
    payload = {
        "request": "/v1/order/new",
        "nonce": set_payload_nonce(),
        "symbol": "btcusd",
        "amount": "5",
        "price": "40000.00",
        "stop_price": "42000.00",
        "side": "sell",
        "type": "exchange limit",
        "options": []
    }

    encoded_payload = encode_payload(payload)
    signature = hmac.new(gemini_api_secret, encoded_payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': encoded_payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)
    assert response.status_code == 200
    new_order_response = response.json()
    assert new_order_response['symbol'] == "btcusd"
    assert new_order_response['type'] == "exchange limit"


def test_option_immediate_or_cancel_request():
    payload = encode_payload(
        set_payload("btcusd", "5", "3633.00", "buy", "exchange limit", ["immediate-or-cancel"]))
    signature = hmac.new(gemini_api_secret, payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)
    assert response.status_code == 200

    new_order_response = response.json()
    assert new_order_response['symbol'] == "btcusd"


def test_option_fill_or_kill_request():
    payload = encode_payload(
        set_payload("btcusd", "5", "3633.00", "buy", "exchange limit", ["fill-or-kill"]))
    signature = hmac.new(gemini_api_secret, payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)
    assert response.status_code == 200

    new_order_response = response.json()
    assert new_order_response['symbol'] == "btcusd"


def test_option_auction_only_request():
    payload = encode_payload(
        set_payload("btcusd", "5", "3633.00", "buy", "exchange limit", ["auction_only"]))
    signature = hmac.new(gemini_api_secret, payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)
    assert response.status_code == 200

    new_order_response = response.json()
    assert new_order_response['symbol'] == "btcusd"


def test_market_buy_high_limit_request():
    payload = encode_payload(
        set_payload("btcusd", "5", "70000.00", "buy", "exchange limit", ["immediate-or-cancel"]))
    signature = hmac.new(gemini_api_secret, payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)
    assert response.status_code == 200

    new_order_response = response.json()
    assert new_order_response['symbol'] == "btcusd"


def test_market_sell_low_limit_request():
    payload = encode_payload(
        set_payload("btcusd", "5", "2.00", "sell", "exchange limit", ["immediate-or-cancel"]))
    signature = hmac.new(gemini_api_secret, payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)
    assert response.status_code == 200

    new_order_response = response.json()
    assert new_order_response['symbol'] == "btcusd"


def test_invalid_signature():
    payload = encode_payload(
        set_payload("btcusd", "5", "2.00", "sell", "exchange limit", ["immediate-or-cancel"]))
    signature = hmac.new("Aa4DAzh8z5g374Qen95bPkTTw1".encode(), payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)

    new_order_response = response.json()
    assert new_order_response['reason'] == "InvalidSignature"


def test_invalid_symbol_request():
    payload = encode_payload(
        set_payload("abc", "5", "3633.00", "buy", "exchange limit", ["maker-or-cancel"]))
    signature = hmac.new(gemini_api_secret, payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)

    new_order_response = response.json()
    assert new_order_response['reason'] == "InvalidSymbol"
    assert new_order_response['message'] == "Received unsupported symbol 'abc'"


def test_invalid_price_request():
    payload = encode_payload(
        set_payload("btcusd", "5", "-3633.00", "buy", "exchange limit", ["maker-or-cancel"]))
    signature = hmac.new(gemini_api_secret, payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)

    new_order_response = response.json()
    assert new_order_response['reason'] == "InvalidPrice"
    assert new_order_response['message'] == "Invalid price for symbol BTCUSD: -3633.00"


def test_invalid_side_request():
    payload = encode_payload(
        set_payload("btcusd", "5", "3633.00", "abc", "exchange limit", ["maker-or-cancel"]))
    signature = hmac.new(gemini_api_secret, payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)

    new_order_response = response.json()
    assert new_order_response['reason'] == "InvalidSide"
    assert new_order_response['message'] == "Invalid side for symbol BTCUSD: 'abc'"


def test_invalid_nonce():
    payload = {
        "request": "/v1/order/new",
        "nonce": 1,
        "symbol": "btcusd",
        "amount": "5",
        "price": "40000.00",
        "stop_price": "42000.00",
        "side": "sell",
        "type": "exchange limit",
        "options": ["maker-or-cancel"]
    }
    encoded_payload = encode_payload(payload)
    signature = hmac.new(gemini_api_secret, encoded_payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)

    new_order_response = response.json()
    assert new_order_response['reason'] == "InvalidNonce"
    assert new_order_response['message'] == "Nonce '1' has not increased since your last call to the Gemini API."


def test_options_should_only_one_option():
    payload = {
        "request": "/v1/order/new",
        "nonce": set_payload_nonce(),
        "symbol": "btcusd",
        "amount": "5",
        "price": "40000.00",
        "stop_price": "42000.00",
        "side": "sell",
        "type": "exchange limit",
        "options": ["maker-or-cancel", "fill-or-kill"]
    }
    encoded_payload = encode_payload(payload)
    signature = hmac.new(gemini_api_secret, encoded_payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': encoded_payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)

    new_order_response = response.json()
    assert new_order_response['reason'] == "ConflictingOptions"
    assert new_order_response[
               'message'] == "A single order supports at most one of these options: ['maker-or-cancel', " \
                             "'immediate-or-cancel', 'auction-only', 'fill-or-kill'] "


def test_invalid_option():
    payload = {
        "request": "/v1/order/new",
        "nonce": set_payload_nonce(),
        "symbol": "btcusd",
        "amount": "5",
        "price": "40000.00",
        "stop_price": "42000.00",
        "side": "sell",
        "type": "exchange limit",
        "options": ["abc"]
    }
    encoded_payload = encode_payload(payload)
    signature = hmac.new(gemini_api_secret, encoded_payload,
                         hashlib.sha384).hexdigest()

    request_headers = {'Content-Type': "text/plain",
                       'Content-Length': "0",
                       'X-GEMINI-APIKEY': gemini_api_key,
                       'X-GEMINI-PAYLOAD': encoded_payload,
                       'X-GEMINI-SIGNATURE': signature,
                       'Cache-Control': "no-cache"}

    response = requests.post(url,
                             data=None,
                             headers=request_headers)

    new_order_response = response.json()
    assert new_order_response['reason'] == "UnsupportedOption"
    assert new_order_response['message'] == "Option 'abc' is not supported."
