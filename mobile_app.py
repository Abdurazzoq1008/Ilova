from flask import Flask, render_template_string, request, jsonify, redirect, url_for, session
import json
import os
import socket
from datetime import datetime

app = Flask(__name__)
app.secret_key = "melfis_flowers_secret_key_samarqand"

SHOP_NAME = "Melfis Flowers"
SHOP_LOCATION = "Samarqand"
INSTAGRAM_URL = "https://www.instagram.com/samarqand.melfisflowers/"
INSTAGRAM_HANDLE = "@samarqand.melfisflowers"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "flowers_data.json")
ORDERS_FILE = os.path.join(BASE_DIR, "orders_data.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

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

MOBILE_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Melfis Flowers Samarqand</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: #FDF2F4;
      color: #1F2937;
      padding-bottom: 90px;
    }
    header {
      background: #FFFFFF;
      position: sticky;
      top: 0;
      z-index: 50;
      padding: 12px 16px;
      border-bottom: 1px solid #FCE7F3;
      box-shadow: 0 2px 10px rgba(225, 29, 72, 0.05);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .brand-title {
      font-weight: 800;
      font-size: 19px;
      color: #E11D48;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .insta-pill {
      background: #FFF1F2;
      border: 1px solid #FECDD3;
      color: #BE123C;
      font-size: 11px;
      font-weight: 700;
      padding: 6px 10px;
      border-radius: 20px;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .search-section {
      padding: 12px 16px;
      background: #FFFFFF;
      border-bottom: 1px solid #F3F4F6;
    }
    .search-input {
      width: 100%;
      padding: 12px 16px;
      border-radius: 12px;
      border: 1px solid #E5E7EB;
      background: #F9FAFB;
      font-size: 14px;
      outline: none;
    }
    .search-input:focus { border-color: #E11D48; background: #fff; }

    .category-pills {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding: 10px 16px;
      white-space: nowrap;
      scrollbar-width: none;
    }
    .category-pills::-webkit-scrollbar { display: none; }
    .cat-pill {
      padding: 7px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      background: #FFFFFF;
      border: 1px solid #F3E8EC;
      color: #4B5563;
      cursor: pointer;
    }
    .cat-pill.active {
      background: #E11D48;
      color: #FFFFFF;
      border-color: #E11D48;
    }

    /* Flowers Grid */
    .catalog-grid {
      padding: 12px;
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
    }
    .flower-card {
      background: #FFFFFF;
      border-radius: 16px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 4px 15px rgba(0,0,0,0.03);
      border: 1px solid #F3E8EC;
      position: relative;
    }
    .card-icon {
      font-size: 42px;
      text-align: center;
      margin: 8px 0;
    }
    .card-stock {
      position: absolute;
      top: 10px;
      right: 10px;
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 6px;
      background: #ECFDF5;
      color: #059669;
    }
    .card-stock.low { background: #FEF3C7; color: #D97706; }
    .card-stock.out { background: #FEE2E2; color: #DC2626; }
    .card-title {
      font-weight: 700;
      font-size: 14px;
      color: #111827;
      line-height: 1.25;
      margin-bottom: 4px;
    }
    .card-desc {
      font-size: 11px;
      color: #6B7280;
      margin-bottom: 8px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .card-footer {
      margin-top: auto;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .card-price {
      font-size: 14px;
      font-weight: 800;
      color: #E11D48;
    }
    .btn-add {
      background: #E11D48;
      color: #FFFFFF;
      border: none;
      border-radius: 10px;
      padding: 9px;
      font-weight: 700;
      font-size: 12px;
      cursor: pointer;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
    }
    .btn-add:disabled { background: #E5E7EB; color: #9CA3AF; }

    /* Navigation Bottom Bar */
    .bottom-nav {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: #FFFFFF;
      border-top: 1px solid #F3F4F6;
      box-shadow: 0 -4px 15px rgba(0,0,0,0.05);
      display: flex;
      justify-content: space-around;
      padding: 10px 0;
      z-index: 60;
    }
    .nav-btn {
      display: flex;
      flex-direction: column;
      align-items: center;
      background: none;
      border: none;
      color: #6B7280;
      font-size: 11px;
      font-weight: 600;
      gap: 4px;
      cursor: pointer;
      position: relative;
    }
    .nav-btn.active { color: #E11D48; }
    .badge-count {
      position: absolute;
      top: -3px;
      right: 18px;
      background: #E11D48;
      color: #FFFFFF;
      font-size: 10px;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 10px;
    }

    /* Views */
    .view-content { display: none; }
    .view-content.active { display: block; }

    /* Form Styles */
    .section-card {
      background: #FFFFFF;
      border-radius: 16px;
      padding: 16px;
      margin: 12px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.03);
      border: 1px solid #F3E8EC;
    }
    .section-title {
      font-size: 16px;
      font-weight: 800;
      color: #111827;
      margin-bottom: 12px;
    }
    .input-group { margin-bottom: 12px; }
    .input-label {
      font-size: 12px;
      font-weight: 700;
      color: #374151;
      margin-bottom: 4px;
      display: block;
    }
    .app-input {
      width: 100%;
      padding: 12px 14px;
      border-radius: 10px;
      border: 1px solid #E5E7EB;
      font-size: 14px;
      outline: none;
    }
    .app-input:focus { border-color: #E11D48; }

    .payment-badge {
      background: #FFF1F2;
      border: 1px solid #FECDD3;
      color: #BE123C;
      padding: 12px;
      border-radius: 12px;
      margin-bottom: 12px;
      font-size: 13px;
    }
    .payment-badge strong { color: #9F1239; font-size: 14px; }

    .btn-submit {
      width: 100%;
      background: #E11D48;
      color: #FFFFFF;
      border: none;
      border-radius: 12px;
      padding: 14px;
      font-size: 15px;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }

    /* Cart Item */
    .cart-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 0;
      border-bottom: 1px solid #F3F4F6;
    }
    .qty-controls {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .btn-qty {
      width: 28px;
      height: 28px;
      border-radius: 8px;
      border: 1px solid #E5E7EB;
      background: #F9FAFB;
      font-weight: 700;
      cursor: pointer;
    }
    .modal-backdrop {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0,0,0,0.6);
      z-index: 100;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .modal-box {
      background: #FFFFFF;
      width: 100%;
      max-width: 360px;
      border-radius: 20px;
      padding: 20px;
      max-height: 85vh;
      overflow-y: auto;
    }
  </style>
</head>
<body>

  <!-- Top App Header -->
  <header>
    <div class="brand-title">
      <span>🌸</span> Melfis Flowers
    </div>
    <a href="https://www.instagram.com/samarqand.melfisflowers/" target="_blank" class="insta-pill">
      📷 Instagram
    </a>
  </header>

  <!-- 1. VITRINA KO'RINISHI -->
  <div id="view-catalog" class="view-content active">
    <div class="search-section">
      <input type="text" id="searchInput" class="search-input" placeholder="🔍 Gul nomi bo'yicha qidirish..." oninput="renderCatalog()">
    </div>

    <div class="category-pills" id="categoryPills">
      <!-- Toifalar JS da chiqadi -->
    </div>

    <div class="catalog-grid" id="flowersGrid">
      <!-- Gullar JS orqali chiqariladi -->
    </div>
  </div>

  <!-- 2. SAVATCHA VA TO'LOV -->
  <div id="view-cart" class="view-content">
    <div class="section-card">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <span class="section-title" style="margin-bottom:0;">🛒 Savatcha</span>
        <button onclick="clearCart()" style="background:none; border:none; color:#DC2626; font-size:12px; font-weight:700; cursor:pointer;">🧹 Tozalash</button>
      </div>
      <div id="cartItemsList">
        <!-- Savatcha elementlari -->
      </div>
      <div style="display:flex; justify-content:space-between; margin-top:14px; font-weight:800; font-size:16px;">
        <span>Jami summa:</span>
        <span id="cartTotalPrice" style="color:#E11D48;">0 so'm</span>
      </div>
    </div>

    <!-- Buyurtma va Karta To'lovi -->
    <div class="section-card">
      <div class="section-title">💳 Buyurtma & Karta To'lovi</div>

      <div class="payment-badge">
        <strong>⚠️ Faqat Karta Orqali To'lov!</strong><br>
        Naqd to'lov qabul qilinmaydi.<br><br>
        💳 Karta: <strong>8600 1234 5678 9012</strong><br>
        (Melfis Flowers Samarqand)
      </div>

      <div class="input-group">
        <label class="input-label">Mijoz Ismi *</label>
        <input type="text" id="orderCustName" class="app-input" placeholder="Ism familiyangiz">
      </div>

      <div class="input-group">
        <label class="input-label">Telefon Raqami *</label>
        <input type="tel" id="orderCustPhone" class="app-input" value="+998 ">
      </div>

      <div class="input-group">
        <label class="input-label">Yetkazish Manzili (Samarqand)</label>
        <input type="text" id="orderCustAddress" class="app-input" placeholder="Ko'cha, xonadon yoki mo'ljal">
      </div>

      <div class="input-group">
        <label class="input-label">Tabriknoma / Izoh (ixtiyoriy)</label>
        <input type="text" id="orderCustNote" class="app-input" placeholder="Tabriknoma matni...">
      </div>

      <div class="input-group">
        <label class="input-label">To'lov Usuli (Karta turi)</label>
        <select id="orderPayMethod" class="app-input" style="background:#fff;">
          <option value="Uzcard / Humo">Uzcard / Humo</option>
          <option value="Click">Click</option>
          <option value="Payme">Payme</option>
        </select>
      </div>

      <div class="input-group">
        <label class="input-label">Karta oxirgi 4 raqami / Chek tranzaksiya ID *</label>
        <input type="text" id="orderCardTx" class="app-input" placeholder="Masalan: 4589 yoki Chek №">
      </div>

      <button class="btn-submit" onclick="submitOrder()">
        ✅ Buyurtmani Qabul Qilish
      </button>
    </div>
  </div>

  <!-- 3. ADMIN PANEL -->
  <div id="view-admin" class="view-content">
    <div class="section-card" id="adminLoginCard">
      <div class="section-title">🔐 Admin Tizimiga Kirish</div>
      <p style="font-size:12px; color:#6B7280; margin-bottom:12px;">Gullarni tahrirlash uchun login va parolni kiriting</p>
      
      <div class="input-group">
        <label class="input-label">Admin Login</label>
        <input type="text" id="adminUser" class="app-input" placeholder="admin">
      </div>
      <div class="input-group">
        <label class="input-label">Admin Parol</label>
        <input type="password" id="adminPass" class="app-input" placeholder="123">
      </div>
      <button class="btn-submit" onclick="checkAdminLogin()">Kirish</button>
    </div>

    <div class="section-card" id="adminDashboardCard" style="display:none;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <span class="section-title" style="margin-bottom:0;">⚙️ Gullar Boshqaruvi</span>
        <button onclick="adminLogout()" style="background:#F3F4F6; border:none; padding:6px 10px; border-radius:8px; font-size:11px; font-weight:700;">🚪 Chiqish</button>
      </div>

      <!-- Yangi Gul Qo'shish Formasi -->
      <div style="background:#F9FAFB; padding:12px; border-radius:12px; margin-bottom:15px; border:1px solid #E5E7EB;">
        <div style="font-weight:700; font-size:13px; margin-bottom:8px; color:#E11D48;" id="flowerFormTitle">Yangi Gul Qo'shish</div>
        <input type="hidden" id="editFlowerId" value="">
        <input type="text" id="flowerName" class="app-input" placeholder="Gul nomi" style="margin-bottom:6px;">
        <input type="text" id="flowerCategory" class="app-input" placeholder="Kategoriya (masalan: Atirgullar)" style="margin-bottom:6px;">
        <input type="number" id="flowerPrice" class="app-input" placeholder="Dona narxi (so'm)" style="margin-bottom:6px;">
        <input type="number" id="flowerStock" class="app-input" placeholder="Ombordagi soni" style="margin-bottom:6px;">
        <input type="text" id="flowerIcon" class="app-input" placeholder="Emoji (masalan: 🌹)" value="🌸" style="margin-bottom:6px;">
        <input type="text" id="flowerDesc" class="app-input" placeholder="Tavsif" style="margin-bottom:10px;">
        
        <button class="btn-submit" onclick="saveFlower()">💾 Saqlash</button>
      </div>

      <!-- Ombordagi gullar ro'yxati -->
      <div style="font-weight:700; font-size:13px; margin-bottom:8px;">Ombordagi Gullar:</div>
      <div id="adminFlowersList"></div>
    </div>
  </div>

  <!-- 4. BUYURTMALAR TARIXI -->
  <div id="view-history" class="view-content">
    <div class="section-card">
      <div class="section-title">📜 Buyurtmalar Tarixi</div>
      <div style="display:flex; justify-content:space-between; font-size:12px; font-weight:700; color:#4B5563; margin-bottom:12px;" id="historyStats">
        <span>Yuklanmoqda...</span>
      </div>
      <div id="historyOrdersList">
        <!-- Tarix elementlari -->
      </div>
    </div>
  </div>

  <!-- Chek Pop-up Modali -->
  <div class="modal-backdrop" id="receiptModal">
    <div class="modal-box" id="receiptContent">
      <!-- Chek mazmuni -->
    </div>
  </div>

  <!-- Bottom App Navigation -->
  <nav class="bottom-nav">
    <button class="nav-btn active" onclick="switchTab('catalog')">
      <span style="font-size:18px;">💐</span> Vitrina
    </button>
    <button class="nav-btn" onclick="switchTab('cart')">
      <span style="font-size:18px;">🛒</span> Savatcha
      <span class="badge-count" id="cartBadge" style="display:none;">0</span>
    </button>
    <button class="nav-btn" onclick="switchTab('admin')">
      <span style="font-size:18px;">🔐</span> Admin
    </button>
    <button class="nav-btn" onclick="switchTab('history')">
      <span style="font-size:18px;">📜</span> Tarix
    </button>
  </nav>

  <script>
    let flowers = [];
    let orders = [];
    let cart = {}; // { id: qty }
    let currentCategory = "Barchasi";
    let isAdmin = false;

    async function loadInitialData() {
      const resF = await fetch('/api/flowers');
      flowers = await resF.json();

      const resO = await fetch('/api/orders');
      orders = await resO.json();

      renderCategories();
      renderCatalog();
      updateCartBadge();
    }

    function switchTab(tabId) {
      document.querySelectorAll('.view-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));

      document.getElementById('view-' + tabId).classList.add('active');
      
      const idxMap = { 'catalog': 0, 'cart': 1, 'admin': 2, 'history': 3 };
      document.querySelectorAll('.nav-btn')[idxMap[tabId]].classList.add('active');

      if (tabId === 'cart') renderCartView();
      if (tabId === 'admin') renderAdminView();
      if (tabId === 'history') renderHistoryView();
    }

    // Categories
    function renderCategories() {
      const cats = ["Barchasi", ...new Set(flowers.map(f => f.category || "Boshqa"))];
      const box = document.getElementById('categoryPills');
      box.innerHTML = cats.map(c => `
        <button class="cat-pill ${c === currentCategory ? 'active' : ''}" onclick="selectCategory('${c}')">${c}</button>
      `).join('');
    }

    function selectCategory(cat) {
      currentCategory = cat;
      renderCategories();
      renderCatalog();
    }

    // Catalog Rendering
    function renderCatalog() {
      const q = (document.getElementById('searchInput').value || "").toLowerCase();
      const grid = document.getElementById('flowersGrid');

      const filtered = flowers.filter(f => {
        const matchesQ = f.name.toLowerCase().includes(q) || (f.desc && f.desc.toLowerCase().includes(q));
        const matchesC = currentCategory === "Barchasi" || f.category === currentCategory;
        return matchesQ && matchesC;
      });

      if (filtered.length === 0) {
        grid.innerHTML = `<div style="grid-column: span 2; text-align:center; padding: 40px; color:#9CA3AF;">Gullar topilmadi 🥀</div>`;
        return;
      }

      grid.innerHTML = filtered.map(f => {
        const stockClass = f.stock === 0 ? 'out' : (f.stock < 5 ? 'low' : '');
        const stockText = f.stock > 0 ? f.stock + ' dona' : 'Tugagan';
        return `
          <div class="flower-card">
            <span class="card-stock ${stockClass}">${stockText}</span>
            <div class="card-icon">${f.icon || '🌸'}</div>
            <div class="card-title">${f.name}</div>
            <div class="card-desc">${f.desc || ''}</div>
            <div class="card-footer">
              <div class="card-price">${Number(f.price).toLocaleString()} so'm</div>
              <button class="btn-add" ${f.stock === 0 ? 'disabled' : ''} onclick="addToCart(${f.id})">
                + Savatchaga
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    // Cart logic
    function addToCart(id) {
      const f = flowers.find(x => x.id === id);
      if (!f) return;
      const cur = cart[id] || 0;
      if (cur + 1 > f.stock) {
        alert("Omborda yetarli qoldiq mavjud emas!");
        return;
      }
      cart[id] = cur + 1;
      updateCartBadge();
    }

    function changeCartQty(id, delta) {
      const f = flowers.find(x => x.id === id);
      if (!f) return;
      const next = (cart[id] || 0) + delta;
      if (next <= 0) {
        delete cart[id];
      } else if (next > f.stock) {
        alert("Omborda faqat " + f.stock + " dona mavjud!");
        return;
      } else {
        cart[id] = next;
      }
      renderCartView();
      updateCartBadge();
    }

    function clearCart() {
      if (Object.keys(cart).length === 0) return;
      if (confirm("Savatchani tozalamoqchimisiz?")) {
        cart = {};
        renderCartView();
        updateCartBadge();
      }
    }

    function updateCartBadge() {
      const totalCount = Object.values(cart).reduce((a, b) => a + b, 0);
      const b = document.getElementById('cartBadge');
      if (totalCount > 0) {
        b.style.display = 'block';
        b.innerText = totalCount;
      } else {
        b.style.display = 'none';
      }
    }

    function renderCartView() {
      const container = document.getElementById('cartItemsList');
      const items = Object.keys(cart);

      if (items.length === 0) {
        container.innerHTML = `<div style="text-align:center; padding: 25px; color:#9CA3AF;">Savatchangiz bo'sh 🛒</div>`;
        document.getElementById('cartTotalPrice').innerText = "0 so'm";
        return;
      }

      let totalSum = 0;
      container.innerHTML = items.map(idStr => {
        const id = parseInt(idStr);
        const f = flowers.find(x => x.id === id);
        if (!f) return '';
        const qty = cart[id];
        const cost = f.price * qty;
        totalSum += cost;

        return `
          <div class="cart-item">
            <div>
              <div style="font-weight:700; font-size:13px;">${f.icon || '🌸'} ${f.name}</div>
              <div style="font-size:11px; color:#E11D48; font-weight:700;">${cost.toLocaleString()} so'm</div>
            </div>
            <div class="qty-controls">
              <button class="btn-qty" onclick="changeCartQty(${id}, -1)">-</button>
              <span style="font-size:12px; font-weight:700;">${qty}</span>
              <button class="btn-qty" onclick="changeCartQty(${id}, 1)">+</button>
            </div>
          </div>
        `;
      }).join('');

      document.getElementById('cartTotalPrice').innerText = totalSum.toLocaleString() + " so'm";
    }

    async function submitOrder() {
      const itemIds = Object.keys(cart);
      if (itemIds.length === 0) {
        alert("Savatchangiz bo'sh! Iltimos, gul tanlang.");
        return;
      }

      const name = document.getElementById('orderCustName').value.trim();
      const phone = document.getElementById('orderCustPhone').value.trim();
      const address = document.getElementById('orderCustAddress').value.trim() || "Do'kondan olib ketish";
      const note = document.getElementById('orderCustNote').value.trim();
      const payMethod = document.getElementById('orderPayMethod').value;
      const cardTx = document.getElementById('orderCardTx').value.trim();

      if (!name || name.length < 2) {
        alert("Iltimos, mijoz ismini kiriting!");
        return;
      }
      if (!phone || phone.length < 9) {
        alert("Iltimos, to'liq telefon raqamini kiriting!");
        return;
      }
      if (!cardTx) {
        alert("⚠️ Faqat karta orqali to'lov qabul qilinadi!\nIltimos, karta oxirgi 4 raqami yoki chek tranzaksiya ID sini kiriting.");
        return;
      }

      const orderItems = [];
      let totalAmount = 0;
      for (const idStr of itemIds) {
        const id = parseInt(idStr);
        const f = flowers.find(x => x.id === id);
        const qty = cart[id];
        const cost = f.price * qty;
        totalAmount += cost;
        orderItems.append ? null : orderItems.push({
          id: f.id,
          name: f.name,
          price: f.price,
          qty: qty,
          total: cost
        });
      }

      const payload = {
        customer: name,
        phone: phone,
        address: address,
        note: note,
        items: orderItems,
        total: totalAmount,
        payment_type: "Karta (" + payMethod + ")",
        card_tx: cardTx
      };

      const res = await fetch('/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (data.success) {
        cart = {};
        updateCartBadge();
        document.getElementById('orderCustName').value = "";
        document.getElementById('orderCustAddress').value = "";
        document.getElementById('orderCustNote').value = "";
        document.getElementById('orderCardTx').value = "";

        await loadInitialData();
        showReceiptModal(data.order);
      } else {
        alert(data.message || "Xatolik yuz berdi!");
      }
    }

    // Receipt Modal
    function showReceiptModal(ord) {
      const itemsHtml = ord.items.map(it => `
        <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
          <span>${it.name} x${it.qty}</span>
          <span style="font-weight:700;">${it.total.toLocaleString()} so'm</span>
        </div>
      `).join('');

      document.getElementById('receiptContent').innerHTML = `
        <div style="text-align:center; margin-bottom:12px;">
          <div style="font-size:24px;">🌸</div>
          <div style="font-weight:800; font-size:17px; color:#E11D48;">${ord.shop || 'Melfis Flowers'}</div>
          <div style="font-size:11px; color:#6B7280;">Samarqand shahri | @samarqand.melfisflowers</div>
        </div>
        <hr style="border:none; border-top:1px dashed #E5E7EB; margin:10px 0;">
        <div style="font-size:12px; line-height:1.6;">
          <div><strong>Buyurtma №:</strong> #${ord.order_id}</div>
          <div><strong>Sana:</strong> ${ord.date}</div>
          <div><strong>Mijoz:</strong> ${ord.customer} (${ord.phone})</div>
          <div><strong>Manzil:</strong> ${ord.address}</div>
          <div><strong>To'lov:</strong> 💳 ${ord.payment_type}</div>
          <div><strong>Chek/Karta:</strong> ${ord.card_tx || '-'}</div>
          ${ord.note ? `<div><strong>Izoh:</strong> ${ord.note}</div>` : ''}
        </div>
        <hr style="border:none; border-top:1px dashed #E5E7EB; margin:10px 0;">
        <div style="font-weight:700; font-size:12px; margin-bottom:6px;">MAHSULOTLAR:</div>
        ${itemsHtml}
        <hr style="border:none; border-top:2px solid #E11D48; margin:10px 0;">
        <div style="display:flex; justify-content:space-between; font-weight:800; font-size:15px; color:#E11D48;">
          <span>JAMI TO'LANDI:</span>
          <span>${ord.total.toLocaleString()} so'm</span>
        </div>
        <button class="btn-submit" style="margin-top:15px;" onclick="closeReceiptModal()">Yopish</button>
      `;

      document.getElementById('receiptModal').style.display = 'flex';
    }

    function closeReceiptModal() {
      document.getElementById('receiptModal').style.display = 'none';
      switchTab('catalog');
    }

    // Admin
    function checkAdminLogin() {
      const u = document.getElementById('adminUser').value.trim();
      const p = document.getElementById('adminPass').value.trim();
      if (u === "admin" && p === "123") {
        isAdmin = true;
        renderAdminView();
      } else {
        alert("Login yoki parol noto'g'ri! (Standart: admin / 123)");
      }
    }

    function adminLogout() {
      isAdmin = false;
      renderAdminView();
    }

    function renderAdminView() {
      if (!isAdmin) {
        document.getElementById('adminLoginCard').style.display = 'block';
        document.getElementById('adminDashboardCard').style.display = 'none';
        return;
      }
      document.getElementById('adminLoginCard').style.display = 'none';
      document.getElementById('adminDashboardCard').style.display = 'block';

      const list = document.getElementById('adminFlowersList');
      list.innerHTML = flowers.map(f => `
        <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #F3F4F6;">
          <div>
            <div style="font-weight:700; font-size:13px;">${f.icon || '🌸'} ${f.name}</div>
            <div style="font-size:11px; color:#6B7280;">${f.category} • ${Number(f.price).toLocaleString()} so'm • ${f.stock} dona</div>
          </div>
          <div style="display:flex; gap:6px;">
            <button onclick="editFlower(${f.id})" style="background:#F3F4F6; border:none; padding:4px 8px; border-radius:6px; font-size:11px;">✏️</button>
            <button onclick="deleteFlower(${f.id})" style="background:#FEE2E2; color:#DC2626; border:none; padding:4px 8px; border-radius:6px; font-size:11px;">🗑️</button>
          </div>
        </div>
      `).join('');
    }

    function editFlower(id) {
      const f = flowers.find(x => x.id === id);
      if (!f) return;
      document.getElementById('editFlowerId').value = f.id;
      document.getElementById('flowerName').value = f.name;
      document.getElementById('flowerCategory').value = f.category || '';
      document.getElementById('flowerPrice').value = f.price;
      document.getElementById('flowerStock').value = f.stock;
      document.getElementById('flowerIcon').value = f.icon || '🌸';
      document.getElementById('flowerDesc').value = f.desc || '';
      document.getElementById('flowerFormTitle').innerText = "Tahrirlash: #" + f.id;
    }

    async function saveFlower() {
      const id = document.getElementById('editFlowerId').value;
      const name = document.getElementById('flowerName').value.trim();
      const cat = document.getElementById('flowerCategory').value.trim() || 'Boshqa';
      const price = parseInt(document.getElementById('flowerPrice').value);
      const stock = parseInt(document.getElementById('flowerStock').value);
      const icon = document.getElementById('flowerIcon').value.trim() || '🌸';
      const desc = document.getElementById('flowerDesc').value.trim();

      if (!name || isNaN(price) || isNaN(stock)) {
        alert("Iltimos, ma'lumotlarni to'liq kiriting!");
        return;
      }

      const payload = { id: id ? parseInt(id) : null, name, category: cat, price, stock, icon, desc };
      const res = await fetch('/api/flowers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.success) {
        document.getElementById('editFlowerId').value = '';
        document.getElementById('flowerName').value = '';
        document.getElementById('flowerCategory').value = '';
        document.getElementById('flowerPrice').value = '';
        document.getElementById('flowerStock').value = '';
        document.getElementById('flowerDesc').value = '';
        document.getElementById('flowerFormTitle').innerText = "Yangi Gul Qo'shish";
        await loadInitialData();
        renderAdminView();
      }
    }

    async function deleteFlower(id) {
      if (!confirm("Haqiqatan ham bu gulni o'chirmoqchimisiz?")) return;
      const res = await fetch('/api/flowers/' + id, { method: 'DELETE' });
      const data = await res.json();
      if (data.success) {
        await loadInitialData();
        renderAdminView();
      }
    }

    // History
    function renderHistoryView() {
      const container = document.getElementById('historyOrdersList');
      const stats = document.getElementById('historyStats');

      let totalRevenue = orders.reduce((s, o) => s + (o.total || 0), 0);
      stats.innerHTML = `<span>Jami: ${orders.length} ta buyurtma</span><span style="color:#E11D48;">${totalRevenue.toLocaleString()} so'm</span>`;

      if (orders.length === 0) {
        container.innerHTML = `<div style="text-align:center; padding: 25px; color:#9CA3AF;">Hozircha buyurtmalar yo'q</div>`;
        return;
      }

      container.innerHTML = orders.slice().reverse().map(o => {
        return `
          <div style="background:#F9FAFB; border-radius:12px; padding:12px; margin-bottom:10px; border:1px solid #E5E7EB;" onclick="showReceiptModal(${JSON.stringify(o).replace(/"/g, '&quot;')})">
            <div style="display:flex; justify-content:space-between; font-weight:700; font-size:13px; margin-bottom:4px;">
              <span>#${o.order_id} - ${o.customer}</span>
              <span style="color:#E11D48;">${Number(o.total).toLocaleString()} so'm</span>
            </div>
            <div style="font-size:11px; color:#6B7280; display:flex; justify-content:space-between;">
              <span>${o.date}</span>
              <span style="color:#059669; font-weight:700;">💳 ${o.payment_type || 'Karta'}</span>
            </div>
          </div>
        `;
      }).join('');
    }

    // On Load
    window.addEventListener('DOMContentLoaded', loadInitialData);
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(MOBILE_HTML)

@app.route("/api/flowers", methods=["GET"])
def get_flowers():
    return jsonify(load_data())

@app.route("/api/flowers", methods=["POST"])
def add_or_update_flower():
    flowers = load_data()
    req = request.json
    f_id = req.get("id")

    if f_id:
        for f in flowers:
            if f["id"] == f_id:
                f["name"] = req["name"]
                f["category"] = req["category"]
                f["price"] = req["price"]
                f["stock"] = req["stock"]
                f["icon"] = req["icon"]
                f["desc"] = req["desc"]
                break
    else:
        new_id = max([f["id"] for f in flowers], default=0) + 1
        flowers.append({
            "id": new_id,
            "name": req["name"],
            "category": req["category"],
            "price": req["price"],
            "stock": req["stock"],
            "icon": req["icon"],
            "desc": req["desc"]
        })

    save_data(flowers)
    return jsonify({"success": True})

@app.route("/api/flowers/<int:flower_id>", methods=["DELETE"])
def delete_flower(flower_id):
    flowers = load_data()
    flowers = [f for f in flowers if f["id"] != flower_id]
    save_data(flowers)
    return jsonify({"success": True})

@app.route("/api/orders", methods=["GET"])
def get_orders():
    return jsonify(load_orders())

@app.route("/api/orders", methods=["POST"])
def create_order():
    flowers = load_data()
    orders = load_orders()
    req = request.json

    items = req.get("items", [])
    # Ombordagi qoldiqni ayirish
    for item in items:
        f_id = item["id"]
        qty = item["qty"]
        for f in flowers:
            if f["id"] == f_id:
                if f["stock"] < qty:
                    return jsonify({"success": False, "message": f"'{f['name']}' yetarli emas!"})
                f["stock"] -= qty

    new_order = {
        "order_id": len(orders) + 1001,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "customer": req.get("customer"),
        "phone": req.get("phone"),
        "address": req.get("address"),
        "note": req.get("note", ""),
        "items": items,
        "total": req.get("total", 0),
        "payment_type": req.get("payment_type", "Karta (Uzcard / Humo)"),
        "card_tx": req.get("card_tx", "-"),
        "status": "To'landi (Karta)"
    }

    orders.append(new_order)
    save_data(flowers)
    save_orders(orders)

    return jsonify({"success": True, "order": new_order})

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

if __name__ == "__main__":
    ip = get_local_ip()
    port = 5000
    print("=" * 60)
    print(f"🌸 MELFIS FLOWERS SAMARQAND - TELEFON ILOVASI ISHGA TUSHDI")
    print(f"📱 Telefoningiz brauzerida oching: http://{ip}:{port}")
    print("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=False)

