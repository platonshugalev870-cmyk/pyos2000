import sys
import time
import tkinter as tk


def typewriter(text, delay=0.02, end="\n"):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()


def typewriter_lines(lines, delay=0.02, line_delay=0.05, color=None):
    for line in lines:
        if color:
            print(color, end="")
        for ch in line:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(delay)
        if color:
            sys.stdout.write("\033[0m")
        sys.stdout.write("\n")
        sys.stdout.flush()
        time.sleep(line_delay)


def progress_dots(prefix, count=3, delay=0.25):
    sys.stdout.write(prefix)
    for _ in range(count):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()


def gui_type_text(widget, text, delay=25, callback=None):
    state = {"i": 0, "after": None}

    def step():
        if state["i"] >= len(text):
            if callback:
                callback()
            return
        if isinstance(widget, tk.Text):
            widget.insert("end", text[state["i"]])
            widget.see("end")
        else:
            widget.config(text=widget.cget("text") + text[state["i"]])
        state["i"] += 1
        state["after"] = widget.after(delay, step)

    step()
    return state


def gui_type_lines(text_widget, lines, delay=0, line_delay=120, callback=None, index=0):
    if index >= len(lines):
        if callback:
            callback()
        return
    text_widget.insert("end", lines[index] + "\n")
    text_widget.see("end")
    text_widget.after(line_delay, lambda: gui_type_lines(text_widget, lines, delay, line_delay, callback, index + 1))


def gui_type_rich(text_widget, segments, delay=12, callback=None):
    state = {"seg_i": 0, "ch_i": 0, "after": None}

    def step():
        if state["seg_i"] >= len(segments):
            if callback:
                callback()
            return
        seg = segments[state["seg_i"]]
        text = seg.get("text", "")
        tags = seg.get("tags", ())
        delay_ms = seg.get("delay", delay)
        if state["ch_i"] >= len(text):
            state["seg_i"] += 1
            state["ch_i"] = 0
            state["after"] = text_widget.after(delay_ms, step)
            return
        text_widget.insert("end", text[state["ch_i"]], tags)
        text_widget.see("end")
        state["ch_i"] += 1
        state["after"] = text_widget.after(delay_ms, step)

    step()
    return state


def fade_in_window(window, steps=12, delay=30):
    try:
        window.attributes("-alpha", 0.0)
    except tk.TclError:
        return

    def step(i):
        if i > steps:
            return
        try:
            window.attributes("-alpha", i / steps)
        except tk.TclError:
            return
        window.after(delay, lambda: step(i + 1))

    step(0)


def slide_in_window(window, target_x, target_y, steps=14, delay=15):
    try:
        window.geometry(f"+{target_x - 40}+{target_y}")
    except tk.TclError:
        return

    def step(i):
        if i > steps:
            try:
                window.geometry(f"+{target_x}+{target_y}")
            except tk.TclError:
                pass
            return
        x = target_x - 40 + int(40 * i / steps)
        try:
            window.geometry(f"+{x}+{target_y}")
        except tk.TclError:
            return
        window.after(delay, lambda: step(i + 1))

    step(0)


def fade_widget(widget, steps=10, delay=25, callback=None):
    widget.update_idletasks()
    bg = widget.cget("bg")
    fg = widget.cget("fg") if "fg" in widget.keys() else "#000000"

    def blend(c1, c2, r):
        c1 = c1.lstrip("#")
        c2 = c2.lstrip("#")
        try:
            r1 = tuple(int(c1[i:i + 2], 16) for i in (0, 2, 4))
            r2 = tuple(int(c2[i:i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            return widget.cget("bg")
        mix = tuple(int(r1[i] + (r2[i] - r1[i]) * r) for i in range(3))
        return "#{:02x}{:02x}{:02x}".format(*mix)

    def step(i):
        if i > steps:
            if callback:
                callback()
            return
        r = i / steps
        try:
            widget.config(bg=blend("#ffffff", bg, r))
        except tk.TclError:
            return
        widget.after(delay, lambda: step(i + 1))

    step(0)


def slide_widget_in(widget, target_x, target_y, steps=14, delay=15):
    try:
        widget.place(x=target_x - 60, y=target_y)
    except tk.TclError:
        return

    def step(i):
        if i > steps:
            try:
                widget.place(x=target_x, y=target_y)
            except tk.TclError:
                pass
            return
        x = target_x - 60 + int(60 * i / steps)
        try:
            widget.place(x=x, y=target_y)
        except tk.TclError:
            return
        widget.after(delay, lambda: step(i + 1))

    step(0)


def slide_row_in(text_widget, line, tag, row_delay=80, x_offset=15):
    text_widget.insert("end", line + "\n", tag)
    text_widget.see("end")


def pulse_text(text_widget, tag, color_a="#000000", color_b="#ff0000", steps=6, delay=80):
    def step(i):
        if i > steps:
            try:
                text_widget.tag_configure(tag, foreground=color_a)
            except tk.TclError:
                pass
            return
        try:
            text_widget.tag_configure(tag, foreground=color_b if i % 2 == 0 else color_a)
        except tk.TclError:
            return
        text_widget.after(delay, lambda: step(i + 1))

    step(0)


def pulse_widget(widget, color_a, color_b, steps=6, delay=60):
    def step(i):
        if i > steps:
            try:
                widget.config(bg=color_a)
            except tk.TclError:
                pass
            return
        try:
            widget.config(bg=color_b if i % 2 == 0 else color_a)
        except tk.TclError:
            return
        widget.after(delay, lambda: step(i + 1))

    step(0)


def animate_progress(text_widget, tag, duration_ms=1200, steps=30, char="━"):
    state = {"i": 0}

    def step():
        if state["i"] >= steps:
            return
        text_widget.insert("end", char, tag)
        text_widget.see("end")
        state["i"] += 1
        text_widget.after(duration_ms // steps, step)

    step()


def blink_tag(text_widget, tag, color1, color2, times=4, delay=200):
    def step(i):
        if i >= times * 2:
            try:
                text_widget.tag_configure(tag, foreground=color1)
            except tk.TclError:
                pass
            return
        try:
            text_widget.tag_configure(tag, foreground=color2 if i % 2 == 0 else color1)
        except tk.TclError:
            return
        text_widget.after(delay, lambda: step(i + 1))

    step(0)


def wave_labels(labels, base_color, wave_color, delay=60, per_step=60):
    n = len(labels)

    def step(k):
        for i, lbl in enumerate(labels):
            try:
                if i == k % n:
                    lbl.config(bg=wave_color)
                else:
                    lbl.config(bg=base_color)
            except tk.TclError:
                pass
        if k < n * 2:
            labels[0].after(per_step, lambda: step(k + 1))
        else:
            for lbl in labels:
                try:
                    lbl.config(bg=base_color)
                except tk.TclError:
                    pass

    step(0)