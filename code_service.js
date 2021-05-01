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

    if(!req.params.body){
		resp.error("Body not passed")
	}
	var newDevice = JSON.parse(req.params.body)
    log("newDevice = "+JSON.stringify(newDevice))
    
    const collection = "ble_devices"
    var ble_col = ClearBlade.Collection( {collectionName: collection } );
    ble_col.create(newDevice, function (err, data) {
            if (err) {
                resp.error("creation error : " + JSON.stringify(data));
            }
        })
    resp.success("Successfully added "+JSON.stringify(newDevice)+" to collection " +collection);
}
