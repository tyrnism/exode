
from typing import List
import mysql.connector, os
import traceback

mysql_connector = None

class lib_mysql:
	def __init__(self, db_user: str, db_version: str, db_password: str) -> None:
		self.mysql_connector = None
		self.cursor = None
		self.db_user = db_user
		self.db_version = db_version
		self.db_password = db_password

	def mysql_connect(self):
		try:
			self.mysql_connector = mysql.connector.connect(user=self.db_user, password=self.db_password, host='127.0.0.1', database=self.db_version)
			self.cursor          = self.mysql_connector.cursor()	
		except:
			err = traceback.format_exc()
			print(f"error: {err}")
			print(f"ERROR: MySQL connection failed")
		
	def get_cursor(self):
		if self.mysql_connector == None:
			self.mysql_connect()
		try:
			self.cursor = self.mysql_connector.cursor()
		except mysql.connector.Error as err:
			self.mysql_connect()
			self.cursor = self.mysql_connector.cursor()
				
		return self.cursor

	def close_cursor(self):
		try:
			if self.cursor == None:
				return
			self.cursor.close()
			self.mysql_connector.disconnect()
			self.cursor = None
			print("Closing cursor")
		except:
			err = traceback.format_exc()
			self.cursor = None
			print(f"error: {err}")
			print("Cursor close failed")

	def select(self, query_str: str, value_tuple: tuple, mysql_continue: bool = False, multi: bool = False) -> list:
		
		output = None
		try:
		#if True:
			if not mysql_continue or self.cursor == None:
				self.get_cursor()
			if multi:
				output = []
					
				if value_tuple == None:
					results = self.cursor.execute( query_str, multi=True )
				else:
					results = self.cursor.execute( query_str, value_tuple, multi=True )
				
				for result in results:
					if result.with_rows:
						output.extend(result.fetchall())
			else:
				self.cursor.execute( query_str, value_tuple )
				output = self.cursor.fetchall()

			self.cursor.reset()
			if not mysql_continue:
				self.close_cursor()
		
		except mysql.connector.Error:
			err = traceback.format_exc()
			self.close_cursor()
			print(f"connector error: {err}")
			print(f"Query failed. query={query_str}")
			raise Exception("connector error")
		except:
			err = traceback.format_exc()
			print(f"error: {err}")
			print(f"Query failed. query={query_str}")
			raise Exception("MySQL error")
		return output

	def commit(self, query_str: str, value_tuple: tuple, mysql_continue: bool = False, multi: bool = False):
		
		last_row, n_rows = self.commits(query_str=query_str, value_tuple=value_tuple, mysql_continue=mysql_continue, multi=multi)
		return last_row

	def commits(self, query_str: str, value_tuple: tuple, mysql_continue: bool = False, multi: bool = False):
		
		try:
		#if True:
			if not mysql_continue or self.cursor == None:
				self.get_cursor()

			if multi:
				if value_tuple == None:

					for result in self.cursor.execute( query_str, multi=True ):
						last_row = result.lastrowid
						n_rows = result.rowcount
						
				else:
					for result in self.cursor.execute( query_str, value_tuple, multi=True ):
						last_row = result.lastrowid
						n_rows = result.rowcount

			else:
				if value_tuple == None:
					self.cursor.execute( query_str )
				else:
					self.cursor.execute( query_str, value_tuple )
				self.mysql_connector.commit()


			last_row = self.cursor.lastrowid
			n_rows = self.cursor.rowcount

			self.cursor.reset()
			if not mysql_continue:
				self.close_cursor()

			return last_row, n_rows

		except mysql.connector.Error:
			err = traceback.format_exc()
			self.close_cursor()
			print(f"connector error: {err}")
			print(f"Query failed. query={query_str}")
			raise Exception("connector error")
		except:
			err = traceback.format_exc()
			print(f"error: {err}")
			print(f"Query failed. query={query_str}")
			raise Exception("MySQL error")

	def commit_many(self, query_str: str, value_tuple: List[tuple], mysql_continue: bool = False):
		
		try:
		#if True:
			if not mysql_continue or self.cursor == None:
				self.get_cursor()
			if value_tuple == None:
				self.cursor.executemany( query_str )
			else:
				self.cursor.executemany( query_str, value_tuple )
			self.mysql_connector.commit()

			last_row = self.cursor.lastrowid
			n_rows = self.cursor.rowcount

			self.cursor.reset()
			if not mysql_continue:
				self.close_cursor()
				
			return last_row, n_rows

		except mysql.connector.Error:
			err = traceback.format_exc()
			self.close_cursor()
			print(f"connector error: {err}")
			print(f"Query failed. query={query_str}")
			raise Exception("connector error")
		except:
			err = traceback.format_exc()
			print(f"error: {err}")
			print(f"Query failed. query={query_str}")
			raise Exception("MySQL error")

