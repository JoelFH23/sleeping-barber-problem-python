import time, random, requests, colorama, os
from threading import Thread
from barberShop import BarberShop
from barber import Barber
from customer import Customer

# Reinicia el color de la consola.
colorama.init(autoreset=True)

def main():
    try:
        maxCustomerInterval = 3 # Segundos máximos que los clientes entraran a barberia.
        totalCustomers = 0 # Almacena el todal de clientes.
        totalChairs=3 # Total de sillas.
        customers = [] # Almacenará a todos los clientes.

        totalCustomers = int(input("Total de clientes: ")) # Pedimos al usuario el total de clientes.

        # Verificamos que sólo se ingresen enteros positivos
        if ( totalCustomers <=0 or totalCustomers >=50 ):
            raise IndexError("Total customers can not be zero.")
        
        # Hacemos una petición a la API.
        response = requests.get(f"https://names.drycodes.com/{totalCustomers}?nameOptions=boy_names")
        # Transformamos la respuesta a formato JSON y la almacenamos.
        data = response.json()

        # Comprobamos que la petición anterior se haya hecho con éxito.
        if( response.status_code == 200):
            for name in data:
                customers.append(Customer(str(name.partition('_')[0])))
        else:
            raise NameError("An error has occurred! Please Check your internet connection or try again later.")
        
        # Crearemos al objeto barbero.
        barber = Barber()

        # Crearemos al objeto barbería y le pasamos...
        # el total de sillas, al berbero, y el total de clientes.
        barberShop = BarberShop(
            totalChairs=totalChairs,
            barber=barber,
            totalCustomers=totalCustomers
        )
        
        # Luego de crear al objeto barberia llamamos al método abrir.
        barberShop.open()

        # Este bucle se ejecutará hasta que ya no haya más clientes en el array.
        while customers:
            # Creamos un hilo y le pasamos al cliente que queremos que entre a la berbería.
            thread = Thread(
                target=barberShop.enter,
                args=( customers.pop(), )
            )
            # Inicializamos el hilo.
            thread.start()
            # Creamos un pequeño delay para que los clientes entren...
            # en un tiempo distinto.
            time.sleep(random.randint(1,maxCustomerInterval))
            
    # Todo el manejo de errores.
    except ValueError as errorMessage:
        print(f"{colorama.Fore.RED}{errorMessage} ")
        os.system("pause")
    except NameError as errorMessage:
        print(f"{colorama.Fore.RED}{errorMessage} ")
        os.system("pause")
    except IndexError as errorMessage:
        print(f"{colorama.Fore.RED}{errorMessage} ")
        os.system("pause")


if __name__ == "__main__":
    main()
