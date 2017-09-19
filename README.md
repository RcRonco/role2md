# role2md
A python script to generate Markdown table from [Ansible](https://github.com/ansible/ansible) role for documentation.

## Prerequisites
1. python 3
2. python 3 packages jinja2, yaml.

## Installation
1. Install python 3

  ```shell
    # Ubuntu
    sudo apt-get install python3 python3-pip
    
    # rhel/centos from epel repository
    sudo yum install python34 python34-pip
    
    # fedora 23+
    sudo dnf install python3 python3-pip 
  ```
  
2. Install the needed python packages
  
  ``` shell
  pip3 install -U pyYAML
  pip3 install -U jinja2
  ```
3. Add a execution permissions to the script

  ```shell
  sudo chmod +x role2md.py
  ```

4. Run the script!

## Running the script
To run the script all you need is to run the command in this format:
```shell
./role2md.py /path/to/role
or
python -m ./role2md.py /path/to/role
```

## Example

###### Thanks to the [nginx role](https://github.com/bennojoy/nginx) from [bennojoy](https://github.com/bennojoy) for testing
```shell
# Running the script
./role2md.py ./test/nginx
```

| Name    | Description    | Required    | Default    | Values | Examples |
|:--|:--|:-:|:-:|:-:|:--|
| ansible_managed | Please fill the description. | Yes | - | - | Please fill the example. |
| ansible_os_family | Please fill the description. | Yes | - | - | Please fill the example. |
| ansible_processor_count | Please fill the description. | Yes | - | - | Please fill the example. |
| item | Please fill the description. | Yes | - | - | Please fill the example. |
| item:server:file_name | Please fill the description. | Yes | - | - | Please fill the example. |
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
| nginx_sites | Please fill the description. | No | [{'server': {'file_name': 'foo', 'server_name': 'localhost', 'root': '/tmp/site1', 'location2': {'try_files': '$uri $uri/ /index.html', 'name': '/images/'}, 'location1': {'try_files': '$uri $uri/ /index.html', 'name': '/'}, 'listen': 8080}}, {'server': {'file_name': 'bar', 'server_name': 'ansible', 'root': '/tmp/site2', 'location2': {'try_files': '$uri $uri/ /index.html', 'name': '/images/'}, 'location1': {'try_files': '$uri $uri/ /index.html', 'name': '/'}, 'listen': 9090}}] | - | Please fill the example. |



## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

