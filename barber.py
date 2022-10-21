import colorama, time, random

colorama.init(autoreset=True)

maxHaircutDuration = 7

class Barber:
    def __init__(self):
        pass
    
    # Método para que el barbero duerma.
    def sleep(self, message):
        print(message)
    
    # Método para que el barbero se despierte.
    def wakeUp(self, customer):
        print(f"{customer} despierta al barbero.")
    
    # Método para que el barbero corte el pelo.
    def hairCutting(self, customer):
        print(f"{colorama.Fore.LIGHTYELLOW_EX}El barbero esta atendiendo a: {customer}")
        randomTime = random.randint(1,maxHaircutDuration)
        print(f"El corte de {customer} finaliza en: {randomTime}s ")
        # Delay para simular la duración del corte.
        time.sleep(randomTime)
        print(f"{colorama.Fore.LIGHTGREEN_EX}El corte de {customer} ha finalizado.")