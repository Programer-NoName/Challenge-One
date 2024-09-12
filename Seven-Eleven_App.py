# import library part

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # ใช้สำหรับแสดงข้อความแจ้งเตือน
from tkinter import font  # ใช้สำหรับจัดการฟอนต์
import requests
from PIL import Image, ImageTk
from io import BytesIO


# def part
# ฟังก์ชันสร้างตาราง
def create_product_table(app):
    # สร้างตาราง
    table = ttk.Treeview(app, columns=('สินค้า', 'ราคาชิ้นละ', 'โปรโมชันซื้อ 2 อัน'), show='headings', height=6)

    # กำหนดหัวตาราง
    table.heading('สินค้า', text='สินค้า', anchor='center')
    table.heading('ราคาชิ้นละ', text='ราคาชิ้นละ (บาท)', anchor='center')
    table.heading('โปรโมชันซื้อ 2 อัน', text='โปรโมชันซื้อ 2 อัน', anchor='center')

    # กำหนดความกว้างคอลัมน์
    table.column('สินค้า', width=150, anchor='center', stretch=False)
    table.column('ราคาชิ้นละ', width=150, anchor='center', stretch=False)
    table.column('โปรโมชันซื้อ 2 อัน', width=150, anchor='center', stretch=False)

    # เพิ่มข้อมูลสินค้า
    products = [
        ('สินค้า A', 20, 'ลด 20 บาท'),
        ('สินค้า B', 30, 'ลด 10 บาท'),
        ('สินค้า C', 10, 'ไม่ลดราคา'),
        ('สินค้า D', 15, 'ลด 15 บาท'),
        ('สินค้า E', 5, 'ลด 2.50 บาท'),
        ('ถ้าซื้อครบ 200 บาท','(หลังหักส่วนลดข้างบนแล้ว)','ลดเพิ่มอีก 20 บาท')
    ]

    # แสดงข้อมูลลงในตาราง
    for product in products:
        table.insert('', tk.END, values=product)

    # วางตารางบนหน้าต่างหลัก
    table.pack()

# ฟังก์ชันสำหรับเก็บค่าจำนวนสินค้า
def keed_values():
    try:
        # ดึงค่าจากช่องกรอกข้อความ และแปลงเป็น int
        product_A = int(entry_A.get())
        product_B = int(entry_B.get())
        product_C = int(entry_C.get())
        product_D = int(entry_D.get())
        product_E = int(entry_E.get())

        # คืนค่าลิสต์ของจำนวนสินค้า
        return [product_A, product_B, product_C, product_D, product_E]
    except ValueError:
        return "error"
# ฟังก์ชันสำหรับแสดงผลลัพธ์
def show_total_price(total_price):
    if total_price < 200:
        total_price_label.config(text=f"ราคารวมทั้งหมด: {total_price} บาท")
    elif total_price >=200:
        total_price_promotion = total_price // 200 
        if total_price_promotion <=1 :
            total_price_sub=20
            total_price=total_price-total_price_sub
        elif total_price_promotion > 1:
            total_price_sub=(20*total_price_promotion)
            total_price=total_price-total_price_sub
        total_price_label.config(text=f"ราคารวมทั้งหมด: {total_price} บาท (ส่วนลด {total_price_sub} บาท)")
        

# calculate
def calculate_Floor_division():
    # part name variable
    quantity_from_keed_values = keed_values()
    if quantity_from_keed_values == "error":
        messagebox.showerror("ข้อผิดพลาด", "กรุณาใส่จำนวนสินค้าให้ถูกต้อง")
        return

    quantity_product_A = quantity_from_keed_values[0]
    quantity_product_B = quantity_from_keed_values[1]
    quantity_product_C = quantity_from_keed_values[2]
    quantity_product_D = quantity_from_keed_values[3]
    quantity_product_E = quantity_from_keed_values[4]
    
    # part price
    price_A, price_B, price_C, price_D, price_E = ["20", "30", "10", "15", "5"]
    promotion_price_A, promotion_price_B, promotion_price_C, promotion_price_D, promotion_price_E = ["20", "10", "0", "15", "2.50"]

    # part calculate_Floor_division //2
    Floor_division_product_A = (quantity_product_A // 2) if quantity_product_A >= 2 else 0
    Floor_division_product_B = (quantity_product_B // 2) if quantity_product_B >= 2 else 0
    Floor_division_product_C = (quantity_product_C // 2) if quantity_product_C >= 2 else 0
    Floor_division_product_D = (quantity_product_D // 2) if quantity_product_D >= 2 else 0
    Floor_division_product_E = (quantity_product_E // 2) if quantity_product_E >= 2 else 0

    # part calculate quantity_product no promotion
    calculate_quantity_product_A = (quantity_product_A * int(price_A))
    calculate_quantity_product_B = (quantity_product_B * int(price_B))
    calculate_quantity_product_C = (quantity_product_C * int(price_C))
    calculate_quantity_product_D = (quantity_product_D * int(price_D))
    calculate_quantity_product_E = (quantity_product_E * int(price_E))

    # part calculate quantity_product with promotion
    promotion_quantity_product_A = (Floor_division_product_A * int(promotion_price_A)) if Floor_division_product_A > 0 else 0
    promotion_quantity_product_B = (Floor_division_product_B * int(promotion_price_B)) if Floor_division_product_B > 0 else 0
    promotion_quantity_product_C = (Floor_division_product_C * int(promotion_price_C)) if Floor_division_product_C > 0 else 0
    promotion_quantity_product_D = (Floor_division_product_D * int(promotion_price_D)) if Floor_division_product_D > 0 else 0
    promotion_quantity_product_E = (Floor_division_product_E * float(promotion_price_E)) if Floor_division_product_E > 0 else 0

    # part calculate price to pay (no promotion - promotion)
    price_to_pay_A = (calculate_quantity_product_A - promotion_quantity_product_A)
    price_to_pay_B = (calculate_quantity_product_B - promotion_quantity_product_B)
    price_to_pay_C = (calculate_quantity_product_C - promotion_quantity_product_C)
    price_to_pay_D = (calculate_quantity_product_D - promotion_quantity_product_D)
    price_to_pay_E = (calculate_quantity_product_E - promotion_quantity_product_E)

    # part sum all product
    total_price_all_product = price_to_pay_A + price_to_pay_B + price_to_pay_C + price_to_pay_D + price_to_pay_E

    # แสดงผลลัพธ์
    show_total_price(total_price_all_product)

# ฟังก์ชันช่วยสำหรับสร้างแถวของป้ายและช่องกรอกข้อมูล
def create_labeled_entry(main_variable, label_text):
    frame = tk.Frame(main_variable)
    frame.pack(pady=5)  # เว้นระยะห่างในแนวดิ่ง

    label = tk.Label(frame, text=label_text, font=new_setup_font)
    label.pack(side=tk.LEFT, padx=5)  # วางป้ายทางซ้าย

    entry = tk.Entry(frame, width=20)
    entry.pack(side=tk.LEFT)  # วางช่องกรอกข้อมูลทางขวา

    unit_label = tk.Label(frame, text="ชิ้น", font=new_setup_font)
    unit_label.pack(side=tk.LEFT, padx=5)  # วางป้าย "ชิ้น" ทางขวาของช่องกรอกข้อมูล

    return entry

# setuup app part
# สร้างหน้าต่างหลัก
app = tk.Tk()
app.configure(bg="#E8F0FE")
app.title("โปรแกรมขายของใน 7-11")
app.geometry('700x600')
photo = ImageTk.PhotoImage(Image.open(BytesIO(requests.get('https://seeklogo.com/images/1/7-Eleven-logo-08AAB4F0FE-seeklogo.com.png').content)))
app.iconphoto(False, photo)

# สร้างฟอนต์ที่มีขนาดใหญ่ขึ้น 10 หน่วย
default_font = font.nametofont("TkDefaultFont")  # ดึงฟอนต์เริ่มต้นมา
setup_font_size = default_font.cget("size") + 5  # เพิ่มขนาดขึ้น 10 หน่วย
new_setup_font = default_font.copy()
new_setup_font.configure(size=setup_font_size)

# เรียกใช้ฟังก์ชันสร้างตาราง
create_product_table(app)

# สร้างป้ายและกล่องข้อความสำหรับการใส่จำนวนสินค้า
entry_A = create_labeled_entry(app, "ใส่จำนวนสินค้า A:")
entry_B = create_labeled_entry(app, "ใส่จำนวนสินค้า B:")
entry_C = create_labeled_entry(app, "ใส่จำนวนสินค้า C:")
entry_D = create_labeled_entry(app, "ใส่จำนวนสินค้า D:")
entry_E = create_labeled_entry(app, "ใส่จำนวนสินค้า E:")

# ป้ายสำหรับแสดงราคารวม
total_price_label = tk.Label(app, text="ราคารวมทั้งหมด: 0 บาท", font=new_setup_font)
total_price_label.pack(pady=10)

# ปุ่มสำหรับยืนยันจำนวนสินค้า
calculate_button = tk.Button(app, text="คำนวณ", command=calculate_Floor_division)
calculate_button.config(width=20, height=3, padx=3, font=setup_font_size)
calculate_button.pack()

# เริ่มต้นโปรแกรม
app.mainloop()
