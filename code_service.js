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
	var messenger = ClearBlade.Messaging()  
    const collection = "ble_devices"
    var ble_col = ClearBlade.Collection( {collectionName: collection } );
    const TOPIC = "ble/_platform";  
	
    messenger.subscribe(TOPIC, function(err, data) {
        if(err) {
            resp.error("subscribe error : " + JSON.stringify(data))
        }
        while (true) {
            messenger.waitForMessage([TOPIC], function(err, msg, topic) {
                if(err) {
                    resp.error("message error : " + JSON.stringify(msg));
                }
                log("msg = "+ JSON.stringify(msg))
                log("topic = "+topic)
                logMsgToCollection(msg,topic)
            })
        }
    })

    function logMsgToCollection(msg, topic) {
        // DEBUG MESSAGE
        log("recording message " +JSON.stringify(msg)+ " from "+ topic + " to "+ ble_devices);
        var newDevice = {
            time: new Date(),
            addr: msg.addr
        };
        if (msg.name) {
            newDevice.name = msg.name
        }
        log("newDevice = "+JSON.stringify(newDevice))
        //this inserts the the newDevice item into the collection that col represents
        ble_col.create(newDevice, function (err, data) {
            if (err) {
                resp.error("creation error : " + JSON.stringify(data));
            } else {
                resp.success(data);
            }
        })
    
	}		  
    resp.success("Success");
}
