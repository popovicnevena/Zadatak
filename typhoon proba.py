from typhoon.api.schematic_editor import SchematicAPI
import typhoon.api.hil as hil




#Definisanje funkcije testiranja
def dummy_test():

    # Čitanje trenutnog stanja
    stanje = hil.get_contactor_settings('S1')
    
    print(stanje['software_value'])
    print(f"U testnoj iteraciji {i+1} prekidač S1 je: {'Zatvoren' if stanje['software_value'] == 'Closed' else 'Otvoren'}")
    if stanje['software_value'] == 'Opened':
        # Zatvaranje prekidača
        hil.set_contactor('S1', swControl=True, swState=True)
        novo_stanje = hil.get_contactor_settings('S1')
        print(f'Prekidač S1 je uspešno zatvoren.')
        print(f"Nakon dummy testa u testnoj iteraciji {i+1} prekidač S1 je: {'Zatvoren' if novo_stanje['software_value'] == 'Closed' else 'Otvoren'}")
    else: 
        #Otvaranje prekidača
        hil.set_contactor('S1', swControl=True, swState=False)
        novo_stanje = hil.get_contactor_settings('S1')
        print(f'Prekidač S1 je uspešno otvoren.')
        print(f"Nakon dummy testa u testnoj iteraciji {i+1} prekidač S1 je: {'Zatvoren' if novo_stanje['software_value'] == 'Closed' else 'Otvoren'}")


#Provera inputa
def input_no_of_test():
    while True:
        unos = input('Koliko puta želite da izvršite test? Unesite 0 za izlaz.\n').strip()
        unos = unos.replace(' ', '')

        if unos == '0':
            
            return 0

        try:
            number = float(unos)

            if number < 0:
                print('Uneli ste negativan broj!')
                continue

            elif not number.is_integer():
                print('Uneli ste realan broj, broj testova mora biti ceo pozitivan broj!')
                continue

            elif number > 50:
                print('Broj testova mora biti manji od 51!')
                continue

            else:
                number = int(number)
                print(f'Validacija je uspešna, tip parsiranog podatka je {type(number)}.')
                return number

        except ValueError:
            print('Broj testova ne može biti tekstualnog tipa!')
            

#Glavni program
appname = 'NevenaP'

print(f'Aplikacija {appname} je uspešno pokrenuta!')


no_of_tests = input_no_of_test()

schema = SchematicAPI()
tse_path = r"C:\Users\user\Downloads\Python vezba\python_test.tse"
cpd_path = r"C:\Users\user\Downloads\Python vezba\python_test Target files\python_test.cpd"

if no_of_tests == 0:
    print('Aplikacija se zatvara.')
else:

    #Učitavanje modela
    print('Učitavanje šeme je započeto...')
    if schema.load(tse_path):
        print('Učitavanje šeme je uspešno završeno.')
        print('Kompajliranje šeme je započeto...')
        
        #Kompajliranje modela
        if schema.compile():
            
            print('Kompajliranje je uspešno završeno.')
            print('Učitavanje kompajliranog fajla je započeto...')

            #Učitavanje kompajliranog modela
            if hil.load_model(file = cpd_path, vhil_device = True):
                print('Kompajlirani fajl je uspešno učitan.')
                print('Simulacija se pokreće...')

                #Pokretanje simulacije
                if hil.start_simulation():
                    print('Simulacija je uspešno pokrenuta')
                    
                else:
                    print('Greška pri pokretanju simulacije')
            else:
                print('Greška pri učitavanju kompajliranog fajla.')
            
        else:
            print('Greška pri kompajliranju.')
    else:
        print('Fajl nije pronađen ili je putanja pogrešna.')

    #Izvršavanje testova u loop-u
    for i in range(no_of_tests):
        dummy_test()


        
    #hil.wait_sec(10)
    #print('Prošlo je 10. sekundi')


    #Zaustavljanje simulacije
    print('Zaustavljanje simulacije je započeto...')
    if hil.stop_simulation():
        print('Simulacija je uspešno zaustavljena.')
        print('Zatvaranje modela je započeto...')

        #Zatvaranje modela
        schema.close_model()
        print('Model je uspešno zatvoren.')


        #Restartovanje HIL-a - ne funkcioniše za virtual HIL
        '''print('Restartovanje HIL uređaja je započeto...')
        if hil.reboot_hil():
            print('HIL uređaj je uspešno restartovan.')
        else:
            print('Greška pri restartovanju HIL uređaja.')
        '''
    else:
        print('Greška pri zaustavljanju simulacije.')




