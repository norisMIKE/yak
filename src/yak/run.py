import json
import os
import click
import git
import sqlalchemy as sa

from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path


# [YAK] Yak Aiohttp devKit

@click.group()
def cli():
    pass

@click.group()
def new():
    pass

@click.command()
@click.option('--rest', is_flag=True, default=True, show_default=True,
              help='This is a REST API, don\'t create views.')
@click.option('--mysql', 'database', flag_value='aiomysql', default=True,
              show_default=True, help='Use MySQL as db tehnology')
@click.option('--pg', 'database', flag_value='aiopg',
              help='Use PostgreSQL as db tehnology')
@click.option('--settings-json', 'settings', flag_value='json',
              help='Use JSON file settings')
@click.option('--settings-yaml', 'settings', flag_value='yaml',
              help='Use YAML file settings')
@click.option('--settings-dummy', 'settings', flag_value='dummy', default=True,
              show_default=True, help='Use dummy settings (in-code)')
@click.option('--commit/--no-commit', default=True, show_default=True,
              help='Create a commit for the changes')
@click.argument('project_name')
def project(**params):
    # Build Jinja2 Template Environment
    env = Environment(
        loader= PackageLoader('yak', 'templates'),
        autoescape=select_autoescape(['python'])
    )

    # Create project path ($PWD/{project_name})
    path = Path.cwd().joinpath(params['project_name'])
    path.mkdir(parents=True, exist_ok=True)

    # Initialize git repo inside the project
    repo = git.Repo.init(str(path))

    # Create the files in the top directory
    # 'setup.py', 'requirements.txt', 'README.md'
    env.get_template('setup.py').stream(**params).dump(
        str(path.joinpath('setup.py'))
    )
    env.get_template('requirements.txt').stream(**params).dump(
        str(path.joinpath('requirements.txt'))
    )
    path.joinpath('README.md').touch()

    with open(str(path.joinpath('.yakrc')), 'w') as fl:
        json.dump(params, fl)

    # Create code source folder ($PWD/{project_name}/src)
    path = path.joinpath('src', params['project_name'])
    path.mkdir(parents=True, exist_ok=True)

    # Create base package __init__.py file
    # ($PWD/{project_name}/src/__init__.py)
    path.joinpath('__init__.py').touch()

    # Create the entry-point file of the web app
    # ($PWD/{project_name}/src/entry.py)
    env.get_template('entry.py').stream(**params).dump(
        str(path.joinpath('entry.py'))
    )

    # Create the entry-point file of the web app
    # ($PWD/{project_name}/src/middleware.py)
    env.get_template('middleware.py').stream(**params).dump(
        str(path.joinpath('middleware.py'))
    )

    # Create the CRUD views for the web app
    # ($PWD/{project_name}/src/crud.py)
    env.get_template('crud.py').stream(**params).dump(
        str(path.joinpath('crud.py'))
    )

    # Create the settings file for the web app
    # ($PWD/{project_name}/src/settings.py)
    env.get_template('settings.py').stream(**params).dump(
        str(path.joinpath('settings.py'))
    )

    # Create folder to namespace db realated namespace
    # ($PWD/{project_name}/src/db/) and
    # ($PWD/{project_name}/src/db/__init__.py)
    path = path.joinpath('db')
    path.mkdir(parents=True, exist_ok=True)
    env.get_template('db__init__.py').stream(**params).dump(
        str(path.joinpath('__init__.py'))
    )

    # Create folder to namespace db realated models
    # ($PWD/{project_name}/src/db/_base.py)
    path.mkdir(parents=True, exist_ok=True)
    env.get_template('db__base.py').stream(**params).dump(
        str(path.joinpath('_base.py'))
    )

    # When ready for first commit
    if params['commit']:
        repo.index.add(repo.untracked_files)
        repo.index.commit('[YAK] Your base project is ready')

@click.command()
@click.option('--column', 'columns', multiple=True,
              help='Column config string. Separate options with \':\'.\n'
              'Syntax: \'name:type-size[:args][:flags][:kwargs]\'\n'
              'Available Flags: '
              'autoincrement, index, primary_key, unique, system')
@click.option('--id/--no-id', default=True, show_default=True,
              help='Add an integer, auto-increment Column named "id".')
@click.option('--commit/--no-commit', default=True, show_default=True,
              help='Create a commit for the changes')
@click.argument('table_name')
def model(**params):
    # Build Jinja2 Template Environment
    env = Environment(
        loader= PackageLoader('yak', 'templates'),
        autoescape=select_autoescape(['python'])
    )

    path = Path.cwd()

    try:
        repo = git.Repo()
        with open(str(path.joinpath('.yakrc'))) as fl:
            params.update(json.load(fl))
    except (IOError, git.exc.InvalidGitRepositoryError):
        print('[YAK] This doesn\'t seem like a YAK project directory. '
              'Are you sure you\'re at the base folder of your project?')
        return 1
    columns = []
    if params['id']:
        params['columns'] = [
            'id:INT:primary_key:autoincrement:index:unique',
            *params['columns']
        ]
    for column in params['columns']:
        # Argument seperator for column definition string is ':'
        columndef = column.split(':')

        # First element is the column name
        column = { 'name': columndef.pop(0), 'args':[], 'kwargs': [] }

        # Second element is the data type
        # Split at '-'. This denotes size constraint
        column_type = columndef.pop(0).split('-')
        # Check if size constraint is present
        try:
            column_type_constraint = column_type[1]
        except IndexError:
            column_type_constraint = None

        # Extract the data type
        column_type = column_type[0].upper()

        # Check if type exists in sqlalchemy else assume it's from
        # db specific dialect
        if hasattr(sa, column_type):
            column_type = 'sa.{}'.format(column_type)
        else:
            column_type = 'dialect.{}'.format(column_type)

        # Add size constraint if one was provided
        if column_type_constraint:
            column_type += '({})'.format(column_type_constraint)

        column['type'] = column_type

        # Check for the flag kwargs accepted by sqlalchemy Column
        if 'nullable' not in columndef:
            column['kwargs'].append('nullable=False')
        else:
            columndef.remove('nullable')

        flags = (
            'autoincrement',
            'index',
            'primary_key',
            'unique',
            'system',
        )
        for flag in flags:
            if flag in columndef:
                column['kwargs'].append('{}=True'.format(flag))
                columndef.remove(flag)

        # For the remainder of the columndef elemets, they are either
        # args or kwargs. Insert them to the appropriate group in the
        # order they were provided
        for element in columndef:
            if '=' in element:
                column['kwargs'].append(element)
            else:
                column['args'].append(element)

        column['string'] = ', '.join([
            "'{}'".format(column['name']), column['type'],
            *column['args'], *column['kwargs']
        ])

        columns.append(column)

    params['columns'] = columns

    path = path.joinpath('src', params['project_name'], 'db')

    with open(str(path.joinpath('__init__.py')), 'a') as fl:
        fl.write(
            "\nfrom {}.db.{} import *".format(
                params['project_name'], params['table_name']
            )
        )

    path = path.joinpath('{}.py'.format(params['table_name']))

    env.get_template('db_model.py').stream(**params).dump(str(path))


    # TODO: Create automatic database migrations using available tools
    # see: http://docs.sqlalchemy.org/en/latest/core/metadata.html#altering-schemas-through-migrations

    if params['commit']:
        # Don't add all untracked files
        # only the files affected by the command
        # repo.index.add([str(path.relative_to(Path.cwd()))])
        repo.index.add([str(path)])
        repo.index.commit(
            '[YAK] Create model for {}'.format(params['table_name'])
        )


# Top-level commands (i.e. yak new)
cli.add_command(new)

# 'new' sub-commands (i.e. yak new project <project_name>)
new.add_command(project)
new.add_command(model)

if __name__ == '__main__':
    cli()
