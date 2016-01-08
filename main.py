#encoding=utf8
from __future__  import absolute_import

import json
import os,sys
import subprocess
from wox import Wox

current_dir = os.path.dirname(__file__)
plugin_home = os.path.dirname(current_dir)
wox_home = os.path.dirname(plugin_home)

os.environ['WOX_HOME'] = wox_home

class PathAlias(Wox):
	IMAGE_PATH = 'img/folder.png'
	ACTION_KEYWORD = 'pa'
	SEPERATER = ' '

	def make_command_usage(self, results, cmd, title, subtitle):
		query = '%s%s%s%s' %(self.ACTION_KEYWORD, 
				self.SEPERATER, cmd, self.SEPERATER
				)
		m = {
				'Title': title,
				'SubTitle': subtitle,
				'IcoPath':self.IMAGE_PATH,
				"JsonRPCAction":{
				  "method": "Wox.ChangeQuery",
				  "parameters":[query, False],
				  "dontHideAfterAction":True
				}
		}

		results.append(m)

	def usage_results(self):
	    results = []
	    self.make_command_usage(results, 'open', 'open <path alias name>', 'open folder quickey')
	    self.make_command_usage(results, 'editconfig', 'editconfig', 'open user config file')
	    return results

    	def load_config(self):
		self.alias_map = {}
		self.open_folder_cmd = 'explorer %s'
		self.data_path = ''

		with open(os.path.join(current_dir,"config.json"), "r") as content_file:
			config = json.loads(content_file.read())
			v = config.get('data_path', self.data_path)
			if v: self.data_path = v
			v = config.get('open_folder_cmd', self.open_folder_cmd)
			if v: self.open_folder_cmd  = v

	def expandpath(self, m):
		new_m = {}
		for key, v in m.iteritems():
			t = os.path.expandvars(v)
			new_m[key] = t	
		return new_m

	def load_data(self):
		path = os.path.join(current_dir, "data.json")

		if os.path.lexists(path):
			with open(path, "r") as content_file:
				m = json.loads(content_file.read())
				m = self.expandpath(m)
				self.alias_map.update(m)

		if self.data_path and os.path.lexists(self.data_path):
			with open(self.data_path, "r") as content_file:
				m = json.loads(content_file.read())
				m = self.expandpath(m)
				self.alias_map.update(m)
		
	def open_command(self, key_list):
		query = None
		if len(key_list) > 1:
			query = key_list[1]

		results = []
		for key, path in self.alias_map.iteritems():

			if query  and query not in key:
				continue

			m = {
				'Title': key,
				'SubTitle': 'open folder %s' % path,
				'IcoPath':self.IMAGE_PATH,
				"JsonRPCAction":{
				  "method": "open_folder",
				  "parameters":[path,],
				}
			}
			results.append(m)

		return results

	def editconfig_command(self, key_list):
		results = []

		if not self.data_path or not os.path.isfile(self.data_path):
			m = 	{
					'Title': "没有定义用户配置文件",
					"JsonRPCAction":{
					  "method": "Wox.ShowApp",
					  "parameters":[],
					  "dontHideAfterAction":True
					}
				}
			results.append(m)
			return results

		path = self.data_path
		m = 	{
				'Title': "打开用户配置文件",
				'SubTitle': '用户配置文件: %s' % path,
				"JsonRPCAction":{
				  "method": "open_userconfig",
				  #"parameters":[path.replace("\\", "\\\\"),],
				  "parameters":[path,],
				}
			}
		results.append(m)
		return results


	def query(self, key):
		if not key:
			return self.usage_results()

		key_list = key.strip().split(' ')
		if len(key_list) < 1: return self.usage_results()

		cmd = key_list[0]

		self.load_config()

		if cmd == 'open':
			self.load_data()
			return self.open_command(key_list)
		elif cmd == 'editconfig':
			return self.editconfig_command(key_list)
		
		return [] 

	def open_userconfig(self, path):
		self.load_config()
		
		p = path.replace("/", "\\")
		p = p.replace("\\\\", "\\")

		cmd = "%s" % p
		#self.debug(cmd)
		subprocess.call(cmd, shell=True)


	def open_folder(self, path):
		self.load_config()

		p = path.replace("/", "\\")
		p = p.replace("\\\\", "\\")

		cmd = self.open_folder_cmd % p
		#self.debug(cmd)
		subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    PathAlias()
