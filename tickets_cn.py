# coding: utf-8
"""Train tickets query via command-line.
Usage:
	tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
	tickets beijing shanghai 2016-08-25
"""
import requests
from docopt import docopt
from stations import stations
from prettytable import PrettyTable
class TrainCollection(object):
	# 显示车次、出发/到达站、 出发/到达时间、历时、商务座、特等座、一等坐、二等坐、软卧、硬卧、硬座 无座
	header = '车次 出发/到站 出发/到达时间 历时 商务座 特等座 一等座 二等座 软卧 硬卧 硬座 无座'.split()
	def __init__(self,rows):
		self.rows = rows
	def _get_duration(self,row):
		"""
		获取车次运行时间
		"""
		duration = row.get('lishi').replace(':','h') + 'm'
		if duration.startswith('00'):
			return duration[3:]
		if duration.startswith('0'):
			return duration[1:]
		return duration
	@property
	def trains(self):
		for row in self.rows:
			train = [
				# 车次
                row['station_train_code'],
                # 出发、到达站
                '\n'.join([row['from_station_name'], row['to_station_name']]),
                # 出发、到达时间
                '\n'.join([row['start_time'], row['arrive_time']]),
                # 历时
                self._get_duration(row),
				#商务座
				row['swz_num'],
				#特等座
				row['tz_num'],
                # 一等坐
                row['zy_num'],
                # 二等坐
                row['ze_num'],
                # 软卧
                row['rw_num'],
                # 软坐
                row['yw_num'],
                # 硬坐
                row['yz_num'],
				#无座
				row['wz_num']
			]
			yield train
	def pretty_print(self):
		pt = PrettyTable()
		pt._set_field_names(self.header)
		for train in self.trains:
			pt.add_row(train)
		print(pt)

def cli():
	"""command-line interface"""
	arguments = docopt(__doc__)
	from_station = stations.get(arguments['<from>'])
	to_station = stations.get(arguments['<to>'])
	date = arguments['<date>']
	#构建url
	url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(
        date, from_station, to_station
    )
	r = requests.get(url,verify=False)
	row = r.json()['data']['datas']
	trains = TrainCollection(row)
	trains.pretty_print()
if __name__ == '__main__':
	cli()	
