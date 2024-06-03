def get_anomaly_from_csv(date, appliance):
    print('近來得', date, type(date))
    # 打开对应设备的 txt 文件
    with open(f'./predict_list/power/p_BME.txt', 'r') as file:
        # 逐行读取文件内容
        for line in file:
            # 将每行按照空格分割，并取出日期和值
            parts = line.strip().split(' ')
            row_date = parts[0]
            value = parts[1]
            # print(row_date)
            # print(value)
            # print('---------')
            
            
            # 如果找到了对应日期的数值，则返回该数值
            if row_date + ' ' + value == date:
                return parts[2]
                
    
    # 如果未找到对应日期的数值，则返回 None
    return None

time = '2013-06-03 17:00:00'
ifAnomaly = get_anomaly_from_csv(time, 'BME')
print(ifAnomaly)



# # 读取 CDE.txt 中的数据
# with open(f'./predict_list/power/p_CDE.txt', 'r') as infile:
#     cde_data = infile.readlines()

# # 将数据转换为与 BME.txt 相同格式
# cde_data_formatted = []
# for line in cde_data:
#     # 分割每行数据，获取日期和数值
#     parts = line.strip().split('\t')
#     date = parts[0]
#     value = parts[1]
#     # 格式化为日期在前、数值在后的格式，并添加到新的列表中
#     cde_data_formatted.append(f"{date} {value}\n")

# # 将转换后的数据写入新文件 CDE_formatted.txt
# with open('./predict_list/power/CDE_formatted.txt', 'w') as outfile:
#     outfile.writelines(cde_data_formatted)
