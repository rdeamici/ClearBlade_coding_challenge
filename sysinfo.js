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

 function collectSystemInfo(req,resp) {
    log("req = "+JSON.stringify(req))
    ClearBlade.init({request:req});

    if(!req.params.body){
		resp.error("Body not passed")
	}
	var sys_info = JSON.parse(req.params.body)
    sys_info.date_time = new Date()
    log("sys_info = "+JSON.stringify(sys_info))

    const rPISystemInfoCollection = "d8f0ee880cdaf9ead3a8cef69628"
    var sysInfo_col = ClearBlade.Collection( {collectionID: rPISystemInfoCollection } );
    sysInfo_col.create(sys_info, function (err, data) {
            if (err) {
                resp.error("creation error : " + JSON.stringify(data));
            }
            log("data added to "+rPISystemInfoCollection+" = "+data)
        })
    resp.success("Successfully added "+JSON.stringify(sys_info)+" to collection "+rPISystemInfoCollection);
}
