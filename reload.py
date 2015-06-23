import sublime, sublime_plugin
import os

files = []

class ReloadEvents(sublime_plugin.EventListener):

	def on_load(self, view):
		global files

		path = view.file_name()
		if path is None:
			return

		stats = self.fileStats(path)
		files.append(stats)

	def on_activated(self, view):
		global files

		path = view.file_name()
		if path is None:
			return

		comp = self.fileStats(path)

		found = False
		for stats in files[:]:
			if stats['file'] != comp['file']:
				continue

			found = True
			if stats['mtime'] == comp['mtime']:
				break

			files.remove(stats)
			found = False

			if self.ask():
				view.run_command("revert")
			break

		if not found:
			files.append(comp)

	def on_close(self, view):
		path = view.file_name()
		if path is None:
			return

		self.remove(path)

	def on_post_save(self, view):
		path = view.file_name()
		if path is None:
			return

		self.replace(path)

	def replace(self, path):
		global files

		if path is None:
			return

		self.remove(path)

		comp = self.fileStats(path)
		files.append(comp)

	def remove(self, path):
		global files

		if path is None:
			return

		for stats in files[:]:
			if stats['file'] == path:
				files.remove(stats)
				break

	def fileStats(self, path):
		return {
			"file":path,
			"mtime":os.path.getmtime(path)
		}

	def ask(self):
		return sublime.ok_cancel_dialog(
			"This file appears to have been modified since you last opened it. Would you like to reload it?",
			"Reload?"
		)
