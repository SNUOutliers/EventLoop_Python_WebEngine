var http = require('http');
var fs = require('fs');
var path = require('path');

http.createServer(function (req, res) {
	var filePath = path.join('../resources', req.url);
	var stat = fs.statSync(filePath);

	res.writeHead(200, {
		'Content-Type': '*/*',
		'Content-Length': stat.size
	});

	var readStream = fs.createReadStream(filePath);
	// We replaced all the event handlers with a simple call to readStream.pipe()
	readStream.pipe(res);
}).listen(8080);

