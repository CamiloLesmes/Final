import re
import json
import json
import matplotlib.pyplot as plt
from collections import Counter

# Ruta donde podemos ver el archivo LOG
log_file_path = 'path/to/your/logfile.log'
output_json_path = 'output.json'

with open('output.json', 'r') as json_file:
    data = json.load(json_file)


ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'
date_pattern = r'(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})'
method_pattern = r'(GET|POST|PUT|DELETE)'
resource_pattern = r'\"(GET|POST|PUT|DELETE) (.*?) HTTP/[\d\.]+\"'
error_code_pattern = r'\s(\d{3})\s'


data = []

# LOG
with open(log_file_path, 'r') as file:
    for line in file:
        ip_match = re.search(ip_pattern, line)
        date_match = re.search(date_pattern, line)
        resource_match = re.search(resource_pattern, line)
        error_code_match = re.search(error_code_pattern, line)

        if ip_match and date_match and resource_match:
            entry = {
                'ip': ip_match.group(),
                'date': date_match.group(),
                'method': resource_match.group(1),
                'resource': resource_match.group(2),
                'error_code': error_code_match.group(1) if error_code_match else None
            }
            data.append(entry)

# Guarda datos
with open(output_json_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)
methods = [entry['method'] for entry in data]
method_counts = Counter(methods)

plt.figure(figsize=(10, 6))
plt.bar(method_counts.keys(), method_counts.values(), color='blue')
plt.title('Distribución Métodos de Solicitud HTTP')
plt.xlabel('Método HTTP')
plt.ylabel('Frecuencia')
plt.tight_layout()
plt.savefig('http_methods_distribution.png')
plt.show()

print(f'Datos extraídos y guardados en {output_json_path}')
