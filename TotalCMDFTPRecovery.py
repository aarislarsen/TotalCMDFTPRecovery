import os
import argparse

RANDOM_BASE = 0


def process_file(filename):
    try:
        print(f"-> Trying: {filename}")
        with open(filename, "r") as f:
            print(f"-> Found: {filename}")
            print(f"-> Decrypting: {filename}\n")
            for line in f:
                line = line.strip()
                if "password" in line:
                    print("password=" + tc_decrypt(line.split("=")[1]))
                else:
                    print(line)
        print()
    except IOError:
        print(f"-> Not found: {filename}\n")


def search_ini():
    """Search the wcx_ftp.ini file in common places."""
    paths = [
        os.path.join(os.getenv("APPDATA", ""), "GHISLER", "wcx_ftp.ini"),
        os.path.join(os.getenv("SYSTEMROOT", ""), "wcx_ftp.ini"),
        "wcx_ftp.ini",
    ]
    for ini in paths:
        process_file(ini)


def tc_random(n_max):
    global RANDOM_BASE
    RANDOM_BASE = ((RANDOM_BASE * 0x8088405) & 0xFFFFFFFF) + 1
    return ((RANDOM_BASE * n_max) >> 32) & 0xFFFFFFFF


def tc_shift(n1, n2):
    return (((n1 << n2) & 0xFFFFFFFF) | ((n1 >> (8 - n2)) & 0xFFFFFFFF)) & 0xFF


def tc_decrypt(pwd):
    global RANDOM_BASE

    pwd = pwd.strip()
    pwlen_hex = len(pwd) // 2 - 4
    password = [int(pwd[2 * i:2 * i + 2], 16) for i in range(pwlen_hex)]
    pwlen = len(password)

    RANDOM_BASE = 849521
    for i in range(pwlen):
        password[i] = tc_shift(password[i], tc_random(8))

    RANDOM_BASE = 12345
    for _ in range(256):
        a = tc_random(pwlen)
        b = tc_random(pwlen)
        password[a], password[b] = password[b], password[a]

    RANDOM_BASE = 42340
    for i in range(pwlen):
        password[i] = (password[i] ^ tc_random(256)) & 0xFF

    RANDOM_BASE = 54321
    for i in range(pwlen):
        password[i] = (password[i] - tc_random(256)) & 0xFF

    return "".join(chr(b) for b in password)


def main():
    parser = argparse.ArgumentParser(
        prog="TotalCMDFTPRecovery",
        description="Recover and decrypt FTP passwords stored by Total Commander (wcx_ftp.ini).",
        epilog='Example: TotalCMDFTPRecovery -c | TotalCMDFTPRecovery -f /path/to/wcx_ftp.ini | TotalCMDFTPRecovery -p <hex_password>'
    )
    parser.add_argument("-c", "--common", action="store_true", default=False,
                        help="Search for wcx_ftp.ini in common Total Commander installation paths")
    parser.add_argument("-f", "--file", default="",
                        help="Path to a wcx_ftp.ini file to decrypt")
    parser.add_argument("-p", "--password", default="",
                        help="Single obfuscated hex password string to decrypt")
    args = parser.parse_args()

    if args.common:
        search_ini()
    if args.file:
        process_file(args.file)
    if args.password:
        print(f"Decrypted password: {tc_decrypt(args.password)}")
    if not args.common and not args.file and not args.password:
        print('Nothing specified, run "TotalCMDFTPRecovery -h" for options')


if __name__ == "__main__":
    main()
