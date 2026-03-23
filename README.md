# TotalCMDFTPRecovery

A Python 3 rewrite of [tcpwrecovery](https://github.com/theevilbit/tcpwrecovery) by Csaba Fitzl ([@theevilbit](https://github.com/theevilbit)).

Recovers and decrypts FTP passwords stored by [Total Commander](https://www.ghisler.com/) in `wcx_ftp.ini`.

---

## Background

Total Commander stores FTP credentials in `wcx_ftp.ini` using a custom obfuscation algorithm. This tool reverses that algorithm to recover plaintext passwords. The original implementation was written in Python 2 by Csaba Fitzl. This project ports it to Python 3 with minor code quality improvements, while preserving the original decryption logic exactly.

---

## Differences from the Original

| | [tcpwrecovery](https://github.com/theevilbit/tcpwrecovery) | TotalCMDFTPRecovery |
|---|---|---|
| Python version | 2 | 3 |
| Argument parser | `optparse` | `argparse` |
| File handling | Manual `open`/`close` | `with` context manager |
| Integer division | `/` | `//` |
| Output | `print` statements | `print()` functions |

The underlying decryption algorithm (`tc_decrypt`, `tc_random`, `tc_shift`) is unchanged.

---

## Requirements

- Python 3.6+
- No third-party dependencies

---

## Usage

```
TotalCMDFTPRecovery [-h] [-c] [-f FILE] [-p PASSWORD]
```

### Options

| Flag | Description |
|---|---|
| `-c`, `--common` | Search for `wcx_ftp.ini` in common Total Commander installation paths |
| `-f`, `--file FILE` | Path to a specific `wcx_ftp.ini` file to decrypt |
| `-p`, `--password PASSWORD` | Decrypt a single obfuscated hex password string |
| `-h`, `--help` | Show help message and exit |

### Examples

Search common paths automatically:
```bash
python TotalCMDFTPRecovery.py -c
```

Target a specific `wcx_ftp.ini`:
```bash
python TotalCMDFTPRecovery.py -f /path/to/wcx_ftp.ini
```

Decrypt a single password hash:
```bash
python TotalCMDFTPRecovery.py -p 4a3f1e2b...
```

---

## Common `wcx_ftp.ini` Locations (Windows)

| Path |
|---|
| `%APPDATA%\GHISLER\wcx_ftp.ini` |
| `%SYSTEMROOT%\wcx_ftp.ini` |
| `.\wcx_ftp.ini` (current directory) |

---

## Credits

- Original tool and decryption research: [Csaba Fitzl (@theevilbit)](https://github.com/theevilbit/tcpwrecovery)
