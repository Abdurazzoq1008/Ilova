import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
import json
import os
import webbrowser
import csv
import subprocess
import socket
from datetime import datetime
from PIL import Image

# ================= BREND VA ASOSIY SOZLAMALAR =================
SHOP_NAME = "Melfis Flowers"
SHOP_LOCATION = "Samarqand"
SHOP_PHONE = "+998 90 000 00 00"
INSTAGRAM_URL = "https://www.instagram.com/samarqand.melfisflowers/"
INSTAGRAM_HANDLE = "@samarqand.melfisflowers"

SHOP_CARDS = {
    "Uzcard / Humo": "8600 1234 5678 9012 (Melfis Flowers Samarqand)",
    "Click / Payme": "+998 90 000 00 00"
}

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123"

DATA_FILE = "flowers_data.json"
ORDERS_FILE = "orders_data.json"

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

DEFAULT_FLOWERS = [
    {
        "id": 1,
        "name": "Qizil Premium Atirgullar (Roza)",
        "category": "Atirgullar",
        "price": 28000,
        "stock": 50,
        "desc": "Gollandiyadan keltirilgan premium qizil atirgullar. Sevgi va nafosat ramzi.",
        "icon": "🌹"
    },
    {
        "id": 2,
        "name": "Oq Ecuador Atirgullari",
        "category": "Atirgullar",
        "price": 25000,
        "stock": 35,
        "desc": "Katta kurtakli, beg'ubor oppoq atirgullar kompozitsiyasi.",
        "icon": "🤍"
    },
    {
        "id": 3,
        "name": "Eksklyuziv Pionlar Guldastasi",
        "category": "Guldastalar",
        "price": 220000,
        "stock": 14,
        "desc": "Melfis Flowers maxsus floristlari tomonidan terilgan nozik pushti pionlar.",
        "icon": "💐"
    },
    {
        "id": 4,
        "name": "Golland Lolalari Mix",
        "category": "Lolalar",
        "price": 19000,
        "stock": 65,
        "desc": "Bahoriy xushbo'y va yorqin rangli lola to'plami.",
        "icon": "🌷"
    },
    {
        "id": 5,
        "name": "Qirolicha Orkideyasi (Tuvakda)",
        "category": "Tuvakdagi gullar",
        "price": 195000,
        "stock": 10,
        "desc": "Xonadonga go'zallik va fayz bag'ishlovchi nafis orkideya.",
        "icon": "🪴"
    },
    {
        "id": 6,
        "name": "Gipsofila va Xrizantema Miks",
        "category": "Guldastalar",
        "price": 135000,
        "stock": 18,
        "desc": "Yumshoq bulutsimon gipsofila va rang-barang xrizantemalar uyg'unligi.",
        "icon": "🌸"
    },
    {
        "id": 7,
        "name": "Moviy Gortenziya (Hydrangea)",
        "category": "Guldastalar",
        "price": 160000,
        "stock": 12,
        "desc": "Betakror moviy rangli hashamatli gortenziya guldastasi.",
        "icon": "🪻"
    },
    {
        "id": 8,
        "name": "Melfis Shokoladli Gul Qutisi",
        "category": "Sovg'a qutilari",
        "price": 260000,
        "stock": 8,
        "desc": "Ferrero Rocher shirinliklari va yangi uzilgan atirgullar qutisi.",
        "icon": "🎁"
    }
]

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_FLOWERS)
        return DEFAULT_FLOWERS
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_FLOWERS

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return []
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_orders(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

class MelfisFlowersApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"🌸 {SHOP_NAME} {SHOP_LOCATION} — Boshqaruv Tizimi")
        self.geometry("1200x780")
        self.minsize(1080, 700)

        if os.path.exists("app_icon.ico"):
            try:
                self.iconbitmap("app_icon.ico")
            except Exception:
                pass

        self.flowers = load_data()
        self.orders = load_orders()
        self.cart = {}
        self.is_admin_logged_in = False

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_main_views()
        self.show_view("catalog")

    # ================= SIDEBAR =================
    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#18181B")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(9, weight=1)

        brand_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand_frame.grid(row=0, column=0, padx=20, pady=(24, 12), sticky="w")

        lbl_logo = ctk.CTkLabel(brand_frame, text="🌸", font=ctk.CTkFont(size=34))
        lbl_logo.pack(side="left", padx=(0, 10))

        brand_text_box = ctk.CTkFrame(brand_frame, fg_color="transparent")
        brand_text_box.pack(side="left")

        title_lbl = ctk.CTkLabel(brand_text_box, text=SHOP_NAME, font=ctk.CTkFont(size=20, weight="bold"), text_color="#F43F5E")
        title_lbl.pack(anchor="w")

        sub_lbl = ctk.CTkLabel(brand_text_box, text=f"📍 {SHOP_LOCATION}", font=ctk.CTkFont(size=12), text_color="#A1A1AA")
        sub_lbl.pack(anchor="w")

        # INSTAGRAM BUTTON
        insta_card = ctk.CTkFrame(self.sidebar, fg_color="#831843", corner_radius=10)
        insta_card.grid(row=1, column=0, padx=16, pady=(0, 10), sticky="ew")

        insta_btn = ctk.CTkButton(
            insta_card,
            text=f"📷 Instagram Sahifa\n{INSTAGRAM_HANDLE}",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="transparent",
            hover_color="#9D174D",
            text_color="#FDF2F8",
            height=44,
            corner_radius=8,
            command=self.open_instagram
        )
        insta_btn.pack(fill="both", expand=True, padx=4, pady=4)

        # TELEFONGA ULASH (QR KOD) TUGMASI
        mobile_qr_btn = ctk.CTkButton(
            self.sidebar,
            text="📱 Telefonga Ulash (QR Kod)",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#047857",
            hover_color="#065F46",
            text_color="#ECFDF5",
            height=36,
            corner_radius=8,
            command=self.open_mobile_qr_popup
        )
        mobile_qr_btn.grid(row=2, column=0, padx=16, pady=(0, 12), sticky="ew")

        self.nav_buttons = {}
        nav_items = [
            ("catalog", "💐 Gullar Vitrinasi"),
            ("cart", "🛒 Savatcha & Buyurtma"),
            ("admin", "🔐 Gullar Boshqaruvi"),
            ("history", "📜 Buyurtmalar Tarixi"),
        ]

        for idx, (view_id, label_text) in enumerate(nav_items, start=3):
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"  {label_text}",
                anchor="w",
                font=ctk.CTkFont(size=14, weight="bold"),
                height=42,
                corner_radius=8,
                fg_color="transparent",
                text_color="#E4E4E7",
                hover_color="#27272A",
                command=lambda v=view_id: self.show_view(v)
            )
            btn.grid(row=idx, column=0, padx=16, pady=5, sticky="ew")
            self.nav_buttons[view_id] = btn

        self.admin_status_btn = ctk.CTkButton(
            self.sidebar,
            text="🔒 Admin: Chiqilgan",
            font=ctk.CTkFont(size=11),
            fg_color="#374151",
            hover_color="#4B5563",
            height=30,
            corner_radius=6,
            command=self.handle_admin_auth_button
        )
        self.admin_status_btn.grid(row=8, column=0, padx=16, pady=(15, 0), sticky="ew")

        bottom_frame = ctk.CTkFrame(self.sidebar, fg_color="#27272A", corner_radius=10)
        bottom_frame.grid(row=10, column=0, padx=16, pady=20, sticky="ew")

        ctk.CTkLabel(bottom_frame, text="Tungi rejim:", font=ctk.CTkFont(size=12), text_color="#A1A1AA").pack(side="left", padx=12, pady=10)
        self.theme_switch = ctk.CTkSwitch(bottom_frame, text="", command=self.toggle_theme, width=44)
        self.theme_switch.pack(side="right", padx=12, pady=10)

    def open_instagram(self):
        webbrowser.open_new_tab(INSTAGRAM_URL)

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    # ================= TELEFONGA ULASH POPUP =================
    def open_mobile_qr_popup(self):
        ip = get_local_ip()
        mobile_url = f"http://{ip}:5000"

        # Server fonda ishga tushirish (agar hali ishlamayotgan bo'lsa)
        try:
            test_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_s.settimeout(0.5)
            is_running = test_s.connect_ex((ip, 5000)) == 0
            test_s.close()

            if not is_running:
                py_path = "C:\\Users\\Saidovs\\AppData\\Local\\Programs\\Python\\Python314\\pythonw.exe"
                if not os.path.exists(py_path):
                    py_path = "python"
                subprocess.Popen([py_path, "mobile_app.py"], cwd=os.getcwd())
        except Exception:
            pass

        qr_win = ctk.CTkToplevel(self)
        qr_win.title("📱 Telefon Ilovasiga Ulash — QR Kod")
        qr_win.geometry("440x530")
        qr_win.attributes("-topmost", True)
        qr_win.resizable(False, False)

        # Center in screen
        qr_win.update_idletasks()
        x = (qr_win.winfo_screenwidth() // 2) - 220
        y = (qr_win.winfo_screenheight() // 2) - 265
        qr_win.geometry(f"+{x}+{y}")

        ctk.CTkLabel(qr_win, text="📱 Mobil Ilova Ulanishi", font=ctk.CTkFont(size=18, weight="bold"), text_color="#E11D48").pack(pady=(18, 4))
        ctk.CTkLabel(qr_win, text="Telefoningiz kamerasini QR-kodga qarating:", font=ctk.CTkFont(size=12), text_color="#6B7280").pack(pady=(0, 12))

        # QR kod rasmi
        qr_path = "telefon_uchun_qr.png"
        if os.path.exists(qr_path):
            try:
                pil_img = Image.open(qr_path)
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(220, 220))
                lbl_img = ctk.CTkLabel(qr_win, image=ctk_img, text="")
                lbl_img.pack(pady=5)
            except Exception:
                ctk.CTkLabel(qr_win, text="[QR Kod yuklanmadi]", font=ctk.CTkFont(size=14)).pack(pady=20)

        # Havola ko'rinishi
        link_card = ctk.CTkFrame(qr_win, fg_color="#F3F4F6", corner_radius=10)
        link_card.pack(fill="x", padx=25, pady=10)

        ctk.CTkLabel(link_card, text="Telefon brauzerida manzil:", font=ctk.CTkFont(size=11), text_color="#6B7280").pack(pady=(8, 2))
        url_lbl = ctk.CTkLabel(link_card, text=mobile_url, font=ctk.CTkFont(size=14, weight="bold"), text_color="#059669")
        url_lbl.pack(pady=(0, 8))

        ctk.CTkButton(qr_win, text="Brauzerda ochib ko'rish", height=36, corner_radius=8,
                      command=lambda: webbrowser.open_new_tab(mobile_url)).pack(padx=25, pady=(5, 10), fill="x")

    # ================= VIEW CONTAINER =================
    def setup_main_views(self):
        self.view_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.view_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.view_container.grid_rowconfigure(0, weight=1)
        self.view_container.grid_columnconfigure(0, weight=1)

        self.views = {
            "catalog": self.create_catalog_view(),
            "cart": self.create_cart_view(),
            "admin": self.create_admin_view(),
            "history": self.create_history_view()
        }

    def show_view(self, view_name):
        if view_name == "admin" and not self.is_admin_logged_in:
            self.show_admin_login_dialog()
            if not self.is_admin_logged_in:
                return

        for name, frame in self.views.items():
            if name == view_name:
                frame.grid(row=0, column=0, sticky="nsew")
                self.nav_buttons[name].configure(fg_color="#E11D48", text_color="#FFFFFF")
            else:
                frame.grid_forget()
                self.nav_buttons[name].configure(fg_color="transparent", text_color="#E4E4E7")

        if view_name == "catalog":
            self.render_catalog_cards()
        elif view_name == "cart":
            self.refresh_cart_view()
        elif view_name == "admin":
            self.refresh_admin_table()
        elif view_name == "history":
            self.refresh_history_table()

    # ================= ADMIN LOGIN =================
    def show_admin_login_dialog(self):
        login_win = ctk.CTkToplevel(self)
        login_win.title("Admin Kirish — Melfis Flowers")
        login_win.geometry("380x380")
        login_win.attributes("-topmost", True)
        login_win.resizable(False, False)

        login_win.update_idletasks()
        x = (login_win.winfo_screenwidth() // 2) - 190
        y = (login_win.winfo_screenheight() // 2) - 190
        login_win.geometry(f"+{x}+{y}")

        ctk.CTkLabel(login_win, text="🔐", font=ctk.CTkFont(size=44)).pack(pady=(20, 5))
        ctk.CTkLabel(login_win, text="Admin Boshqaruvi", font=ctk.CTkFont(size=18, weight="bold"), text_color="#E11D48").pack()
        ctk.CTkLabel(login_win, text="Gullarni tahrirlash uchun login va parolni kiriting", font=ctk.CTkFont(size=11), text_color="#6B7280").pack(pady=(2, 15))

        f_inputs = ctk.CTkFrame(login_win, fg_color="transparent")
        f_inputs.pack(fill="x", padx=30)

        ctk.CTkLabel(f_inputs, text="Login:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(2, 2))
        u_entry = ctk.CTkEntry(f_inputs, placeholder_text="admin", height=38, corner_radius=8)
        u_entry.pack(fill="x", pady=(0, 10))
        u_entry.focus()

        ctk.CTkLabel(f_inputs, text="Parol:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(2, 2))
        p_entry = ctk.CTkEntry(f_inputs, placeholder_text="Parol", show="•", height=38, corner_radius=8)
        p_entry.pack(fill="x", pady=(0, 15))

        def attempt_login(event=None):
            username = u_entry.get().strip()
            password = p_entry.get().strip()

            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                self.is_admin_logged_in = True
                self.admin_status_btn.configure(text="🔓 Admin: Kirilgan (Chiqish)", fg_color="#059669", hover_color="#047857")
                login_win.destroy()
                messagebox.showinfo("Muvaffaqiyatli", "Admin panelga xush kelibsiz!")
                self.show_view("admin")
            else:
                messagebox.showerror("Xatolik", "Login yoki parol noto'g'ri!\n(Standart: admin / 123)")

        p_entry.bind("<Return>", attempt_login)
        u_entry.bind("<Return>", attempt_login)

        btn_box = ctk.CTkFrame(login_win, fg_color="transparent")
        btn_box.pack(fill="x", padx=30, pady=10)

        ctk.CTkButton(
            btn_box,
            text="Kirish",
            height=40,
            corner_radius=8,
            fg_color="#E11D48",
            hover_color="#BE123C",
            font=ctk.CTkFont(weight="bold"),
            command=attempt_login
        ).pack(fill="x")

        login_win.grab_set()
        self.wait_window(login_win)

    def handle_admin_auth_button(self):
        if self.is_admin_logged_in:
            if messagebox.askyesno("Chiqish", "Admin tizimidan chiqmoqchimisiz?"):
                self.is_admin_logged_in = False
                self.admin_status_btn.configure(text="🔒 Admin: Chiqilgan", fg_color="#374151", hover_color="#4B5563")
                self.show_view("catalog")
        else:
            self.show_admin_login_dialog()

    # ================= 1. VITRINA / KATALOG =================
    def create_catalog_view(self):
        frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        top_bar = ctk.CTkFrame(frame, corner_radius=12, height=65)
        top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        search_lbl = ctk.CTkLabel(top_bar, text="🔍", font=ctk.CTkFont(size=16))
        search_lbl.pack(side="left", padx=(15, 5), pady=12)

        self.catalog_search_var = ctk.StringVar()
        self.catalog_search_var.trace_add("write", lambda *a: self.render_catalog_cards())
        search_entry = ctk.CTkEntry(
            top_bar,
            placeholder_text="Gul nomi yoki tavsifini qidiring...",
            textvariable=self.catalog_search_var,
            width=280,
            height=36,
            corner_radius=8
        )
        search_entry.pack(side="left", padx=5, pady=12)

        cat_lbl = ctk.CTkLabel(top_bar, text="Kategoriya:", font=ctk.CTkFont(size=13, weight="bold"))
        cat_lbl.pack(side="left", padx=(25, 8), pady=12)

        self.catalog_cat_var = ctk.StringVar(value="Barchasi")
        self.cat_menu = ctk.CTkOptionMenu(
            top_bar,
            values=["Barchasi"],
            variable=self.catalog_cat_var,
            command=lambda v: self.render_catalog_cards(),
            width=160,
            height=36,
            corner_radius=8
        )
        self.cat_menu.pack(side="left", padx=5, pady=12)

        self.cart_quick_badge = ctk.CTkButton(
            top_bar,
            text="🛒 Savatcha (0)",
            command=lambda: self.show_view("cart"),
            height=36,
            corner_radius=8,
            fg_color="#E11D48",
            hover_color="#BE123C",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.cart_quick_badge.pack(side="right", padx=15, pady=12)

        self.cards_scroll = ctk.CTkScrollableFrame(frame, corner_radius=12)
        self.cards_scroll.grid(row=1, column=0, sticky="nsew")

        return frame

    def update_category_options(self):
        cats = sorted(list({f.get("category", "Boshqa") for f in self.flowers}))
        options = ["Barchasi"] + cats
        self.cat_menu.configure(values=options)
        if self.catalog_cat_var.get() not in options:
            self.catalog_cat_var.set("Barchasi")

    def render_catalog_cards(self):
        self.update_category_options()
        query = self.catalog_search_var.get().lower().strip()
        cat = self.catalog_cat_var.get()

        for w in self.cards_scroll.winfo_children():
            w.destroy()

        filtered = [
            f for f in self.flowers
            if ((query in f["name"].lower()) or (query in f.get("desc", "").lower()))
            and (cat == "Barchasi" or f.get("category") == cat)
        ]

        if not filtered:
            empty_lbl = ctk.CTkLabel(
                self.cards_scroll,
                text="Mos keladigan gul topilmadi 🥀",
                font=ctk.CTkFont(size=16),
                text_color="#9CA3AF"
            )
            empty_lbl.pack(pady=60)
            return

        columns = 3
        for i in range(columns):
            self.cards_scroll.grid_columnconfigure(i, weight=1)

        for idx, flower in enumerate(filtered):
            r = idx // columns
            c = idx % columns

            card = ctk.CTkFrame(self.cards_scroll, corner_radius=12, border_width=1, border_color="#E5E7EB")
            card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")

            h_frame = ctk.CTkFrame(card, fg_color="transparent")
            h_frame.pack(fill="x", padx=12, pady=(12, 0))

            icon_lbl = ctk.CTkLabel(h_frame, text=flower.get("icon", "🌸"), font=ctk.CTkFont(size=38))
            icon_lbl.pack(side="left")

            stock_text = f"{flower['stock']} dona" if flower['stock'] > 0 else "Tugagan"
            stock_color = "#DC2626" if flower['stock'] == 0 else ("#D97706" if flower['stock'] < 5 else "#059669")
            stock_badge = ctk.CTkLabel(
                h_frame,
                text=stock_text,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=stock_color
            )
            stock_badge.pack(side="right", anchor="n")

            title_lbl = ctk.CTkLabel(
                card,
                text=flower["name"],
                font=ctk.CTkFont(size=15, weight="bold"),
                anchor="w",
                wraplength=220
            )
            title_lbl.pack(fill="x", padx=14, pady=(8, 2))

            cat_lbl = ctk.CTkLabel(
                card,
                text=f"Turkum: {flower.get('category', 'Boshqa')}",
                font=ctk.CTkFont(size=11),
                text_color="#9CA3AF",
                anchor="w"
            )
            cat_lbl.pack(fill="x", padx=14, pady=(0, 4))

            desc_lbl = ctk.CTkLabel(
                card,
                text=flower.get("desc", ""),
                font=ctk.CTkFont(size=12),
                text_color="#6B7280",
                anchor="w",
                justify="left",
                wraplength=220,
                height=38
            )
            desc_lbl.pack(fill="x", padx=14, pady=(0, 8))

            footer = ctk.CTkFrame(card, fg_color="transparent")
            footer.pack(fill="x", padx=14, pady=(0, 14))

            price_lbl = ctk.CTkLabel(
                footer,
                text=f"{flower['price']:,} so'm".replace(",", " "),
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color="#E11D48"
            )
            price_lbl.pack(side="left")

            add_btn = ctk.CTkButton(
                footer,
                text="+ Qo'shish",
                width=85,
                height=32,
                corner_radius=8,
                fg_color="#E11D48",
                hover_color="#BE123C",
                font=ctk.CTkFont(size=12, weight="bold"),
                state="normal" if flower["stock"] > 0 else "disabled",
                command=lambda f_id=flower["id"]: self.add_to_cart(f_id)
            )
            add_btn.pack(side="right")

        self.update_cart_quick_badge()

    def add_to_cart(self, flower_id):
        flower = next((f for f in self.flowers if f["id"] == flower_id), None)
        if not flower:
            return

        current_qty = self.cart.get(flower_id, 0)
        if current_qty + 1 > flower["stock"]:
            messagebox.showwarning("Ogohlantirish", f"Omborda faqat {flower['stock']} dona '{flower['name']}' mavjud!")
            return

        self.cart[flower_id] = current_qty + 1
        self.update_cart_quick_badge()
        messagebox.showinfo("Melfis Flowers", f"'{flower['name']}' savatchaga qo'shildi!\nSavatchada: {self.cart[flower_id]} dona")

    def update_cart_quick_badge(self):
        total_items = sum(self.cart.values())
        self.cart_quick_badge.configure(text=f"🛒 Savatcha ({total_items})")

    # ================= 2. SAVATCHA VA BUYURTMA =================
    def create_cart_view(self):
        frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=3)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_rowconfigure(0, weight=1)

        left_box = ctk.CTkFrame(frame, corner_radius=12)
        left_box.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_box.grid_rowconfigure(1, weight=1)
        left_box.grid_columnconfigure(0, weight=1)

        header_l = ctk.CTkFrame(left_box, fg_color="transparent")
        header_l.grid(row=0, column=0, sticky="ew", padx=15, pady=12)

        ctk.CTkLabel(header_l, text="Savatchadagi Mahsulotlar", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        clear_btn = ctk.CTkButton(header_l, text="🧹 Tozalash", width=90, height=30, corner_radius=6,
                                  fg_color="#EF4444", hover_color="#DC2626", font=ctk.CTkFont(size=12),
                                  command=self.clear_cart_action)
        clear_btn.pack(side="right")

        self.cart_items_scroll = ctk.CTkScrollableFrame(left_box, corner_radius=8)
        self.cart_items_scroll.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))

        right_box = ctk.CTkFrame(frame, corner_radius=12)
        right_box.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        right_scroll = ctk.CTkScrollableFrame(right_box, fg_color="transparent")
        right_scroll.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(right_scroll, text="Buyurtmani Rasmiylashtirish", font=ctk.CTkFont(size=17, weight="bold"), text_color="#E11D48").pack(anchor="w", padx=15, pady=(10, 10))

        ctk.CTkLabel(right_scroll, text="Mijoz ismi *", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(2, 2))
        self.order_name = ctk.CTkEntry(right_scroll, placeholder_text="Mijoz ismini kiriting", height=34, corner_radius=8)
        self.order_name.pack(fill="x", padx=15, pady=(0, 8))

        ctk.CTkLabel(right_scroll, text="Telefon raqami *", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(2, 2))
        self.order_phone = ctk.CTkEntry(right_scroll, placeholder_text="+998 90 123 45 67", height=34, corner_radius=8)
        self.order_phone.insert(0, "+998 ")
        self.order_phone.pack(fill="x", padx=15, pady=(0, 8))

        ctk.CTkLabel(right_scroll, text="Yetkazish manzili (Samarqand)", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(2, 2))
        self.order_address = ctk.CTkEntry(right_scroll, placeholder_text="Masalan: Registon ko'chasi, 12-uy", height=34, corner_radius=8)
        self.order_address.pack(fill="x", padx=15, pady=(0, 8))

        ctk.CTkLabel(right_scroll, text="Tabriknoma / Izoh (ixtiyoriy)", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(2, 2))
        self.order_note = ctk.CTkEntry(right_scroll, placeholder_text="Tabriknoma so'zlari yoki lenta rangi...", height=34, corner_radius=8)
        self.order_note.pack(fill="x", padx=15, pady=(0, 10))

        # TO'LOV BLOKI
        pay_box = ctk.CTkFrame(right_scroll, corner_radius=10, fg_color="#F3F4F6", border_width=1, border_color="#E5E7EB")
        pay_box.pack(fill="x", padx=15, pady=(0, 10))

        pay_header = ctk.CTkFrame(pay_box, fg_color="transparent")
        pay_header.pack(fill="x", padx=12, pady=(10, 4))
        ctk.CTkLabel(pay_header, text="💳 To'lov Usuli (Faqat Karta)", font=ctk.CTkFont(size=13, weight="bold"), text_color="#1F2937").pack(side="left")
        ctk.CTkLabel(pay_header, text="🚫 Naqd qabul qilinmaydi", font=ctk.CTkFont(size=10, weight="bold"), text_color="#DC2626").pack(side="right")

        self.payment_method_var = ctk.StringVar(value="Uzcard / Humo")
        pay_menu = ctk.CTkSegmentedButton(
            pay_box,
            values=["Uzcard / Humo", "Click", "Payme"],
            variable=self.payment_method_var,
            command=self.update_payment_details
        )
        pay_menu.pack(fill="x", padx=12, pady=(2, 6))

        self.card_info_lbl = ctk.CTkLabel(
            pay_box,
            text=f"Karta raqami: 8600 1234 5678 9012\n(Melfis Flowers Samarqand)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#059669",
            justify="center"
        )
        self.card_info_lbl.pack(pady=(0, 8))

        ctk.CTkLabel(pay_box, text="Mijoz kartasi / Tranzaksiya chek raqami *", font=ctk.CTkFont(size=11, weight="bold"), text_color="#374151").pack(anchor="w", padx=12, pady=(2, 2))
        self.card_tx_entry = ctk.CTkEntry(pay_box, placeholder_text="Mijoz karta oxirgi 4 raqami yoki chek ID", height=32, corner_radius=6)
        self.card_tx_entry.pack(fill="x", padx=12, pady=(0, 10))

        total_card = ctk.CTkFrame(right_scroll, corner_radius=10, fg_color="#FFF1F2")
        total_card.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkLabel(total_card, text="Jami to'lov summasi:", font=ctk.CTkFont(size=12), text_color="#9F1239").pack(pady=(8, 0))
        self.cart_total_lbl = ctk.CTkLabel(total_card, text="0 so'm", font=ctk.CTkFont(size=20, weight="bold"), text_color="#E11D48")
        self.cart_total_lbl.pack(pady=(0, 8))

        self.confirm_order_btn = ctk.CTkButton(
            right_scroll,
            text="💳 Karta To'lovini Tasdiqlash",
            height=42,
            corner_radius=8,
            fg_color="#E11D48",
            hover_color="#BE123C",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.submit_order_action
        )
        self.confirm_order_btn.pack(fill="x", padx=15, pady=(5, 15))

        return frame

    def update_payment_details(self, selected_method):
        if selected_method == "Uzcard / Humo":
            self.card_info_lbl.configure(text="Karta raqami: 8600 1234 5678 9012\n(Melfis Flowers Samarqand)")
        elif selected_method == "Click":
            self.card_info_lbl.configure(text="Click raqam: +998 90 000 00 00\nyoki Click Up: @melfisflowers")
        else:
            self.card_info_lbl.configure(text="Payme raqam: +998 90 000 00 00\n(Melfis Flowers)")

    def refresh_cart_view(self):
        for w in self.cart_items_scroll.winfo_children():
            w.destroy()

        if not self.cart:
            empty = ctk.CTkLabel(self.cart_items_scroll, text="Savatchangiz bo'sh 🛒\nVitrinadan gullar tanlang",
                                 font=ctk.CTkFont(size=15), text_color="#9CA3AF")
            empty.pack(pady=50)
            self.cart_total_lbl.configure(text="0 so'm")
            return

        total_price = 0
        for f_id, qty in list(self.cart.items()):
            flower = next((f for f in self.flowers if f["id"] == f_id), None)
            if not flower:
                continue

            item_sum = flower["price"] * qty
            total_price += item_sum

            row = ctk.CTkFrame(self.cart_items_scroll, corner_radius=8)
            row.pack(fill="x", pady=5, padx=5)

            icon_lbl = ctk.CTkLabel(row, text=flower.get("icon", "🌸"), font=ctk.CTkFont(size=26))
            icon_lbl.pack(side="left", padx=10, pady=8)

            info_box = ctk.CTkFrame(row, fg_color="transparent")
            info_box.pack(side="left", fill="both", expand=True, padx=5)

            ctk.CTkLabel(info_box, text=flower["name"], font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(info_box, text=f"{flower['price']:,} so'm x {qty} dona = {item_sum:,} so'm".replace(",", " "),
                         font=ctk.CTkFont(size=12), text_color="#E11D48", anchor="w").pack(fill="x")

            btn_box = ctk.CTkFrame(row, fg_color="transparent")
            btn_box.pack(side="right", padx=10)

            ctk.CTkButton(btn_box, text="-", width=28, height=28, corner_radius=6, fg_color="#E5E7EB", text_color="#111",
                          hover_color="#D1D5DB", command=lambda id_=f_id: self.change_cart_qty(id_, -1)).pack(side="left", padx=2)

            ctk.CTkLabel(btn_box, text=str(qty), font=ctk.CTkFont(size=13, weight="bold"), width=24).pack(side="left")

            ctk.CTkButton(btn_box, text="+", width=28, height=28, corner_radius=6, fg_color="#E5E7EB", text_color="#111",
                          hover_color="#D1D5DB", command=lambda id_=f_id: self.change_cart_qty(id_, 1)).pack(side="left", padx=2)

            ctk.CTkButton(btn_box, text="✕", width=28, height=28, corner_radius=6, fg_color="#FEE2E2", text_color="#DC2626",
                          hover_color="#FCA5A5", command=lambda id_=f_id: self.remove_cart_item(id_)).pack(side="left", padx=(6, 0))

        self.cart_total_lbl.configure(text=f"{total_price:,} so'm".replace(",", " "))
        self.update_cart_quick_badge()

    def change_cart_qty(self, flower_id, delta):
        flower = next((f for f in self.flowers if f["id"] == flower_id), None)
        if not flower:
            return
        new_qty = self.cart.get(flower_id, 0) + delta
        if new_qty <= 0:
            del self.cart[flower_id]
        elif new_qty > flower["stock"]:
            messagebox.showwarning("Ogohlantirish", f"Omborda ko'pi bilan {flower['stock']} dona mavjud!")
            return
        else:
            self.cart[flower_id] = new_qty
        self.refresh_cart_view()

    def remove_cart_item(self, flower_id):
        if flower_id in self.cart:
            del self.cart[flower_id]
            self.refresh_cart_view()

    def clear_cart_action(self):
        if not self.cart:
            return
        if messagebox.askyesno("Tasdiqlash", "Savatchani butunlay tozalamoqchimisiz?"):
            self.cart.clear()
            self.refresh_cart_view()

    def submit_order_action(self):
        if not self.cart:
            messagebox.showwarning("Bo'sh", "Savatchangiz bo'sh! Iltimos, vitrinadan gul tanlang.")
            return

        name = self.order_name.get().strip()
        phone = self.order_phone.get().strip()
        address = self.order_address.get().strip() or "Do'kondan olib ketish"
        note = self.order_note.get().strip()
        pay_method = self.payment_method_var.get()
        card_tx = self.card_tx_entry.get().strip()

        if not name or len(name) < 2:
            messagebox.showerror("Xatolik", "Iltimos, mijoz ismini kiriting!")
            return

        if not phone or len(phone) < 9:
            messagebox.showerror("Xatolik", "Iltimos, telefon raqamini to'liq kiriting!")
            return

        if not card_tx or len(card_tx) < 2:
            messagebox.showerror("To'lov tekshiruvi", "Iltimos, mijoz karta raqami yoki to'lov cheki/tranzaksiya raqamini kiriting!\n(Faqat karta orqali to'lov qabul qilinadi)")
            return

        order_items = []
        total_amount = 0
        for f_id, qty in self.cart.items():
            f = next((it for it in self.flowers if it["id"] == f_id), None)
            if not f or f["stock"] < qty:
                messagebox.showerror("Xato", f"'{f['name'] if f else 'Gul'}' omborda yetarli emas!")
                return
            cost = f["price"] * qty
            total_amount += cost
            order_items.append({
                "id": f["id"],
                "name": f["name"],
                "price": f["price"],
                "qty": qty,
                "total": cost
            })

        for f_id, qty in self.cart.items():
            f = next((it for it in self.flowers if it["id"] == f_id), None)
            if f:
                f["stock"] -= qty

        new_order = {
            "order_id": len(self.orders) + 1001,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "customer": name,
            "phone": phone,
            "address": address,
            "note": note,
            "items": order_items,
            "total": total_amount,
            "payment_type": f"Karta ({pay_method})",
            "card_tx": card_tx,
            "status": "To'landi (Karta)"
        }

        self.orders.append(new_order)
        save_data(self.flowers)
        save_orders(self.orders)

        self.cart.clear()
        self.order_name.delete(0, "end")
        self.order_address.delete(0, "end")
        self.order_note.delete(0, "end")
        self.card_tx_entry.delete(0, "end")
        self.order_phone.delete(0, "end")
        self.order_phone.insert(0, "+998 ")

        self.refresh_cart_view()
        self.show_receipt_popup(new_order)

    # ================= KVITANSIYA / CHEK =================
    def show_receipt_popup(self, order):
        receipt_win = ctk.CTkToplevel(self)
        receipt_win.title(f"🧾 Kvitansiya - Buyurtma #{order['order_id']}")
        receipt_win.geometry("450x640")
        receipt_win.attributes("-topmost", True)

        scroll = ctk.CTkScrollableFrame(receipt_win, corner_radius=10)
        scroll.pack(fill="both", expand=True, padx=15, pady=15)

        ctk.CTkLabel(scroll, text=f"🌸 {SHOP_NAME} 🌸", font=ctk.CTkFont(size=20, weight="bold"), text_color="#E11D48").pack(pady=(10, 2))
        ctk.CTkLabel(scroll, text=f"Samarqand shahri | {INSTAGRAM_HANDLE}", font=ctk.CTkFont(size=11), text_color="#6B7280").pack(pady=(0, 10))

        sep1 = ctk.CTkFrame(scroll, height=1, fg_color="#D1D5DB")
        sep1.pack(fill="x", pady=5)

        info_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        info_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(info_frame, text=f"Buyurtma №: #{order['order_id']}", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"Sana va vaqt: {order['date']}", font=ctk.CTkFont(size=11), text_color="#6B7280").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"Mijoz: {order['customer']}", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"Telefon: {order['phone']}", font=ctk.CTkFont(size=11)).pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"Manzil: {order['address']}", font=ctk.CTkFont(size=11)).pack(anchor="w")
        
        pay_info = order.get("payment_type", "Karta")
        tx_info = order.get("card_tx", "-")
        ctk.CTkLabel(info_frame, text=f"To'lov turi: 💳 {pay_info}", font=ctk.CTkFont(size=11, weight="bold"), text_color="#059669").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"Chek / Karta: {tx_info}", font=ctk.CTkFont(size=11), text_color="#374151").pack(anchor="w")

        if order.get("note"):
            ctk.CTkLabel(info_frame, text=f"Izoh: {order['note']}", font=ctk.CTkFont(size=11, slant="italic"), text_color="#4B5563").pack(anchor="w")

        sep2 = ctk.CTkFrame(scroll, height=1, fg_color="#D1D5DB")
        sep2.pack(fill="x", pady=8)

        ctk.CTkLabel(scroll, text="BUYURTMA TARKIBI:", font=ctk.CTkFont(size=12, weight="bold"), anchor="w").pack(fill="x", pady=(0, 5))

        for it in order.get("items", []):
            item_row = ctk.CTkFrame(scroll, fg_color="transparent")
            item_row.pack(fill="x", pady=2)
            ctk.CTkLabel(item_row, text=f"{it['name']} x{it['qty']}", font=ctk.CTkFont(size=12), anchor="w").pack(side="left")
            ctk.CTkLabel(item_row, text=f"{it['total']:,} so'm".replace(",", " "), font=ctk.CTkFont(size=12, weight="bold")).pack(side="right")

        sep3 = ctk.CTkFrame(scroll, height=2, fg_color="#E11D48")
        sep3.pack(fill="x", pady=12)

        tot_row = ctk.CTkFrame(scroll, fg_color="transparent")
        tot_row.pack(fill="x")
        ctk.CTkLabel(tot_row, text="JAMI TO'LANGAN (KARTA):", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left")
        ctk.CTkLabel(tot_row, text=f"{order['total']:,} so'm".replace(",", " "), font=ctk.CTkFont(size=16, weight="bold"), text_color="#E11D48").pack(side="right")

        ctk.CTkLabel(scroll, text="\nXaridingiz uchun rahmat!\nGo'zallik va ifor hamrohingiz bo'lsin 🌹", 
                     font=ctk.CTkFont(size=11, slant="italic"), text_color="#6B7280").pack(pady=15)

        btn_box = ctk.CTkFrame(receipt_win, fg_color="transparent")
        btn_box.pack(fill="x", padx=15, pady=(0, 15))

        save_txt_btn = ctk.CTkButton(btn_box, text="💾 Chekni matn (.txt) qilib saqlash", height=36, corner_radius=8,
                                     command=lambda: self.save_receipt_to_file(order))
        save_txt_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        close_btn = ctk.CTkButton(btn_box, text="Yopish", width=80, height=36, corner_radius=8,
                                  fg_color="#6B7280", hover_color="#4B5563", command=receipt_win.destroy)
        close_btn.pack(side="right")

    def save_receipt_to_file(self, order):
        filename = f"chek_buyurtma_{order['order_id']}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"=========================================\n")
            f.write(f"           {SHOP_NAME} - {SHOP_LOCATION}       \n")
            f.write(f"      Instagram: {INSTAGRAM_HANDLE}     \n")
            f.write(f"=========================================\n")
            f.write(f"Buyurtma №: #{order['order_id']}\n")
            f.write(f"Sana va vaqt: {order['date']}\n")
            f.write(f"Mijoz: {order['customer']}\n")
            f.write(f"Telefon: {order['phone']}\n")
            f.write(f"Yetkazish manzili: {order['address']}\n")
            f.write(f"To'lov usuli: {order.get('payment_type', 'Karta')}\n")
            f.write(f"Chek / Tranzaksiya: {order.get('card_tx', '-')}\n")
            if order.get("note"):
                f.write(f"Izoh: {order['note']}\n")
            f.write(f"-----------------------------------------\n")
            f.write(f"MAHSULOTLAR:\n")
            for it in order.get("items", []):
                f.write(f"- {it['name']} x{it['qty']} = {it['total']:,} so'm\n")
            f.write(f"-----------------------------------------\n")
            f.write(f"JAMI TO'LANDI: {order['total']:,} so'm (KARTA ORQALI)\n".replace(",", " "))
            f.write(f"=========================================\n")
            f.write(f"     Xaridingiz uchun tashakkur!\n")

        messagebox.showinfo("Saqlandi", f"Chek muvaffaqiyatli saqlandi: {filename}")

    # ================= 3. ADMIN BOSHQARUV =================
    def create_admin_view(self):
        frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=3)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_rowconfigure(0, weight=1)

        left_box = ctk.CTkFrame(frame, corner_radius=12)
        left_box.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_box.grid_rowconfigure(1, weight=1)
        left_box.grid_columnconfigure(0, weight=1)

        header_top = ctk.CTkFrame(left_box, fg_color="transparent")
        header_top.grid(row=0, column=0, sticky="ew", padx=15, pady=15)

        ctk.CTkLabel(header_top, text=f"🔐 {SHOP_NAME} — Ombordagi Qoldiq", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        logout_btn = ctk.CTkButton(header_top, text="🚪 Chiqish", width=80, height=30, corner_radius=6,
                                   fg_color="#6B7280", hover_color="#4B5563",
                                   command=self.handle_admin_auth_button)
        logout_btn.pack(side="right")

        tree_frame = ctk.CTkFrame(left_box, corner_radius=8)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))

        style = ttk.Style()
        style.configure("Admin.Treeview", rowheight=32, font=("Segoe UI", 10))
        style.configure("Admin.Treeview.Heading", font=("Segoe UI", 10, "bold"))

        cols = ("id", "name", "cat", "price", "stock")
        self.admin_tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse", style="Admin.Treeview")
        self.admin_tree.heading("id", text="ID")
        self.admin_tree.heading("name", text="Gul Nomi")
        self.admin_tree.heading("cat", text="Kategoriya")
        self.admin_tree.heading("price", text="Narxi")
        self.admin_tree.heading("stock", text="Omborda")

        self.admin_tree.column("id", width=40, anchor="center")
        self.admin_tree.column("name", width=160)
        self.admin_tree.column("cat", width=100, anchor="center")
        self.admin_tree.column("price", width=90, anchor="e")
        self.admin_tree.column("stock", width=80, anchor="center")

        scr = ttk.Scrollbar(tree_frame, orient="vertical", command=self.admin_tree.yview)
        self.admin_tree.configure(yscrollcommand=scr.set)
        self.admin_tree.pack(side="left", fill="both", expand=True)
        scr.pack(side="right", fill="y")

        self.admin_tree.bind("<<TreeviewSelect>>", self.on_admin_table_select)

        right_box = ctk.CTkFrame(frame, corner_radius=12)
        right_box.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.admin_form_title = ctk.CTkLabel(right_box, text="Yangi Gul Qo'shish", font=ctk.CTkFont(size=18, weight="bold"), text_color="#E11D48")
        self.admin_form_title.pack(anchor="w", padx=20, pady=(20, 15))

        ctk.CTkLabel(right_box, text="Gul nomi:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(4, 2))
        self.f_name = ctk.CTkEntry(right_box, height=36, corner_radius=8)
        self.f_name.pack(fill="x", padx=20, pady=(0, 6))

        ctk.CTkLabel(right_box, text="Kategoriya:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(4, 2))
        self.f_cat = ctk.CTkEntry(right_box, height=36, corner_radius=8, placeholder_text="Masalan: Atirgullar")
        self.f_cat.pack(fill="x", padx=20, pady=(0, 6))

        ctk.CTkLabel(right_box, text="Dona narxi (so'm):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(4, 2))
        self.f_price = ctk.CTkEntry(right_box, height=36, corner_radius=8)
        self.f_price.pack(fill="x", padx=20, pady=(0, 6))

        ctk.CTkLabel(right_box, text="Ombordagi miqdori (dona):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(4, 2))
        self.f_stock = ctk.CTkEntry(right_box, height=36, corner_radius=8)
        self.f_stock.pack(fill="x", padx=20, pady=(0, 6))

        ctk.CTkLabel(right_box, text="Emoji yoki Belgisi (masalan, 🌹):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(4, 2))
        self.f_icon = ctk.CTkEntry(right_box, height=36, corner_radius=8)
        self.f_icon.insert(0, "🌸")
        self.f_icon.pack(fill="x", padx=20, pady=(0, 6))

        ctk.CTkLabel(right_box, text="Tavsif (nav, xususiyat):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(4, 2))
        self.f_desc = ctk.CTkEntry(right_box, height=36, corner_radius=8)
        self.f_desc.pack(fill="x", padx=20, pady=(0, 15))

        self.btn_save_flower = ctk.CTkButton(right_box, text="💾 Saqlash", height=38, corner_radius=8,
                                             fg_color="#E11D48", hover_color="#BE123C", font=ctk.CTkFont(weight="bold"),
                                             command=self.save_flower_handler)
        self.btn_save_flower.pack(fill="x", padx=20, pady=4)

        self.btn_del_flower = ctk.CTkButton(right_box, text="🗑️ Gulni O'chirish", height=36, corner_radius=8,
                                            fg_color="#EF4444", hover_color="#DC2626",
                                            command=self.delete_flower_handler)
        self.btn_del_flower.pack(fill="x", padx=20, pady=4)

        self.btn_reset_form = ctk.CTkButton(right_box, text="🔄 Yangi gul qo'shish rejimi", height=36, corner_radius=8,
                                            fg_color="#4B5563", hover_color="#374151",
                                            command=self.reset_admin_form)
        self.btn_reset_form.pack(fill="x", padx=20, pady=(4, 20))

        self.editing_id = None
        return frame

    def refresh_admin_table(self):
        for it in self.admin_tree.get_children():
            self.admin_tree.delete(it)

        for f in self.flowers:
            self.admin_tree.insert("", "end", iid=str(f["id"]), values=(
                f["id"],
                f"{f.get('icon', '🌸')} {f['name']}",
                f.get("category", "-"),
                f"{f['price']:,}".replace(",", " "),
                f"{f['stock']} dona"
            ))

    def on_admin_table_select(self, event):
        sel = self.admin_tree.selection()
        if not sel:
            return
        flower_id = int(sel[0])
        flower = next((f for f in self.flowers if f["id"] == flower_id), None)
        if not flower:
            return

        self.editing_id = flower["id"]
        self.admin_form_title.configure(text=f"Tahrirlash: #{flower['id']}")

        self.f_name.delete(0, "end")
        self.f_name.insert(0, flower["name"])

        self.f_cat.delete(0, "end")
        self.f_cat.insert(0, flower.get("category", ""))

        self.f_price.delete(0, "end")
        self.f_price.insert(0, str(flower["price"]))

        self.f_stock.delete(0, "end")
        self.f_stock.insert(0, str(flower["stock"]))

        self.f_icon.delete(0, "end")
        self.f_icon.insert(0, flower.get("icon", "🌸"))

        self.f_desc.delete(0, "end")
        self.f_desc.insert(0, flower.get("desc", ""))

    def reset_admin_form(self):
        self.editing_id = None
        self.admin_form_title.configure(text="Yangi Gul Qo'shish")
        self.f_name.delete(0, "end")
        self.f_cat.delete(0, "end")
        self.f_price.delete(0, "end")
        self.f_stock.delete(0, "end")
        self.f_icon.delete(0, "end")
        self.f_icon.insert(0, "🌸")
        self.f_desc.delete(0, "end")
        self.admin_tree.selection_remove(self.admin_tree.selection())

    def save_flower_handler(self):
        if not self.is_admin_logged_in:
            messagebox.showerror("Ruxsat yo'q", "Amalni bajarish uchun admin bo'lib kiring!")
            return

        name = self.f_name.get().strip()
        cat = self.f_cat.get().strip() or "Boshqa"
        price_str = self.f_price.get().strip()
        stock_str = self.f_stock.get().strip()
        icon = self.f_icon.get().strip() or "🌸"
        desc = self.f_desc.get().strip()

        if not name:
            messagebox.showerror("Xato", "Gul nomini kiriting!")
            return

        try:
            price = int(price_str)
            stock = int(stock_str)
            if price < 0 or stock < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Xato", "Narx va miqdorga musbat raqam kiriting!")
            return

        if self.editing_id:
            flower = next((f for f in self.flowers if f["id"] == self.editing_id), None)
            if flower:
                flower["name"] = name
                flower["category"] = cat
                flower["price"] = price
                flower["stock"] = stock
                flower["icon"] = icon
                flower["desc"] = desc
                messagebox.showinfo("Saqlandi", "Gul ma'lumotlari yangilandi!")
        else:
            new_id = max([f["id"] for f in self.flowers], default=0) + 1
            self.flowers.append({
                "id": new_id,
                "name": name,
                "category": cat,
                "price": price,
                "stock": stock,
                "icon": icon,
                "desc": desc
            })
            messagebox.showinfo("Muvaffaqiyatli", "Yangi gul qo'shildi!")

        save_data(self.flowers)
        self.refresh_admin_table()
        self.reset_admin_form()

    def delete_flower_handler(self):
        if not self.is_admin_logged_in:
            messagebox.showerror("Ruxsat yo'q", "Amalni bajarish uchun admin bo'lib kiring!")
            return

        if not self.editing_id:
            messagebox.showinfo("Eslatma", "O'chirish uchun avval ro'yxatdan gulni tanlang!")
            return

        if messagebox.askyesno("Tasdiqlash", "Haqiqatan ham bu gulni o'chirmoqchimisiz?"):
            self.flowers = [f for f in self.flowers if f["id"] != self.editing_id]
            if self.editing_id in self.cart:
                del self.cart[self.editing_id]
            save_data(self.flowers)
            self.refresh_admin_table()
            self.reset_admin_form()
            messagebox.showinfo("O'chirildi", "Gul muvaffaqiyatli o'chirildi!")

    # ================= 4. BUYURTMALAR TARIXI =================
    def create_history_view(self):
        frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        top_banner = ctk.CTkFrame(frame, corner_radius=12, height=70)
        top_banner.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        self.stat_orders_lbl = ctk.CTkLabel(top_banner, text="Jami Buyurtmalar: 0 ta", font=ctk.CTkFont(size=14, weight="bold"))
        self.stat_orders_lbl.pack(side="left", padx=20, pady=15)

        self.stat_revenue_lbl = ctk.CTkLabel(top_banner, text="Umumiy Tushum: 0 so'm", font=ctk.CTkFont(size=14, weight="bold"), text_color="#E11D48")
        self.stat_revenue_lbl.pack(side="left", padx=15, pady=15)

        btn_container = ctk.CTkFrame(top_banner, fg_color="transparent")
        btn_container.pack(side="right", padx=15, pady=15)

        excel_btn = ctk.CTkButton(btn_container, text="📊 Excel (CSV) yuklab olish", width=160, height=36, corner_radius=8,
                                  fg_color="#059669", hover_color="#047857", font=ctk.CTkFont(size=12, weight="bold"),
                                  command=self.export_orders_to_excel)
        excel_btn.pack(side="left", padx=(0, 8))

        refresh_btn = ctk.CTkButton(btn_container, text="🔄 Yangilash", width=90, height=36, corner_radius=8,
                                    fg_color="#E11D48", hover_color="#BE123C", command=self.refresh_history_table)
        refresh_btn.pack(side="left")

        table_card = ctk.CTkFrame(frame, corner_radius=12)
        table_card.grid(row=1, column=0, sticky="nsew")

        cols = ("id", "date", "customer", "phone", "total", "pay", "status")
        self.history_tree = ttk.Treeview(table_card, columns=cols, show="headings", selectmode="browse", style="Admin.Treeview")
        self.history_tree.heading("id", text="Buyurtma №")
        self.history_tree.heading("date", text="Sana")
        self.history_tree.heading("customer", text="Mijoz")
        self.history_tree.heading("phone", text="Telefon")
        self.history_tree.heading("total", text="Summa")
        self.history_tree.heading("pay", text="To'lov Usuli (Karta)")
        self.history_tree.heading("status", text="Holat")

        self.history_tree.column("id", width=85, anchor="center")
        self.history_tree.column("date", width=120, anchor="center")
        self.history_tree.column("customer", width=140)
        self.history_tree.column("phone", width=120, anchor="center")
        self.history_tree.column("total", width=110, anchor="e")
        self.history_tree.column("pay", width=170, anchor="center")
        self.history_tree.column("status", width=120, anchor="center")

        scr = ttk.Scrollbar(table_card, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scr.set)
        self.history_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scr.pack(side="right", fill="y", padx=(0, 10), pady=10)

        self.history_tree.bind("<Double-1>", self.on_history_double_click)

        return frame

    def on_history_double_click(self, event):
        sel = self.history_tree.selection()
        if not sel:
            return
        item_vals = self.history_tree.item(sel[0], "values")
        if not item_vals:
            return
        order_id_str = str(item_vals[0]).replace("#", "").strip()
        try:
            ord_id = int(order_id_str)
            order = next((o for o in self.orders if o["order_id"] == ord_id), None)
            if order:
                self.show_receipt_popup(order)
        except Exception:
            pass

    def export_orders_to_excel(self):
        if not self.orders:
            messagebox.showinfo("Ma'lumot yo'q", "Eksport qilish uchun buyurtmalar mavjud emas!")
            return

        filename = f"melfis_flowers_hisobot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(["Buyurtma №", "Sana va Vaqt", "Mijoz Ismi", "Telefon", "Manzil", "Izoh", "Jami Summa (so'm)", "To'lov Turi", "Karta/Chek ID", "Mahsulotlar Tarkibi", "Holati"])
                for o in self.orders:
                    items_str = ", ".join([f"{it['name']} ({it['qty']} dona)" for it in o.get("items", [])])
                    writer.writerow([
                        f"#{o.get('order_id')}",
                        o.get("date"),
                        o.get("customer"),
                        o.get("phone"),
                        o.get("address"),
                        o.get("note", ""),
                        o.get("total", 0),
                        o.get("payment_type", "Karta"),
                        o.get("card_tx", "-"),
                        items_str,
                        o.get("status", "Bajarildi")
                    ])

            messagebox.showinfo("Eksport qilindi", f"Hisobot Excel (CSV) formatida saqlandi:\n📁 {filename}")
        except Exception as e:
            messagebox.showerror("Xatolik", f"Faylni saqlashda xatolik yuz berdi: {str(e)}")

    def refresh_history_table(self):
        for it in self.history_tree.get_children():
            self.history_tree.delete(it)

        total_rev = 0
        for ord in reversed(self.orders):
            total_rev += ord.get("total", 0)
            pay_str = f"{ord.get('payment_type', 'Karta')}"
            self.history_tree.insert("", "end", values=(
                f"#{ord.get('order_id')}",
                ord.get("date"),
                ord.get("customer"),
                ord.get("phone"),
                f"{ord.get('total', 0):,}".replace(",", " "),
                pay_str,
                ord.get("status", "Bajarildi")
            ))

        self.stat_orders_lbl.configure(text=f"Jami Buyurtmalar: {len(self.orders)} ta")
        self.stat_revenue_lbl.configure(text=f"Umumiy Tushum: {total_rev:,} so'm".replace(",", " "))

if __name__ == "__main__":
    app = MelfisFlowersApp()
    app.mainloop()
