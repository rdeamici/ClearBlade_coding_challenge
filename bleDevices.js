/**
 * Type: Micro Service
 * Description: A short-lived service which is expected to complete within a fixed period of time.
 * @param {CbServer.BasicReq} req
 * @param {string} req.systemKey
 * @param {string} req.systemSecret
 * @param {string} req.userEmail
 * @param {string} req.userid
 * @param {string} req.userToken
 * @param {boolean} req.isLogging
 * @param {[id: string]} req.params
 * @param {CbServer.Resp} resp
 */

function bleDevices(req,resp) {
    log("req = "+JSON.stringify(req))
    ClearBlade.init({request:req});

    if(!req.params.body) {
        resp.error("Body not passed")
    }
    var newDevice = JSON.parse(req.params.body)
    newDevice.date = new Date()
    
    log("newDevice = "+JSON.stringify(newDevice))
    
    const ble_collection = "de83e2880ca4b886938cfbbbac2c"
    var ble_col = ClearBlade.Collection( {collectionID: ble_collection } );

    ble_col.create(newDevice, function (err, data) {
        if (err) {
            resp.error("creation error : " + JSON.stringify(data));
        }

	log("data added to "+collection+" = "+data)
    })

    resp.success("Successfully added "+JSON.stringify(newDevice)+" to collection "+ble_collection);
}
