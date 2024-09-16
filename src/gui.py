import tkinter as tk
from tkinter import ttk, messagebox
import openpyxl
import json
import os

FILE_PATH = "./stock.json"


# 初始化库存字典
def init():
    citys = ['上海', '广州', '武汉', '北京', '济南', '苏州', '常熟', '泰安', '深圳', '珠海']
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    goods = ['品牌茶饮', '品牌果汁', '品牌咖啡', '品牌汽水', '品牌饮用水', '网红茶饮', '网红果汁', '网红咖啡',
             '网红汽水', '网红饮用水', '自营茶饮', '自营咖啡', '自营果汁', '自营汽水', '自营饮用水']
    stock = {}

    for city in citys:
        stock[city] = {}
        for month in months:
            stock[city][month] = {}
            for good in goods:
                stock[city][month][good] = 0

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(stock, f, ensure_ascii=False)


# 增加库存
def add_stock(city, month, good, num):
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        stock = json.load(f)

    if city in stock and str(month) in stock[city] and good in stock[city][str(month)]:
        stock[city][str(month)][good] += num
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(stock, f, ensure_ascii=False)
        messagebox.showinfo("成功", "库存增加成功")
    else:
        messagebox.showerror("错误", "输入的城市、月份或商品不正确")


# 保存库存到Excel
def save_to_excel():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        stock = json.load(f)

    if not os.path.exists('./stock'):
        os.makedirs('./stock')

    for city in stock:
        wb = openpyxl.Workbook()
        wb.remove(wb.active)

        for month in stock[city]:
            ws = wb.create_sheet(str(month))
            ws.append(['商品', '库存'])

            for good in stock[city][month]:
                ws.append([good, stock[city][month][good]])

        wb.save(f'./stock/{city}.xlsx')

    messagebox.showinfo("成功", "库存已保存到Excel文件")


# 创建GUI
def create_gui():
    window = tk.Tk()
    window.title("库存管理系统")

    goods = ['品牌茶饮', '品牌果汁', '品牌咖啡', '品牌汽水', '品牌饮用水', '网红茶饮', '网红果汁', '网红咖啡',
             '网红汽水', '网红饮用水', '自营茶饮', '自营咖啡', '自营果汁', '自营汽水', '自营饮用水']
    citys = ['上海', '广州', '武汉', '北京', '济南', '苏州', '常熟', '泰安', '深圳', '珠海']
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    # 月份下拉菜单
    selected_month = tk.StringVar(window)
    selected_month.set(months[0])  # 默认选择1月
    tk.Label(window, text="选择月份:").grid(row=0, column=0)
    month_menu = tk.OptionMenu(window, selected_month, *months)
    month_menu.grid(row=0, column=1)

    # 商品表格标题
    for i, good in enumerate(goods):
        tk.Label(window, text=good).grid(row=1, column=i + 1)

    # 创建一个二维表格，行为城市，列为商品
    entries = {}
    for i, city in enumerate(citys):
        tk.Label(window, text=city).grid(row=i + 2, column=0)  # 城市名称在第一列
        entries[city] = {}
        for j, good in enumerate(goods):
            entry = tk.Entry(window, width=5)
            entry.grid(row=i + 2, column=j + 1)
            entries[city][good] = entry  # 保存每个城市和商品的输入框

    # 增加库存按钮
    def on_add_stock():
        month = int(selected_month.get())
        for city in entries:
            for good in entries[city]:
                try:
                    num = int(entries[city][good].get())  # 获取输入的数量
                    if num > 0:
                        add_stock(city, month, good, num)  # 调用增加库存函数
                except ValueError:
                    continue  # 忽略空输入或非法输入

    tk.Button(window, text="增加库存", command=on_add_stock).grid(row=len(citys) + 3, column=0,
                                                                  columnspan=len(goods) + 1)

    # 保存到Excel按钮
    tk.Button(window, text="保存到Excel", command=save_to_excel).grid(row=len(citys) + 4, column=0,
                                                                      columnspan=len(goods) + 1)

    window.mainloop()


# 初始化库存字典并启动GUI
init()
create_gui()
