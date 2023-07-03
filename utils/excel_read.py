# import xlrd
#
#
# class ExcelRead():
#     def __init__(self, file):
#         self.file = file
#
#     def _open_excel(self):
#         try:
#             data = xlrd.open_workbook(self.file)
#         except Exception as e:
#             raise e
#         else:
#             return data
#
#     def read_excel(self):
#         data = self._open_excel()
#         table = data.sheets()[0]
#         n_rows = table.nrows  # 总行数
#         list_data = [table.row_values(row_num) for row_num in range(0, n_rows)]
#         # 返回数据格式
#         dict_data = {row[0]: row[1] for row in list_data}
#
#         if len(list_data) == len(dict_data):
#             return dict_data
#         else:
#             return {}
