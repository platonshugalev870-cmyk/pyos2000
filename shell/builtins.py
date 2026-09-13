def cmd_exit(shell, args):
    shell.quit()


def cmd_cls(shell, args):
    shell.colors.clear()


def cmd_echo(shell, args):
    print(" ".join(args))


def cmd_help(shell, args):
    print(shell.colors.c("Available commands:", shell.colors.yellow))
    for name in sorted(shell.commands.list()):
        print("  " + name)


def cmd_cd(shell, args):
    if not args:
        shell.cwd = "/"
        return
    target = args[0]
    if target == "..":
        parts = [p for p in shell.cwd.split("/") if p]
        shell.cwd = "/" + "/".join(parts[:-1]) if parts[:-1] else "/"
        return
    new = (shell.cwd.rstrip("/") + "/" + target).replace("//", "/")
    if shell.vfs.exists(new):
        shell.cwd = new
    else:
        print(shell.colors.c("Path not found.", shell.colors.red))


BUILTINS = {
    "exit": cmd_exit,
    "quit": cmd_exit,
    "cls": cmd_cls,
    "clear": cmd_cls,
    "echo": cmd_echo,
    "help": cmd_help,
    "cd": cmd_cd,
}