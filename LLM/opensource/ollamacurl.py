curl -X POST http://localhost:11434/api/generate -d '{"model": "deepseek-r1:1.5b","prompt": "Write a function that calculates fibonacci numbers","stream": true}'
curl -X POST http://localhost:11434/api/generate -d '{"model": "deepseek-r1:1.5b","prompt": "Write a function that calculates fibonacci numbers","stream": false}' -o response.json

curl -s -X POST http://localhost:11434/api/generate \
  -d '{"model": "deepseek-r1:1.5b", "prompt": "Write a function that calculates fibonacci numbers", "stream": false}' \
| jq -r '.response'


