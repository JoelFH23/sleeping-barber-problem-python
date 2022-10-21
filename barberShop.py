import colorama, os
from threading import Thread, Lock, Event
from queue import Queue

colorama.init(autoreset=True)

class BarberShop:
    # Contructor de la clase
    def __init__(self, totalChairs, barber, totalCustomers):
        # Cola que simula ser las tres sillas de espera.
        self.waitingRoom = Queue(maxsize=totalChairs)
        self.totalCustomers = totalCustomers # Total de clientes
        self.barberChairOccupied = False # Conocer si la silla del berbero esta ocupada.
        self.totalChairs = totalChairs # Sillas totales
        self.barber = barber # El barbero que estará trabajando en la barbería.
        self.event = Event() # Event permite la comunicación entre hilos.
        self.lock = Lock() # Para la exclución mutua.
        self.count = 0 # Contador de los clientes que han entrado a la barbería.

    # Método para abrir la barbería.
    def open(self):
        # Impresión de algunos datos informativos.
        print("+++++ Se abre la barberia +++++", end="\n")
        print(f"Numero de clientes: {self.totalCustomers} ")
        print(f"Numero de sillas: {self.totalChairs} ")
        # Se crea un hilo para que el barbero empice a trabajar.
        thread = Thread(target=self.work)
        # Iniciamos el hilo.
        thread.start()

    # Método para representar el trabajo del barbero.
    def work(self):
        # Critical Section
        while True:
            # Bloquamos la sección crítica para que nadie más entre.
            self.lock.acquire()
            # Verificamos si existen clientes en la sala de espera.
            if( self.waitingRoom.qsize() > 0):
                # Se marcar la silla del barbero como ocupada.
                self.barberChairOccupied = True
                # Se llama al metodo que permite el corte
                # y como es una cola el primero que llego será antendido.
                self.barber.hairCutting(self.waitingRoom.get())
                # Marcamos la silla del barbero como desocupada.
                self.barberChairOccupied = False
                # Desbloqueamos la sección crítica.
                self.lock.release()
                self.event.clear()
            else:
                # Marcamos la silla del barbero como desocupada.
                self.barberChairOccupied = False
                # Desbloqueamos la sección crítica.
                self.lock.release()
                # Llamamos al método sleep para que el barbero se vaya a dormir.
                self.barber.sleep("El barbero se va a dormir.")
                # Esperamos la llegada de algún cliente.
                self.event.wait()
            # Esto solo para que el programa no se quede en un cliclo infinito...
            # luego de antender a todos los clientes.
            if ( self.totalCustomers == self.count and self.waitingRoom.empty()):
                print(f"\n{colorama.Fore.GREEN}Todos los clientes atendidos.")
                self.barber.sleep(f"{colorama.Fore.GREEN}El barbero se va a dormir.")
                os.system("pause")
                break

    # Método para que los clientes vayan entrando.
    def enter(self, customer):
        # Imprimimos algunos mensajes.
        print(f"\n{colorama.Fore.LIGHTCYAN_EX}>>>>> {customer.name} Entra a la barberia <<<<<")
        print(f"Sillas disponibles: {self.totalChairs - self.waitingRoom.qsize()} ")
        # Comprobamos si hay lugares disponebles.
        if( self.waitingRoom.full()):
            print(f"{colorama.Fore.LIGHTRED_EX}<<<<< La berberia esta llena. {customer.name} sale de la berberia >>>>>")
        else:
            # Comprobamos si el barbero está ocupado.
            # Si lo esta el cliente se sentará en una silla.
            if(self.barberChairOccupied):
                print(f"{customer.name} se sienta en una silla.")
            # Si no lo esta el cliente despertara al berbero y él lo atenderá.
            else:
                self.barber.wakeUp(customer.name)
                self.event.set()
            self.waitingRoom.put(customer.name)
        self.count += 1