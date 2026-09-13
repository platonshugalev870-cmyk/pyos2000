from tqdm import tqdm
import time


class FileCopy:
    def __init__(self, logger, colors, vfs):
        self.logger = logger
        self.colors = colors
        self.vfs = vfs

    def copy_gui(self, state, on_line, on_finish):
        self.vfs.mkdir("/system")
        self.vfs.mkdir("/system/drivers")
        self.vfs.mkdir("/system/apps")
        self.vfs.mkdir("/users")
        self.vfs.mkdir("/temp")
        self.vfs.mkdir("/registry")
        self.vfs.write("/system/pyos.sys", state["version"]["name"])
        self.vfs.write("/system/version.txt", state["version"]["name"] + " build " + state["version"]["build"])

        files = [
            ("/system/kernel.bin", 4096),
            ("/system/shell.bin", 512),
            ("/system/gui.bin", 2048),
        ]
        for d in state["selected_devices"]:
            files.append((f"/system/drivers/{d['driver']}.drv", 128))
        for app in state["version"]["apps"]:
            files.append((f"/system/apps/{app}.app", 256))

        on_line("Extracting files:")
        bar = tqdm(files, desc="Copying", ncols=70, leave=False, ascii=True)
        for path, size in bar:
            bar.set_description(f"Copy {path.split('/')[-1]}")
            self.vfs.write(path, "BLOB:" + str(size))
            on_line(f"  -> {path}  ({size} KB)")
            time.sleep(0.02)
        bar.close()

        on_line("Writing registry...")
        self.vfs.write("/registry/system.dat", "PyOS2000")
        self.vfs.write(
            "/registry/hardware.dat",
            ",".join(d["driver"] for d in state["selected_devices"])
        )
        on_line("  -> /registry/system.dat")
        on_line("  -> /registry/hardware.dat")
        on_line("")
        on_line("Done.")
        on_finish()