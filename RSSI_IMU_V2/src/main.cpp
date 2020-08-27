#include "WiFi.h"
#include "I2Cdev.h"

#include "MPU6050_6Axis_MotionApps20.h"
MPU6050 mpu;
//Wifi info 

const char* ssid = "The_Lair_of_Task_&_Jakiro";
const char* password = "Divine_Rapier_330";

const uint16_t port = 8007;
const char * host = "192.168.0.9";
String data;
#define OUTPUT_READABLE_WORLDACCEL
String tab = "X";

#define INTERRUPT_PIN 23  // use pin 2 on Arduino Uno & most boards
#define LED_PIN 13 // (Arduino is 13, Teensy is 11, Teensy++ is 6)
bool blinkState = false;

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


unsigned long Time_counter = 0;

int16_t Ax[800];
int16_t Ay[800];
int16_t Az[800];
unsigned long timeArray[800];
int Array_counter = 0;
void addValues(int Array_counter, int16_t AxWorld,int16_t AyWorld,int16_t AzWorld){
  Ax[Array_counter] = AxWorld;
  Ay[Array_counter] = AyWorld;
  Az[Array_counter] = AzWorld;
  timeArray[Array_counter] = millis();
}
void PrintValues(int Array_counter){
  Serial.print("aworld\t");
  Serial.print(Ax[Array_counter]);
  Serial.print("\t");
  Serial.print(Ay[Array_counter]);
  Serial.print("\t");
  Serial.print(Az[Array_counter]);
  Serial.print("\t time \t");
  Serial.println(timeArray[Array_counter]);  
}

//void ServerSendValues(int Array_counter, WiFiClient client){
// String tab = "   ";
//  String data = "aworld   " + Ax[Array_counter] + tab + Ay[Array_counter] + tab + Az[Array_counter] + tab + timeArray[Array_counter];
//  client.print(data);  
//}

void SendData(String data){
  WiFiClient client;
 
  if (!client.connect(host, port)) {
 
    Serial.println("Connection to host failed");
 
    delay(1000);
    return;
  }
  client.print(data);
  client.stop();
}
// ================================================================
// ===               INTERRUPT DETECTION ROUTINE                ===
// ================================================================

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
            mpu.dmpGetAccel(&aa, fifoBuffer);
            mpu.dmpGetGravity(&gravity, &q);
            mpu.dmpGetLinearAccel(&aaReal, &aa, &gravity);
            mpu.dmpGetLinearAccelInWorld(&aaWorld, &aaReal, &q);
            //Serial.print("aworld\t");
            //Serial.print(aaWorld.x);
            //Serial.print("\t");
            //Serial.print(aaWorld.y);
            //Serial.print("\t");
            //Serial.println(aaWorld.z);
        #endif
    }
}

// ================================================================
// ===                      INITIAL SETUP                       ===
// ================================================================

void setup()
{
    Serial.begin(115200);

    // Set WiFi to station mode and disconnect from an AP if it was previously connected
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    delay(100);
    
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.println("...");
    }
 
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
    Serial.println("Setup done");

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

    // configure LED for output
    pinMode(LED_PIN, OUTPUT);
}

void loop()
{
  MPU_Update();
  addValues(Array_counter, aaWorld.x, aaWorld.y, aaWorld.z);
  Array_counter ++;
  if (millis() >= Time_counter + 30000) {
    Time_counter = millis();
    data = "Data Start:";
    while (Array_counter > 0){
      Array_counter = Array_counter - 1;
      PrintValues(Array_counter);
      data = data + tab + Ax[Array_counter] + tab + Ay[Array_counter] + tab + Az[Array_counter] + tab + timeArray[Array_counter];
    }
    data = data + WifiScan_Update();
    data = data + "   End";
    SendData(data);
    //PrintValues(Array_counter);
    Serial.print(data);
    Serial.print(data.length());
  }

  // Wait a bit before scanning again
  delay(40);
  // if programming failed, don't try to do anything


}