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
  pip3 install -U yaml
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
python -m ./role2md.py
```

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

