import sublime
import sublime_plugin
import os

class PasteAlgorithmCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sublime.active_window().show_input_panel("Введите название алгоритма", "", self.write_code, None, None)

    def write_code(self, user_input):
        max_similar = -1
        needed_file = ""
        algos_dir = os.path.join(os.path.dirname(__file__), "algos")
        for file in os.listdir(algos_dir):
            current_similar = 0
            for letter in user_input:
                if letter in file:
                    current_similar += 1
            if current_similar / len(file) > max_similar:
                max_similar = current_similar / len(file)
                needed_file = file

        settings = sublime.load_settings("Preferences.sublime-settings")
        settings.set("auto_indent", False)
        settings.set("smart_indent", False)
        sublime.save_settings("Preferences.sublime-settings")
        with open(os.path.join(algos_dir, needed_file)) as file:
            for line in file.readlines():
                self.view.run_command("insert", {"characters": line})
        settings = sublime.load_settings("Preferences.sublime-settings")
        settings.set("auto_indent", True)
        settings.set("smart_indent", True)
        sublime.save_settings("Preferences.sublime-settings")


class OpenCopyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_name = self.view.file_name()
        new_file_name = file_name.replace('.', "_copy.", 1)
        with open(file_name) as file:
            text = file.read()
        with open(new_file_name, 'w') as file:
            file.write(text)
        sublime.active_window().open_file(new_file_name, sublime.ENCODED_POSITION)