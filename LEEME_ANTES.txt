usuario: sosa
pass: dgs
IP: 192.168.1.123

ssh sosa@192.168.1.123

Poner IP fija:
	Editamos: sudo nano /etc/dhcpcd.conf
	
	Y en la parte que pone: 
	"# Example static IP configuration:" 
	
	Le agregamos estas líneas para ponerle una ip 192.168.1.123
	
	#interface eth0
	interface wlan0
	static ip_address=192.168.1.123/24
	static routers=192.168.1.1
	static domain_name_servers=192.168.1.1 8.8.8.8
	static domain_search=

*******************************************************************************************
***  ESTO ES PARA HACER TODO EL TRABAJO DESDE CERO. LEER MÁS ABAJO PARA AUTOMATIZAR     ***
*******************************************************************************************
directorio de trabajo: ~/NFC

Cero el directorio si no existe: mkdir ~/NFC
Voy al dir de trabajo: cd NFC
Creo entorno virtual: python -m venv nfc-env
entorno virtual: nfc-env 
Estando en el dir de trabajo, activo el entorno virtual: source nfc-env/bin/activate
(Para desactivar, ejecuto: deactivate)

Si al ejecutar el script de python da error de que le falta alguna librería (GPIO y/o mrfc):
!! Con el entorno virtual activado, ejecutar

pip install RPi.GPIO
pip install mfrc522

*******************************************************************************************
***                     CON ESTO SE DEBERÍA INSTALAR TODO AUTOMÁTICO                    ***
*******************************************************************************************
En tu raspberry:

mkdir NFC
cd NFC
python3 -m venv nfc-env
source nfc-env/bin/activate
pip install -r requirements.txt

Y ta, después ejecutas los archivos nomás:
python lectura.py para que lea una tarjeta
python escritura.py te pide que le queres poner en el campo "data" y te lo escribe



Conexin del modulo de RFID con la raspberry:
HACE REFERENCIA A LOS PINES FISICOS, o sea, el 1 es el 1 del pinout de la raspberry
y no respecto al pinout de alguna libreria.

SDA se conecta al Pin 24 
SCK se conecta al pin 23 
MOSI se conecta al Pin 19 
MISO se conecta al Pin 21 
GND se conecta al Pin 6 
RST se conecta al pin 22 
3.3v se conecta al Pin 1 
