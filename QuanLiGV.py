import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class GiaoVien:
    def __init__(self, ID, ten):
        self.ID = ID
        self.ten = ten

    def to_dict(self):
        return {"ID": self.ID, "ten": self.ten}

class QuanLyGiaoVien:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản Lý Giáo Viên")
        self.root.geometry("600x400")

        self.ten_file = "c:/Users/hongo/OneDrive/Máy tính/SNLT/SLTW/GV.json"
        self.GV = self.doc_file_json()

        # Combobox ở giữa cửa sổ
        self.combobox = ttk.Combobox(self.root, width=40)
        self.combobox.place(x=150, y=20)
        self.combobox.bind("<<ComboboxSelected>>", self.hien_thi_thong_tin)

        self.tao_giao_dien()
        self.cap_nhat_combobox()

    def tao_giao_dien(self):
        # Bên trái: Nhập và nút
        left_frame = tk.Frame(self.root)
        left_frame.pack(side="left", padx=20, pady=20)

        tk.Label(left_frame, text="ID giáo viên:").pack(pady=5)
        self.id_entry = tk.Entry(left_frame)
        self.id_entry.pack()

        tk.Label(left_frame, text="Tên giáo viên:").pack(pady=5)
        self.ten_entry = tk.Entry(left_frame)
        self.ten_entry.pack()

        tk.Button(left_frame, text="Thêm giáo viên", command=self.them_giao_vien).pack(pady=5)
        tk.Button(left_frame, text="Xóa giáo viên", command=self.xoa_giao_vien).pack(pady=5)

        # Bên phải: Hiển thị thông tin
        right_frame = tk.Frame(self.root)
        right_frame.pack(side="right", padx=20, pady=20)

        self.info_label = tk.Label(right_frame, text="Thông tin giáo viên sẽ hiển thị tại đây", justify="left")
        self.info_label.pack()

    def them_giao_vien(self):
        ID = self.id_entry.get().strip()
        ten = self.ten_entry.get().strip()

        if not ID or not ten:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ ID và tên giáo viên.")
            return

        if self.kiem_tra_trung_ID(ID):
            messagebox.showerror("Trùng ID", f"ID '{ID}' đã tồn tại.")
            return

        gv = GiaoVien(ID, ten)
        self.GV.append(gv)
        self.luu_file_json()
        self.cap_nhat_combobox()

        self.id_entry.delete(0, tk.END)
        self.ten_entry.delete(0, tk.END)

    def xoa_giao_vien(self):
        selected = self.combobox.get()
        if not selected:
            messagebox.showwarning("Chưa chọn giáo viên", "Vui lòng chọn giáo viên để xóa.")
            return

        ID = selected.split(" | ")[0].split(": ")[1]
        self.GV = [gv for gv in self.GV if gv.ID != ID]
        self.luu_file_json()
        self.cap_nhat_combobox()
        self.info_label.config(text="Thông tin giáo viên sẽ hiển thị tại đây")

    def kiem_tra_trung_ID(self, ID):
        return any(gv.ID == ID for gv in self.GV)

    def cap_nhat_combobox(self):
        self.combobox.set('')
        self.combobox['values'] = [f"ID: {gv.ID} | Tên: {gv.ten}" for gv in self.GV]

    def hien_thi_thong_tin(self, event=None):
        selected = self.combobox.get()
        if selected:
            ID = selected.split(" | ")[0].split(": ")[1]
            gv = next((gv for gv in self.GV if gv.ID == ID), None)
            if gv:
                info = f"ID: {gv.ID}\nTên: {gv.ten}"
                self.info_label.config(text=info)

    def luu_file_json(self):
        data = [gv.to_dict() for gv in self.GV]
        with open(self.ten_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def doc_file_json(self):
        if os.path.exists(self.ten_file):
            try:
                with open(self.ten_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [GiaoVien(item["ID"], item["ten"]) for item in data]
            except json.JSONDecodeError:
                messagebox.showerror("Lỗi", "File JSON bị lỗi hoặc trống.")
                return []
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = QuanLyGiaoVien(root)
    root.mainloop()
