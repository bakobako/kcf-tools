# kcf-tools

## Introduction

<code>kcf-tools</code> is a CLI tool for making Python Component development for Keboola Connection faster and easier.

PYPI project : [https://pypi.org/project/kcf-tools/](https://pypi.org/project/kcf-tools/)

It provides the following functionality;

* Generating Configuration Schemas for the UI of Keboola Components
* Generating ReadMe files for Keboola Components
* Generating documentation for Keboola Components for help.keboola.com
* Generating key definitions for parameters of Keboola Components
* Generating a client skeleton for Keboola Components

# Installation

The package may be installed via PIP:

 ```
pip install kcf-tools
```

# Functionality

The CLI provides multiple subcommands for various tasks for information on all subcommands run:

 ```
kcf-tools -h
```

## Generate subcommand

The generate subcommand is used for generating various files for you component. To list all possible **generate**
commands run:

 ```
kcf-tools generate -h
```

### Generate ReadMe

The readme generator uses the component config to generate a readme file. The readme file is then saved in
generated/readme directory. To generate a readme run:

 ```
kcf-tools generate readme
```

If you want to write directly to your component ReadMe then add the tag <code>-w</code>:

 ```
kcf-tools generate readme -w
```

### Help Documentation Generator

The doc generator uses the component config to generate an index.md in the necessary directory. The documentation files
are then saved in generated directory. To generate a docs run:

 ```
kcf-tools generate docs
```

### Config Schema Generator

The Config Schema Generator will take the parameters in the config.json and create a config schema and config row schema
based on some questions answered with the cli tool. The config schemas are saved to a "generated/config_schemas"
directory. To generate your config schemas run :

 ```
kcf-tools generate config_schema
```

If you want to write directly to your component "component_config" directory then add the tag <code>-w</code>:

 ```
kcf-tools generate config_schema -w
```

### Key Definition Generator

The Key Definition Generator will use the config.json file to generate all key definitions. These will then be printed
to the command line. To generate your key definitions run :

 ```
kcf-tools generate key_definitions
```

### Client Generator

The Client Generator will generate a skeleton for your component client with the Keboola Http-Client library. The
Client will be saved to the "generated/client" directory. To generate a client run:

 ```
kcf-tools generate client
```
If you want to write directly to your component src directory then add the tag <code>-w</code>:

 ```
kcf-tools generate client -w
```