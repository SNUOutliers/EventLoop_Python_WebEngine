var http = require('http');
var fs = require('fs');
 
http.createServer(function (req, res) {
	if (req.url == '/') {
		res.writeHead(200, {'Content-Type':'*/*'});
		res.write('');
		res.end();
		return;
	}
	fs.readFile('../resources' + req.url, 'utf-8', function (err,data) {
   	 	res.writeHead(200, {'Content-Type': '*/*'});
     	res.write(data);
    	res.end();
	});
}).listen(8080);
