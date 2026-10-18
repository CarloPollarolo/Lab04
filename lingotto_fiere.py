import csv


class Stand:
    def __init__(self,codice_stand,sup,padiglione,prezzo):
        self.__codice_stand=codice_stand
        self.__sup=sup
        self.__padiglione=padiglione
        self.__prezzo=prezzo
        self.__espositore=None #attributo che contiene l'oggetto intero di espositore, con i suoi vari attributi
    @property
    def codice_stand(self):
        return self.__codice_stand

    @property
    def sup(self):
        return self.__sup

    @property
    def padiglione(self):
        return self.__padiglione

    @property
    def prezzo(self):
        return self.__prezzo
    @prezzo.setter  #il prezzo può variare successivamente, quindi lo rendo accessibile e modificabile
    def prezzo(self,prezzo):
        self.__prezzo=prezzo

    @property
    def espositore(self): #in stand definisco pure espositore come attributo, perchè in seguito gliene vengono assegnati
        return self.__espositore
    @espositore.setter
    def espositore(self,espositore):
        self.__espositore=espositore #servirà nella funzione dell'assegnazione dello stand
        #verrà richiamato direttamente come '.espositore' e ora può essere modificato

    def disponibile(self):
        return self.__espositore is None
    #metodo che specifica la disponibilità dell'oggetto Stand, se è occupato o meno da un espositore
    
    def stato(self):
        if self.disponibile():
            return 'Disponibile' #quando è definito come inizializzato, ovvero senza espositore assegnato
        return 'Non disponibile'

    
    def nuovo_prezzo(self):
        return self.prezzo

    #perche qua metto pure nuovo_prezzo? non bastava solo prezzo???
    #imposto nuovo prezzo pure nella padre e non solo nelle figlie per:
    #1) chiarire che il prezzo iniziale self.__prezzo --> self.prezzo non viene modificato
    #2) serve per il confronto richiesto dall'ultima def di consegna, ovvero ordinare in ordine crescente per
    #prezzo tutti gli stand compresi in padre e figlie, e quindi si imposta un nuovo prezzo per tutte e tre,
    #che viene modificato da aggiunte specifiche nelle figlie e che invece rimane costante nella padre

    def __lt__(self, other):
        return self.nuovo_prezzo() < other.nuovo_prezzo()

    def __str__(self):
        return f"{self.__codice_stand}: Standard | {self.__sup} mq - Padiglione {self.__padiglione} - Prezzo {self.prezzo}€ - {self.stato()}"


class StandPremium(Stand):
    def __init__(self,codice_stand,sup,padiglione,prezzo,posizione):
        super().__init__(codice_stand,sup,padiglione,prezzo) #nel super attributi ereditati
        self.__posizione=posizione  #dopo super nuovo attributo specifico

    @property
    def posizione(self):
        return self.__posizione

    def nuovo_prezzo(self):   #usando la sua def, nuovo_prezzo diventa nuovo attributo di questa classe figlia
        return self.prezzo*1.30    #modificando il prezzo originale

    def __str__(self):
        return f"{self.codice_stand}: Premium | {self.sup} mq - Padiglione {self.padiglione} - Prezzo {self.nuovo_prezzo()}€ - Posizione: {self.__posizione} - {self.stato()}"


class StandPreseExtra(Stand):
    def __init__(self,codice_stand,sup,padiglione,prezzo,prese):
        super().__init__(codice_stand,sup,padiglione,prezzo)
        self.__prese=prese

    @property
    def prese(self):
        return self.__prese
    @prese.setter
    def prese(self,prese):
        self.__prese=int(prese)

    def nuovo_prezzo(self):
        return self.prezzo*(1+0.07*self.prese)

    def __str__(self):
        return f"{self.codice_stand}: Prese Extra | {self.sup} mq - Padiglione {self.padiglione} - Prezzo {self.nuovo_prezzo()}€ - Prese aggiuntive: {self.prese} - {self.stato()}"




class Espositore:
    def __init__(self, codice_espositore, nome, cognome):
        self.__codice_espositore=codice_espositore
        self.__nome=nome
        self.__cognome=cognome
    @property
    def codice_espositore(self):
        return self.__codice_espositore

    @property
    def nome(self):
       return self.__nome
   
    @property
    def cognome(self):
       return self.__cognome
    
    def __eq__(self, other):
        if isinstance(other, Espositore):
            return self.__codice_espositore == other.__codice_espositore
        return False

    def __str__(self):
        return f"{self.__codice_espositore},{self.__nome},{self.__cognome}"




class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self.__nome=nome
        self.stand={}
        self.espositori={}

    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, nome):
        self.__nome=nome


    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        
        with open(file_path,'r',newline='',encoding='utf-8') as infile:
            reader = csv.reader(infile)

            for line in reader:
                if line[0].startswith("E"):
                    codice_espositore = line[0]
                    nome = line[1]
                    cognome = line[2]
                    espositore = Espositore(codice_espositore, nome, cognome)
                    self.espositori[codice_espositore] = espositore

                if line[0].startswith("S") and len(line) < 5: # se ha solo 4 colonne piene, allora è stand standard
                    codice_stand = line[0]
                    sup = line[1]
                    padiglione = line[2]
                    prezzo = float(line[3])
                    stand = Stand(codice_stand, sup, padiglione, prezzo)
                    self.stand[codice_stand] = stand

                if len(line) == 5:
                    codice_stand = line[0]
                    sup = line[1]
                    padiglione = line[2]
                    prezzo = float(line[3])
                    valore = line[4]

                    if valore.isdigit():
                        prese_elettriche = int(valore)
                        prese = StandPreseExtra(codice_stand, sup, padiglione, prezzo, prese_elettriche)
                        self.stand[codice_stand] = prese

                    else:
                        posizione = valore
                        premium = StandPremium(codice_stand, sup, padiglione, prezzo, posizione)
                        self.stand[codice_stand] = premium
                #assegno alla chiave codice come valore un oggetto della classe, con i suoi attributi


    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        #problemi: inseistenza dei due codici, stand senza disponibilità oppure espositore già assegnato,
        #ovvero si trova già posto come attributo in uno stand

        """Associa uno stand a un espositore"""
        if codice_stand not in self.stand: #controllo se il codice non esiste tra le chiavi del diz. degli stand
            raise Exception(f"Stand {codice_stand} non trovato")

        if codice_espositore not in self.espositori: #stesso controllo ma del codice esp. in Espositori
            raise Exception(f"Espositore {codice_espositore} non trovato")

        if not self.stand[codice_stand].disponibile():
            raise Exception(f"Stand {codice_stand} già occupato")


        espositore = self.espositori[codice_espositore] # valore del dizionario self.espositori
        for s in self.stand.values():
            if s.espositore == espositore:  #controllo tra tutti gli stand se l'espositore è gia stato assegnato, ovvero se quell'esp. è presente come attributo di uno stand
                raise Exception(f"Espositore {codice_espositore} già assegnato a uno stand")

        #infine, se non si verifica alcun problema, assegno all'attributo 'espositore' dello stand richiesto l'espositore richiesto
        self.stand[codice_stand].espositore = espositore #come l'intero oggetto espositore, data la riga 201
        # il controllo della riga 203 avviene grazie a __eq__ definito della classe Espositore, che
        # considera due espositori uguali dato il codice_espositore
        #nel dizionario self.stand con chiave codice_stand il valore è l'oggetto della classe Stand,
        #classe in cui abbiamo definito pure l' attributo 'responsabile' che non compare fra gli attributi dell'
        #oggetto-valore ma è cmq recuperabile dagli attributi totali della sua classe, facendo appunto '.espositore'

        #chiave --> valore --> classe --> attributo(usato solo nella costruzione della classe)
    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for espositore in self.espositori.values(): # i valori di quel dizionario sono tutti gli esp. della classe Espositori
            codice_stand = None  #inizialmente imposto per ogni esp. uno stand nullo

            for s in self.stand.values(): #controllo date le modifiche della def precedente!!!:
                if s.espositore == espositore: #se vedo che l'esp. di uno stand coincide con uno fra gli esp. in Espositori
                    codice_stand = s.codice_stand #allora gli assegno nello stand nullo quello stand
                    break

            if codice_stand is None: #se a qeull'esp. non gli è stato assegnato nulla e rimane nullo
                print(f"Nessuno stand assegnato all'espositore {espositore}")

            else: #se invcece gli è stato assegnato uno stand
                print(f"Stand {codice_stand} assegnato all'espositore {espositore}")


    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.stand.values())




