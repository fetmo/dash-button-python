import requests


class Shopware:
    actions = {
        'auth': '/DashAuthentication/authButton',
        'triggerClick': '/DashButton/triggerClick',
        'getProduct': '/DashButton/getProduct'}

    def __init__(self, url, buttoncode):
        self.url = url.rstrip('/')
        self.buttoncode = buttoncode
        self.authtoken = ''

    def auth(self):
        url = self.url + self.actions['auth']
        response = requests.get(url, params={'buttoncode': self.buttoncode})
        if response.status_code == 200:
            json = response.json()
            self.authtoken = json['token']

    def triggerClick(self):
        if self.authtoken == '':
            self.auth()

        url = self.url + self.actions['triggerClick']

        response = requests.post(url, params={'token': self.authtoken})
        if response.status_code == 200:
            responseJson = response.json()
            return responseJson['success']

        return False

    def getProduct(self):
        if self.authtoken == '':
            self.auth()

        url = self.url + self.actions['getProduct']
        productData = {}

        response = requests.get(url, params={'token': self.authtoken})

        if response.status_code == 200:
            responseJson = response.json()
            productData = responseJson['product']

        return productData
