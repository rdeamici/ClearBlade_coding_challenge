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

 function rpi_analytics(req,resp){
    const ms_per_hour = 3600000
    const TOPIC='analytics'
    var right_now = new Date()-(ms_per_hour*7)
    log("right_now = "+right_now)
    var prev_hour = new Date(right_now - ms_per_hour)
    log("prev_hour == "+prev_hour)
	
    ClearBlade.init({request:req});
    var msg = ClearBlade.Messaging();
    var rpi_query = ClearBlade.Query({collectionName: "rPISystemInfo"})        
    rpi_query.greaterThan("date_time", prev_hour)
    
    // compute ram usage percentage and percentage increase hour over hour
    function ram_usage_info(data) {
        var tot_entries_last_hour = data.length
        var total_avail = 0
        data.forEach(function(entry){total_avail+=entry.available_ram})
        var av_percentage = (total_avail/tot_entries_last_hour)/data[0].total_ram
        message = "average percentage of ram in use last hour was "+parseInt(Math.ceil(av_percentage*100))+"%"
        msg.publish(TOPIC,message)
    }
    // compute avg num processes last hour
    function av_num_processes(data) {
        tot_entries_last_hour = data.length
        var total_processes = 0
        data.forEach(function(entry) {total_processes+=entry.number_of_running_processes})
        
        var avg_per_hour = Math.ceil(total_processes / tot_entries_last_hour)
        message = "average number of active processes running at any point last hour was "+parseInt(avg_per_hour)
        msg.publish(TOPIC,message)
    }
    function temp_analytics(data) {
        var highest_temp = 0
        var num_processes = 0
        
        var total_temp = 0
        var avg_temp = 0

        data.forEach(function(entry) {
            if (entry.device_temperature> highest_temp) {
                highest_temp = +(entry.device_temperature)
                num_processes = entry.number_of_running_processes
            }
            total_temp += +(entry.device_temperature)
        })
        avg_temp = Math.ceil(total_temp/data.length)
        log("avg temp = ")
        log(avg_temp)
        message = "The highest recorded temperature last hour was "+parseFloat(highest_temp)
        message += "'F. "+parseInt(num_processes)+" processes were running at the time."
        message += " This temp was "+parseInt(highest_temp-avg_temp)+" degrees higher than the average temp of "+parseInt(avg_temp)
        msg.publish(TOPIC, message)
    }
    function ble_device_info(data) {
        rpi_model = data[0].raspberry_model
        rpi_serial = data[0].raspberry_serial_num
        log(data)
        log(rpi_serial)
        var ble_devices = ClearBlade.Collection({collectionName: "ble_devices"})
        var ble_query = ClearBlade.Query()
        
        ble_query.greaterThan("date",prev_hour)
        ble_devices.count(ble_query, function(err,resp) {
            if (err) {
                resp.error("fetch error : " + JSON.stringify(resp));
            }
            var count = 0
            count = data.count
            var message = ""
            if (count > 0) {
                message += parseInt(count)
            } else {
                message += "No "
            }
            message += "new Bluetooth devices came within range of the "
            message += rpi_model+" serial number: "+rpi_serial
            msg.publish(TOPIC,message)
        })

    }

    rpi_query.fetch(function (err, resp) {
        if (err) {
            resp.error("fetch error : " + JSON.stringify(resp));
        }
        log(resp)
        data = resp.DATA
        log(data)
        
        ram_usage_info(data)
        av_num_processes(data)
        // compute avg temperature, hottest_temperature
        temp_analytics(data)
        // publish a message if new ble devices in range detected
        ble_device_info(data)
    })
    resp.success("Success");
}
