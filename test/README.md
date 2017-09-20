# nginx

install nginx ansible playbook

## Example
```yaml
---
- name: A playbook example use of nginx
  host: all
  remote_user: user
  become: yes

  roles:
    - nginx
```

## Variables
| Name    | Description    | Required    | Default    | Values | Examples |
|:--|:--|:-:|:-:|:-:|:--|
| nginx_access_log_name | Please fill the description. | No | access.log | - | Please fill the example. |
| nginx_error_log_name | Please fill the description. | No | error.log | - | Please fill the example. |
| nginx_http_params | Please fill the description. | Yes | - | - | Please fill the example. |
| nginx_http_params:keepalive_timeout | Please fill the description. | No | 65 | - | Please fill the example. |
| nginx_http_params:sendfile | Please fill the description. | No | on | - | Please fill the example. |
| nginx_http_params:tcp_nodelay | Please fill the description. | No | on | - | Please fill the example. |
| nginx_http_params:tcp_nopush | Please fill the description. | No | on | - | Please fill the example. |
| nginx_log_dir | Please fill the description. | No | /var/log/nginx | - | Please fill the example. |
| nginx_max_clients | Please fill the description. | No | 512 | - | Please fill the example. |
| nginx_separate_logs_per_site | Please fill the description. | No | False | - | Please fill the example. |
| nginx_sites | Please fill the description. | No | [{'server': {'file_name': 'foo', 'root': '/tmp/site1', 'server_name': 'localhost', 'listen': 8080, 'location1': {'name': '/', 'try_files': '$uri $uri/ /index.html'}, 'location2': {'name': '/images/', 'try_files': '$uri $uri/ /index.html'}}}, {'server': {'file_name': 'bar', 'root': '/tmp/site2', 'server_name': 'ansible', 'listen': 9090, 'location1': {'name': '/', 'try_files': '$uri $uri/ /index.html'}, 'location2': {'name': '/images/', 'try_files': '$uri $uri/ /index.html'}}}] | - | Please fill the example. |



## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
