#include "WiFi.h"
#include "I2Cdev.h"
#include "WiFiAP.h"


#include "MPU6050_6Axis_MotionApps20.h"
MPU6050 mpu;
//Wifi info 

const char* ssid = "Test_00";
const char* password = "12233qsx";
//const char* ssid = "The_Lair_of_Task_&_Jakiro";
//const char* password = "Divine_Rapier_330";

const char *ssidAP = "TAG_0002_ID";
String TAG_ID = "TAG_0002_ID";

String PollingEvents[6] = {"13:00:00","14:43:00","15:00:00","16:00:00","17:00:00","18:00:00"};
int Hour;
int Min;
int Sec;

WiFiServer server(80);

const uint16_t port = 8007;
//const char * host = "192.168.0.9";
const char * host = "192.168.43.248";

String data;
#define OUTPUT_READABLE_WORLDACCEL
String tab = "X";
char c;

#define INTERRUPT_PIN 23  // use pin 2 on Arduino Uno & most boards
#define LED_PIN 13 // (Arduino is 13, Teensy is 11, Teensy++ is 6)
#define POWER_PIN 25
#define ON_PIN 19


bool blinkState = false;
bool APFLAG = false;

// MPU control/status vars
bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

// orientation/motion vars
Quaternion q;           // [w, x, y, z]         quaternion container
VectorInt16 aa;         // [x, y, z]            accel sensor measurements
VectorInt16 aaReal;     // [x, y, z]            gravity-free accel sensor measurements
VectorInt16 aaWorld;    // [x, y, z]            world-frame accel sensor measurements
VectorFloat gravity;    // [x, y, z]            gravity vector
float euler[3];         // [psi, theta, phi]    Euler angle container
float ypr[3];           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector


unsigned long Time_counter_IMU = 0;
unsigned long Time_counter = 0;
unsigned long Time_counter_Polling_Event = 86400000;
unsigned long Current_time_in_millis = 0;
unsigned long Off_counter = 0;


long buttonTimer = 0;
long longPressTime = 2500;

boolean buttonActive = false;
boolean longPressActive = false;

int16_t Ax[7000];
int16_t Ay[7000];
//int16_t Az[4000];
float yaw[7000];
//float pitch[400];
//float roll[4000];
unsigned long timeArray[7000];
int Array_counter = 0;

String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

unsigned long Calculate_micros_polling(String PollingEvents[6],int Hour, int Min, int Sec){

  unsigned long MicrosVal =86400000;
  unsigned long tempMicros =0;
  for (int i =0; i < 6; i++){
    int PollingHour = getValue(PollingEvents[i], ':', 0).toInt();
    int PollingMin = getValue(PollingEvents[i], ':', 1).toInt();
    int PollingSec = getValue(PollingEvents[i], ':', 2).toInt();
    unsigned long currentMillis = (Hour)*3600000 + (Min)*60000 + (Sec)*1000;
    unsigned long PollMillis = (PollingHour)*3600000 + (PollingMin)*60000 + (PollingSec)*1000;
    Serial.println(currentMillis);
    Serial.println(PollMillis);
    if (PollMillis > currentMillis){
      tempMicros = PollMillis - currentMillis;
      Serial.println(tempMicros);
    }
    if ((tempMicros < MicrosVal) && tempMicros > 0){
      MicrosVal = tempMicros;
      Serial.println(MicrosVal);
    }
  }
  Serial.println(MicrosVal + millis());
  return MicrosVal + millis();
}

void addValues(int Array_counter, int16_t AxWorld,int16_t AyWorld,int16_t AzWorld,float y, float p, float r){
  Ax[Array_counter] = AxWorld;
  Ay[Array_counter] = AyWorld;
  //Az[Array_counter] = AzWorld;
  yaw[Array_counter] = y;
  //pitch[Array_counter] = p;
  //roll[Array_counter] = r;
  timeArray[Array_counter] = millis();
}
void PrintValues(int Array_counter){
  Serial.print("aworld\t");
  Serial.print(Ax[Array_counter]);
  Serial.print("\t");
  Serial.print(Ay[Array_counter]);
  Serial.print("\t");
  //Serial.print(Az[Array_counter]);
  Serial.print("\t time \t");
  Serial.println(timeArray[Array_counter]);  
}

void HostAP(){
  WiFi.mode(WIFI_AP_STA);
  WiFi.softAP(ssidAP);
  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
}

void ButtonCheck(){
  if (digitalRead(POWER_PIN) == LOW) {

    if (buttonActive == false) {

      buttonActive = true;
      buttonTimer = millis();

    }

    if ((millis() - buttonTimer > longPressTime) && (longPressActive == false)) {

      longPressActive = true;
      Serial.println("Button held");

    }

  } else {

    if (buttonActive == true) {

      if (longPressActive == true) {

        longPressActive = false;
        Serial.println("TURNING OFF");
        pinMode(POWER_PIN, OUTPUT);
        digitalWrite(POWER_PIN, LOW);
        digitalWrite(ON_PIN, LOW);
      } else {

      }

      buttonActive = false;

    }

  }
}

void SendData(String data){
  WiFiClient client;
 
  if (!client.connect(host, port)) {
 
    Serial.println("Connection to host failed");
 
    delay(1000);
    return;
  }
  client.print(data);
  Serial.println(" ");
  Serial.println("Data Recived is:");
  unsigned long tempclock = millis();

  while(!client.available() && tempclock + 5000 >= millis()) {
   delay(1);
  }
  Serial.println("recig");
  String line = client.readString();
  Hour = getValue(line, ':', 0).toInt();
  Min = getValue(line, ':', 1).toInt();
  Sec = getValue(line, ':', 2).toInt();
  if (Hour == 66){
    digitalWrite(ON_PIN, LOW);
  } else{
    Current_time_in_millis = (Hour)*3600000 + (Min)*60000 + (Sec)*1000;
    Time_counter_Polling_Event = Calculate_micros_polling(PollingEvents,Hour,Min,Sec);
  }

  Serial.println(Hour);
  Serial.println(Min);
  Serial.println(Sec);
  client.stop();
  Serial.println(" ");
  Serial.println("End of data recieved");
}

volatile bool mpuInterrupt = false;     // indicates whether MPU interrupt pin has gone high
void dmpDataReady() {
    mpuInterrupt = true;
}

String WifiScan_Update(){
  Serial.println("scan start");
  String ScanString = "Scan Start:";
  // WiFi.scanNetworks will return the number of networks found
  int n = WiFi.scanNetworks();
  Serial.println("scan done");
  if (n == 0) {
    Serial.println("no networks found");
    ScanString = "NONE";
  } else {
    Serial.print(n);
    Serial.println(" networks found");
    for (int i = 0; i < n; ++i) {
      // Print SSID and RSSI for each network found
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(")");
      Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN)?" ":"*");
      ScanString = ScanString + tab + WiFi.SSID(i) + tab + WiFi.RSSI(i);
    }
  }
  Serial.println("");
  return ScanString;
}


void MPU_Update() {
    if (!dmpReady) return;
    // read a packet from FIFO
    if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) { // Get the Latest packet 

        #ifdef OUTPUT_READABLE_WORLDACCEL
            // display initial world-frame acceleration, adjusted to remove gravity
            // and rotated based on known orientation from quaternion
            mpu.dmpGetQuaternion(&q, fifoBuffer);
            mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
            mpu.dmpGetAccel(&aa, fifoBuffer);
            mpu.dmpGetGravity(&gravity, &q);
            mpu.dmpGetLinearAccel(&aaReal, &aa, &gravity);
            mpu.dmpGetLinearAccelInWorld(&aaWorld, &aaReal, &q);
            delay(10);
            //Serial.print("aworld\t");
            //Serial.print(aaWorld.x);
            //Serial.print("\t");
            //Serial.print(aaWorld.y);
            //Serial.print("\t");
            //Serial.println(aaWorld.z);
        #endif
    }
}

void WifiConnect(){
      // Set WiFi to station mode and disconnect from an AP if it was previously connected
  detachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN));
  WiFi.disconnect();
  WiFi.softAPdisconnect(true);
  WiFi.mode(WIFI_STA);
  delay(100);
  ///######## Important #######
    //maybe add another condition to while loop to check if ip address is not 0.0.0.0
  WiFi.begin(ssid, password);
  delay(2000);
  unsigned long tempTimer = millis();
  while (WiFi.status() != WL_CONNECTED && WiFi.localIP().toString() == "0.0.0.0" && millis() <= tempTimer +5000 ) {
    delay(100);
    Serial.println("...");
  }
  Serial.println("CONNECTED");
  Serial.println(WiFi.localIP());
  pinMode(INTERRUPT_PIN, INPUT);
}

void setup()
{
  pinMode(ON_PIN, OUTPUT);
  digitalWrite(ON_PIN, HIGH);
  pinMode(POWER_PIN, INPUT_PULLUP);
  Serial.begin(115200);
  //digitalWrite(POWER_PIN, HIGH);

  WifiConnect();
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());


      // join I2C bus (I2Cdev library doesn't do this automatically)
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
        Wire.setClock(400000); // 400kHz I2C clock. Comment this line if having compilation difficulties
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif


    Serial.println(F("Initializing I2C devices..."));
    mpu.initialize();
    pinMode(INTERRUPT_PIN, INPUT);

    // verify connection
    Serial.println(F("Testing device connections..."));
    Serial.println(mpu.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));


    // load and configure the DMP
    Serial.println(F("Initializing DMP..."));
    devStatus = mpu.dmpInitialize();

    // supply your own gyro offsets here, scaled for min sensitivity
    mpu.setXGyroOffset(-7);
    mpu.setYGyroOffset(39);
    mpu.setZGyroOffset(61);
    mpu.setZAccelOffset(1302); // 1688 factory default for my test chip
    mpu.setXAccelOffset(-4884);
    mpu.setYAccelOffset(2341);
    // make sure it worked (returns 0 if so)
    if (devStatus == 0) {
        // Calibration Time: generate offsets and calibrate our MPU6050
        mpu.CalibrateAccel(6);
        mpu.CalibrateGyro(6);
        mpu.PrintActiveOffsets();
        // turn on the DMP, now that it's ready
        Serial.println(F("Enabling DMP..."));
        mpu.setDMPEnabled(true);

        // enable Arduino interrupt detection
        Serial.print(F("Enabling interrupt detection (Arduino external interrupt "));
        Serial.print(digitalPinToInterrupt(INTERRUPT_PIN));
        Serial.println(F(")..."));
        attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), dmpDataReady, RISING);
        mpuIntStatus = mpu.getIntStatus();

        // set our DMP Ready flag so the main loop() function knows it's okay to use it
        Serial.println(F("DMP ready! Waiting for first interrupt..."));
        dmpReady = true;

        // get expected DMP packet size for later comparison
        packetSize = mpu.dmpGetFIFOPacketSize();
    } else {
        // ERROR!
        // 1 = initial memory load failed
        // 2 = DMP configuration updates failed
        // (if it's going to break, usually the code will be 1)
        Serial.print(F("DMP Initialization failed (code "));
        Serial.print(devStatus);
        Serial.println(F(")"));
    }

}

void loop()
{
  ButtonCheck();
  if (millis() >= Time_counter_IMU + 150){
    Time_counter_IMU = millis();
    MPU_Update();
    addValues(Array_counter, aaWorld.x, aaWorld.y, aaWorld.z,ypr[0],ypr[1],ypr[2]);
    Array_counter ++;
  }

  if ((millis() >= Time_counter + 15000) && ((millis()< Time_counter_Polling_Event)||APFLAG == false)) {
    WifiConnect();
    Time_counter = millis();
    data = "Data Start:";
    data = data + tab + TAG_ID + tab;
    while (Array_counter > 0){
      Array_counter = Array_counter - 1;
      data = data + tab + Ax[Array_counter] + tab + Ay[Array_counter] + tab+ yaw[Array_counter]  +  tab + timeArray[Array_counter];
    }
    if (WifiScan_Update() != "NONE"){
      data = data + WifiScan_Update();
    } else{
      APFLAG = true;
    }
    
    data = data + "   End";
    SendData(data);
    Serial.print(data);
    Serial.print(data.length());

  } else if((millis() >= Time_counter_Polling_Event)&& (APFLAG == true)){
    WiFi.disconnect();
    HostAP();
    Time_counter = millis();
    Serial.println("ACCESS POINT MODE");
    APFLAG = false;   
  }
}