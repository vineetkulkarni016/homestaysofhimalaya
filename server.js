const http = require('http');

try {
  require('dd-trace').init();
  console.log('Datadog tracer initialized');
} catch (err) {
  console.warn('Datadog tracer not initialized:', err.message);
}

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello from homestaysofhimalaya');
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
