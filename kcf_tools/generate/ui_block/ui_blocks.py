base_schema = {
    "type": "object",
    "title": "Configuration",
    "required": [
    ],
    "properties": {
    }
}

use_ssh_block = {"use_ssh": {
    "title": "SSH",
    "type": "boolean",
    "propertyOrder": 10,
    "format": "checkbox",
    "description": "If checked SSH will be used for connection"
}}

ssh_block = {
    "ssh": {
        "title": "SSH",
        "type": "object",
        "required": [
            "hostname",
            "port",
            "username",
            "#private_key"
        ],
        "options": {
            "dependencies": {
                "use_ssh": True
            }
        },
        "propertyOrder": 100,
        "properties": {
            "hostname": {
                "title": "SSH Hostname",
                "type": "string",
                "propertyOrder": 10
            },
            "port": {
                "title": "SSH Port",
                "type": "integer",
                "propertyOrder": 20,
                "default": 22
            },
            "username": {
                "title": "SSH Username",
                "type": "string",
                "propertyOrder": 30
            },
            "#private_key": {
                "title": "SSH Private Key",
                "type": "string",
                "propertyOrder": 40,
                "description": "Base64 encoded SSH private key"
            }
        }
    }}

sync_options_block = {"sync_options": {
    "type": "object",
    "title": "Sync Options",
    "propertyOrder": 200,
    "properties": {
        "sync_mode": {
            "required": True,
            "type": "string",
            "title": "Sync Mode",
            "enum": [
                "Full Sync",
                "Incremental Sync"
            ],
            "default": "Full Sync",
            "description": "Full Sync downloads all data from the source every run, Incremental Sync downloads data created or updated in a specified time range",
            "propertyOrder": 10
        },
        "date_from": {
            "type": "string",
            "title": "Date From",
            "default": "last run",
            "description": "Date from which data is downloaded. Either date in YYYY-MM-DD format or dateparser string i.e. 5 days ago, 1 month ago, yesterday, etc. You can also set this as last run, which will fetch data from the last run of the component.",
            "propertyOrder": 20,
            "options": {
                "dependencies": {
                    "sync_mode": "Incremental Sync"
                }
            }
        },
        "date_to": {
            "type": "string",
            "title": "Date to",
            "default": "now",
            "description": "Date from which data is downloaded. Either date in YYYY-MM-DD format or dateparser string i.e. 5 days ago, 1 month ago, now, etc.",
            "propertyOrder": 30,
            "options": {
                "dependencies": {
                    "sync_mode": "Incremental Sync"
                }
            }
        }
    }
}}
sync_options_with_custom_field_block = {"sync_options": {
    "type": "object",
    "title": "Sync Options",
    "propertyOrder": 300,
    "properties": {
        "sync_mode": {
            "type": "string",
            "title": "Sync Mode",
            "required": True,
            "enum": [
                "Full Sync",
                "Incremental Sync"
            ],
            "default": "Full Sync",
            "description": "Full Sync downloads all data from the source every run, Incremental Sync downloads data created or updated in a specified time range",
            "propertyOrder": 10
        },
        "date_from": {
            "type": "string",
            "title": "Date From",
            "default": "last run",
            "description": "Date from which data is downloaded. Either date in YYYY-MM-DD format or dateparser string i.e. 5 days ago, 1 month ago, yesterday, etc. You can also set this as last run, which will fetch data from the last run of the component.",
            "propertyOrder": 20,
            "options": {
                "dependencies": {
                    "sync_mode": "Incremental Sync"
                }
            }
        },
        "date_to": {
            "type": "string",
            "title": "Date to",
            "default": "now",
            "description": "Date from which data is downloaded. Either date in YYYY-MM-DD format or dateparser string i.e. 5 days ago, 1 month ago, now, etc.",
            "propertyOrder": 30,
            "options": {
                "dependencies": {
                    "sync_mode": "Incremental Sync"
                }
            }
        },
        "incremental_field": {
            "type": "string",
            "title": "Incremental Field",
            "default": "LastModified",
            "description": "Field/column to be used for incremental fetching",
            "propertyOrder": 40,
            "options": {
                "dependencies": {
                    "sync_mode": "Incremental Sync"
                }
            }
        }
    }
}}

destination_block = {"destination": {
    "title": "Destination",
    "type": "object",
    "propertyOrder": 400,
    "required": [
        "output_table_name",
        "incremental"
    ],
    "properties": {
        "output_table_name": {
            "type": "string",
            "title": "Storage Table Name",
            "description": "Name of the table stored in Storage.",
            "propertyOrder": 10
        },
        "incremental": {
            "type": "boolean",
            "format": "checkbox",
            "title": "Incremental Load",
            "description": "If incremental load is turned on, the table will be updated instead of rewritten. Tables with a primary key will have rows updated, tables without a primary key will have rows appended.",
            "propertyOrder": 20
        },
        "primary_keys": {
            "type": "string",
            "title": "Primary Keys",
            "description": "List of primary keys separated by commas e.g. id, other_id. If a primary key is set, updates can be done on the table by selecting incremental loads. The primary key can consist of multiple columns. The primary key of an existing table cannot be changed.",
            "propertyOrder": 30
        }
    }
}}

report_settings_block = {"report_settings": {
    "title": "Report Settings",
    "type": "object",
    "propertyOrder": 500,
    "required": [
        "dimensions",
        "metrics",
        "report_type",
        "date_from",
        "date_to"
    ],
    "properties": {
        "report_type": {
            "title": "Report type",
            "type": "string",
            "required": True,
            "enum": [
                "TYPE 1",
                "TYPE 2"
            ],
            "default": "Object",
            "propertyOrder": 10,
            "description": "Select one of the available report types described in the <a href='https://google.com'>documentation</a>"
        },
        "dimensions": {
            "type": "string",
            "title": "Dimensions",
            "format": "textarea",
            "options": {
                "input_height": "100px"
            },
            "description": "Comma separated list of dimensions to use for the report, find supported dimensions for specific report types in the <a href='https://google.com'>documentation</a>",
            "propertyOrder": 20
        },
        "metrics": {
            "type": "string",
            "format": "textarea",
            "options": {
                "input_height": "100px"
            },
            "title": "Metrics",
            "description": "Comma separated list of metrics to use for the report, find supported dimensions for specific report types in the <a href='https://google.com'>documentation</a>",
            "propertyOrder": 30
        },
        "date_from": {
            "type": "string",
            "title": "Date From",
            "default": "1 week ago",
            "description": "Start date of the report. Either date in YYYY-MM-DD format or dateparser string i.e. 5 days ago, 1 month ago, yesterday, etc.",
            "propertyOrder": 40
        },
        "date_to": {
            "type": "string",
            "title": "Date to",
            "default": "now",
            "description": "End date of the report. Either date in YYYY-MM-DD format or dateparser string i.e. 5 days ago, 1 month ago, yesterday, etc.",
            "propertyOrder": 50
        }
    }
}}
