# YAK

> YAK (Yak Aiohttp devKit) is a tool to help you kickstart your application and keep your CRUDs [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself).

## Features

* Create project boilerplate
    * Folder Structure
    * setup.py
    * requirements.txt
    * git
    * Out of the Box modular CRUD
* Create models directly from the cli

## Development

For development it's suggested to use virtual environments. See [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/).

After activating a virtual env, instal YAK in editable mode:


```sh
pip install -e .
```

## Build

```sh
PYTHONDONTWRITEBYTECODE=1 python3 setup.py bdist_wheel
```

## TODO

- [ ] Travis integration for automatic releases
- [ ] Travis integration for PR testing
- [ ] Unit tests (for YAK itself)
- [ ] Generate unit tests (in the generated applications)
- [ ] Documentation
- [ ] More settings formats (currently only dummy is implemented)
- [ ] Web views using Jinja2 Templates
- [ ] Use of environment variables for defaults / settings
- [ ] (Far future) Automated docs generation
- [ ] (Far future) Better querying options (search etc)

## Contributors

* [panagiks](https://github.com/panagiks/) // Author

## License

MIT
