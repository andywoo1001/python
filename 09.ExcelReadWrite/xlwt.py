#!/usr/bin/python 
# -*- coding: utf-8 -*- 

import xlwt 
import datetime

book = xlwt.Workbook(encoding="utf-8") 

sheet1 = book.add_sheet("MySheet 1") 
sheet2 = book.add_sheet("MySheet 2") 
sheet3 = book.add_sheet("MySheet 3") 

sheet1.write(0, 0, "Sheet1, 0, 0") 
sheet2.write(0, 0, "Sheet2, 0, 0") 
sheet3.write(0, 0, "Sheet3, 0, 0") 
sheet2.write(1, 5, "Sheet2, 1, 5") 
sheet3.write(0, 2, "Sheet3, 0, 2") 
sheet3.write(1, 2, "Sheet3, 1, 2") 
sheet3.write(2, 2, "Sheet3, 2, 2") 
sheet3.write(3, 2, "Sheet3, 3, 2") 

book.save("Results.xls")