/*
References PacketClient.cpp provided by NatNet SDK
Written by Emily Lam, adapted by Noah Robitshek Summer 2024

TODO: Adapt this to write to to a text file in format: {epoch time, x, y, z}
*/
const { InfluxDB, Point } = require('@influxdata/influxdb-client');

// Required modules
const dgram = require('dgram');           // UDP Datagrams
const process = require("process");       // Node.js process

// IPs and ports -- match information on Motive GUI
var PORT_MOTIVE = 1511;                   // Motive NatNet data channel
var LOCAL = '0.0.0.0';                    // All IPs on local machine
const MULTICAST_ADDR = '239.255.42.99';   // Motive NatNet multicast IP

// NATNET message ids
const NAT_FRAMEOFDATA = 7;                // ID for data frame

// Global variables for InfluxDB connection
const influxDBToken = process.env.INFLUXDB_TOKEN; // Replace with your token
const influxDBUrl = 'http://localhost:8086'; // Replace with your InfluxDB URL
const influxDBOrg = 'littlelab'; // Replace with your InfluxDB organization
const influxDBBucket = 'TaskingProject'; // Replace with your InfluxDB bucket name

// NATNET 3.1 compatiable with Motive 2.1.0 -- Tested July 9th, 2019
var major = 3;
var minor = 1;

// Define rigidbodies object
var rigidBodies = {};

// Function to write data to InfluxDB
async function writeToInfluxDB(data) {
  // Create InfluxDB client instance
  const client = new InfluxDB({ url: influxDBUrl, token: influxDBToken });

  // Get write API for the specified organization and bucket
  const writeApi = client.getWriteApi(influxDBOrg, influxDBBucket);

  try {
    // Create a Point with measurement name and fields
    const point = new Point('measurement1')
      .tag('ID', String(data.ID)) // Assuming ID should be stored as a tag (string)
      .floatField('x', data.x) // Store x as a float field
      .floatField('z', data.z); // Store z as a float field

    // Write the point to InfluxDB
    await writeApi.writePoint(point);

    // Ensure all pending writes are flushed to InfluxDB
    await writeApi.flush();

    console.log('Data written successfully to InfluxDB');
  } catch (error) {
    console.error('Error writing to InfluxDB', error);
  } finally {
    // Close the write API connection
    writeApi.close();
  }
}


// Create a UDP socket and bind -- For Optitrack/Motive/NatNet
const socketOpti = dgram.createSocket({ type: "udp4", reuseAddr: true });
socketOpti.bind({address: LOCAL, port: PORT_MOTIVE}, function() {
  socketOpti.addMembership(MULTICAST_ADDR);
});

// Logs >> UDP socket listening on 0.0.0.0:1511 pid: XXXX
socketOpti.on("listening", function() {
  const address = socketOpti.address();
  console.log(
    `UDP socket listening on ${address.address}:${address.port} pid: ${
      process.pid
    }`
  );
});

// Handles errors
socketOpti.on('error', (err) => {
  console.error(`UDP error: ${err.stack}`);
});
// Handles messages
socketOpti.on('message', (msg, rinfo) => {
  // console.log('---------------------------');
  // console.log('Recieved UDP message');
 
  // console.log(msg);
  parseData(msg);
});

// Functions //////////////////////////////////////////////////////////////////

// Parse data -- little endian
async function parseData(msg) {
  // Msg buffer index
  var offset = 0;

  // First 2 Bytes is message ID
  var msgID = msg.readUIntLE(offset, 2); offset += 2;
  // console.log('Message: ' + msgID.toString(8));

  // // Second 2 Bytes is the size of the packet
  var nBytes = msg.readUIntLE(offset, 2); offset += 2;
  // console.log('Bytes received: ' + nBytes.toString(8));

  // If FRAME OF MOCAP DATA packet (there are other message IDs)
  if (msgID == NAT_FRAMEOFDATA) {
    // console.log('Parsing data frame');

    // Next 4 Bytes is the frame number
    var frameNumber = msg.readUInt32LE(offset, offset += 4);
    // console.log('Frame: ' + frameNumber);

    // -----

    // Markersets (ignored) -----
    var nMarkerSets = msg.readUInt32LE(offset, offset += 4);
    // console.log('Markersets: ' + nMarkerSets);

    // Unlabeled markersets (ignored) -----
    var nOtherMarkerSets = msg.readUInt32LE(offset, offset += 4);
    // console.log('OtherMarkersets: ' + nOtherMarkerSets);

    // Rigid bodies -----

    // Next 4 Bytes is the number of rigidbodies
    var nRigidBodies = msg.readUInt32LE(offset, offset += 4);
    // console.log('RigidBodies: ' + nRigidBodies);

    var j;
    for (j = 0; j < nRigidBodies; j++) {
      // Rigid body ID
      var rID = msg.readUInt32LE(offset, offset += 4);
      // console.log('Rigidbody ID: ' + rID);

      // Rigid body position
      var x = msg.readFloatLE(offset, offset += 4);
      var y = msg.readFloatLE(offset, offset += 4);
      var z = msg.readFloatLE(offset, offset += 4);

      const dataToWrite = { ID: rID, x: ((x*1000).toFixed(4)), z: ((z*1000).toFixed(4)) };

      // console.log(dataToWrite);

      await writeToInfluxDB(dataToWrite);
    }
  }
}
