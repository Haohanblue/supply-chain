import tkinter as tk
from tkinter import ttk, messagebox
import json

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


# 清除所有输入框数据
def clear_entries(entries):
    for city in entries:
        for good in entries[city]:
            entries[city][good].delete(0, tk.END)


# 更新Treeview上的库存并保存到JSON
def update_stock_in_json(selected_city, selected_month, good, new_value):
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        stock = json.load(f)

    if selected_city in stock and str(selected_month) in stock[selected_city]:
        stock[selected_city][str(selected_month)][good] = int(new_value)

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(stock, f, ensure_ascii=False)


# 显示库存到Treeview表格
def display_stock(tree, selected_month, selected_city):
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        stock = json.load(f)

    # 清空旧的表格内容
    for item in tree.get_children():
        tree.delete(item)

    # 在Treeview中添加新内容
    if selected_city in stock:
        for good, num in stock[selected_city][str(selected_month)].items():
            tree.insert("", tk.END, values=(selected_city, good, num))


# 创建GUI
def create_gui():
    window = tk.Tk()
    window.title("库存管理系统")

    goods = ['品牌茶饮', '品牌果汁', '品牌咖啡', '品牌汽水', '品牌饮用水', '网红茶饮', '网红果汁', '网红咖啡',
             '网红汽水', '网红饮用水', '自营茶饮', '自营咖啡', '自营果汁', '自营汽水', '自营饮用水']
    citys = ['上海', '广州', '武汉', '北京', '济南', '苏州', '常熟', '泰安', '深圳', '珠海']
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    # 设置布局
    main_frame = ttk.Frame(window, padding="50")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # 月份下拉菜单
    ttk.Label(main_frame, text="选择月份:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    selected_month = tk.StringVar()
    month_menu = ttk.Combobox(main_frame, textvariable=selected_month, values=months, state="readonly")
    month_menu.grid(row=0, column=1, padx=5, pady=5)
    month_menu.current(0)

    # 城市下拉菜单
    ttk.Label(main_frame, text="选择城市:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
    selected_city = tk.StringVar()
    city_menu = ttk.Combobox(main_frame, textvariable=selected_city, values=citys, state="readonly")
    city_menu.grid(row=0, column=3, padx=5, pady=5)
    city_menu.current(0)

    # 商品表格标题
    for i, good in enumerate(goods):
        ttk.Label(main_frame, text=good).grid(row=1, column=i + 1, padx=5, pady=5)

    # 创建一个二维表格，行为城市，列为商品
    entries = {}
    for i, city in enumerate(citys):
        ttk.Label(main_frame, text=city).grid(row=i + 2, column=0, padx=5, pady=5)  # 城市名称在第一列
        entries[city] = {}
        for j, good in enumerate(goods):
            entry = ttk.Entry(main_frame, width=5)
            entry.grid(row=i + 2, column=j + 1, padx=5, pady=6)
            entries[city][good] = entry  # 保存每个城市和商品的输入框

    # 创建Treeview用于显示库存数据
    tree_frame = ttk.Frame(main_frame)
    tree_frame.grid(row=len(citys) + 3, column=0, columnspan=20, pady=10)

    columns = ("城市", "商品", "库存")
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="browse", height=8)
    tree.heading("城市", text="城市")
    tree.heading("商品", text="商品")
    tree.heading("库存", text="库存")
    tree.grid(row=0, column=0, padx=5, pady=5)

    # 选择的库存数据的输入框
    ttk.Label(main_frame, text="修改库存值:").grid(row=len(citys) + 4, column=0, padx=5, pady=5, sticky=tk.W)
    entry_edit = ttk.Entry(main_frame)
    entry_edit.grid(row=len(citys) + 4, column=3, padx=5, pady=5)

    # 保存修改按钮
    ttk.Button(main_frame, text="保存修改", command=lambda: save_changes(tree, entry_edit, selected_month)).grid(row=len(citys) + 4, column=4, padx=5, pady=5)

    # 选中Treeview中的数据并显示在Entry中
    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item, 'values')
            entry_edit.delete(0, tk.END)
            entry_edit.insert(0, values[2])  # 填入库存值

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # 保存修改功能
    def save_changes(tree, entry_edit, selected_month):
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item, 'values')
            selected_city_val, good, _ = values
            new_value = entry_edit.get()

            # 更新Treeview
            tree.item(selected_item, values=(selected_city_val, good, new_value))

            # 同步到JSON文件
            update_stock_in_json(selected_city_val, int(selected_month.get()), good, new_value)
            messagebox.showinfo("成功", "库存已更新")

    # 增加库存按钮
    ttk.Button(main_frame, text="增加库存", command=lambda: on_add_stock(entries, selected_month, tree, selected_city)).grid(row=len(citys) + 4, column=0, padx=5, pady=5)

    # 清除所有输入框数据按钮
    ttk.Button(main_frame, text="清除所有数据", command=lambda: clear_entries(entries)).grid(row=len(citys) + 4, column=1, padx=5, pady=5)

    # 显示库存数据按钮
    ttk.Button(main_frame, text="显示库存数据", command=lambda: on_display_stock(tree, selected_month, selected_city)).grid(row=len(citys) + 4, column=2, padx=5, pady=5)
   # 初始化库存按钮
    ttk.Button(main_frame, text="重置库存", command=init).grid(row=len(citys) + 4, column=5, padx=5, pady=5)

    window.mainloop()


# 增加库存逻辑
def on_add_stock(entries, selected_month, tree, selected_city):
    month = int(selected_month.get())
    updated = False
    for city in entries:
        for good in entries[city]:
            try:
                num = int(entries[city][good].get())  # 获取输入的数量
                if num > 0:
                    add_stock(city, month, good, num)  # 调用增加库存函数
                    updated = True
            except ValueError:
                continue  # 忽略空输入或非法输入
    if updated:
        messagebox.showinfo("成功", "库存增加成功")
        # 自动刷新库存显示
        display_stock(tree, month, selected_city.get())


# 显示库存数据按钮逻辑
def on_display_stock(tree, selected_month, selected_city):
    month = int(selected_month.get())
    city = selected_city.get()
    display_stock(tree, month, city)

# 初始化库存字典并启动GUI

create_gui()
