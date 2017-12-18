var http = require('http');
var fs = require('fs');

http.createServer(function (req, res) {
		fs.readFile('../resources' + req.url, 'utf8', function (err,data) {
  		if (err) {
    		return console.log(err);
  		}
  	 	res.writeHead(200, {'Content-Type': '*/*'});
    	res.write(data);
    	res.end();
		});
}).listen(8080);

