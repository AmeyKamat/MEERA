#import webbrowser

from circuits.web import Server

from app_config import BOOTSTRAP_MODULES
from definitions import IP_ADDR, PORT

def bootstrap_app_components(app, components):
    for component in components:
        component.register(app)

def bootstrap_gateways(app, gateways):
    for gateway in gateways:
        gateway.register(app)

def bootstrap_dispatchers(app, dispatchers):
    for dispatcher in dispatchers:
        dispatcher.register(app)

def bootstrap_circuit_components(app, components):
    for component in components:
        component.register(app)


def main():
    app = Server((IP_ADDR, PORT))
    bootstrap_app_components(app, BOOTSTRAP_MODULES['appComponents'])
    bootstrap_gateways(app, BOOTSTRAP_MODULES['gateways'])
    bootstrap_dispatchers(app, BOOTSTRAP_MODULES['dispatchers'])
    bootstrap_circuit_components(app, BOOTSTRAP_MODULES['circuitComponents'])

    #webbrowser.open('http://localhost:8000')

    app.run()

if __name__ == '__main__':
    main()
