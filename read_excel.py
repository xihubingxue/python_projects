import xlrd


def read_excel():

    workbook=xlrd.open_workbook("work_plan.xlsx")
    print("The sheet name is {}".format(workbook.sheet_names()))
    sheet1= workbook.sheet_by_name("Mon")
    nrows = sheet1.nrows
    ncols = sheet1.ncols
    print("We have {} rows and {} columns".format(nrows, ncols))
    plan_list = []
    temp_value = ""
    for i in range(nrows):
        plan_dict = {}
        for j in range(4):
            if i >= 3:
              value=sheet1.cell_value(i,j)
              if j==0 and value != "":
                  temp_value = value
              value = value if value else temp_value
              plan_dict.update({sheet1.cell(2,j).value:value})
        #delete the blank row
        plan_temp = []
        for val in plan_dict.values():
            plan_temp.append(val)
        if set(plan_temp).__len__() != plan_temp.__len__():
            continue
        if plan_dict:
         plan_list.append(plan_dict)
    for plan in plan_list:
        print(plan)
    return plan_list


if __name__ == "__main__":
    read_excel()