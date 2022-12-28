# OpcodeDoc

OpcodeDoc is the name of this website and the protocol for documenting opcodes of various CPU's and VM bytecode's.

The goal of this project is to create a one-stop shop where both emulator and compiler developers can find information about the different CPU's and VM's in a consistent format.

## OpcodeDoc Spec

The OpcodeDoc Spec format is a JSON file with various blocks of data. The idea behind this format is to provide a consistent format that can be easily consumed by a program, so you can generate source code from it, for example, as is the case with OpenAPI.

### Metablocks

There are currently two types of metablocks. Each metablock begins with a `$`-Character.

```json
"$spec": "1.0.0"
```

This block contains the version number of the specification used for a file. The versioning type used here is [semver](https://semver.org/).

```json
"$info": {
    "title": "Name of the Processor / VM",
    "description": "Description of what type of processor we are dealing with",
    "clock_speed": "Clock speed of the processor + unit (Hz, KHz, MHz, GHz)",
    "cache": {
        "CACHE NAME e.g. L1": {
            "size": "Size of the cache + unit (B, KB, MB)",
            "comment": "Additional comment e.g. Special use case"
        }

        Multiple caches are possible.
    },
    "address_bus": Size of the address bus in bits e.g. 32 or 0 if unknown,
    "version": "Document version also in semver starting by 1.0.0",
    "sources": [ "Where does all this information come from? We don't want any plagiarize." ],
    "complete": true or false if this document is not complete
}
```

```json
"glossary": {
    "Term": "Explanation"
}
```

The glossary is for web documentation only.

```json
"registers": {
    "Core or processor name e.g. Main": [
        {"name": "Name of the register", "value": "Value of the register", "size": Size of the register in bits}
    ]
}
```

The register block contains a map of different cores or processing units, each of which can have its own register.

```json
"groups": [
    "Group name"
]
```

The groups can be referenced by each opcode. This helps to categories the opcodes on the web interface.

```json
"opcodes": [
    {
        "group": Group index starting with 1 for the first group in the group array or 0 for no group,
        "name": "Name of the assembly e.g. MOV",
        "opcode": Opcode value e.g. 50,
        "decode": {
            "Name for a variable or just a binary value": Size in bits
        },
        "format": "Assembly example on how to use this introduction e.g. MOV reg1, reg2",
        "purpose": "What does this command?",
        "description": "Example of how an emulator might emulate this command e.g. reg2 = reg1"
    }
]
```

This block describes how an opcode works and is encoded. The decoding map shows how a sequence of bytes can be decoded to get all the necessary values, or conversely, how an assembler introduction is encoded.

> For more information you can have a look at some files in the spec folder.

# License

All files, except the files inside the specs and fonts folder, are under the [MIT License](LICENSE). The informations, which are inside the `specs/*.json`, are without warranty of correctness or completeness.